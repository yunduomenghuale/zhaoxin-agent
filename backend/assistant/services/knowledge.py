import re
import os
import json
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from django.conf import settings


class KnowledgeService:
    def __init__(self):
        self.knowledge_base = []
        self.image_base = []
        self._loaded = False
        self.embeddings_model = DashScopeEmbeddings(
            model="text-embedding-v2",
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        self.cache_path = os.path.join(settings.BASE_DIR, 'media', 'embeddings_cache.json')
        self._embedding_cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载向量缓存失败: {e}")
        return {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self._embedding_cache, f, ensure_ascii=False)
        except Exception as e:
            print(f"保存向量缓存失败: {e}")

    def load_documents(self):
        self.knowledge_base = []
        self.image_base = []
        self._load_db_documents()
        self._load_db_images()
        self._loaded = True

    def _load_db_documents(self):
        try:
            from admin_panel.models import KnowledgeDocument
            db_docs = KnowledgeDocument.objects.filter(is_active=True)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
            )
            from langchain_core.documents import Document
            
            all_chunks = []
            for doc in db_docs:
                langchain_doc = Document(
                    page_content=doc.content,
                    metadata={'source': doc.title}
                )
                chunks = splitter.split_documents([langchain_doc])
                for chunk in chunks:
                    all_chunks.append({
                        'source': doc.title,
                        'content': chunk.page_content,
                    })
            
            if all_chunks:
                # 找出不在缓存中的片段
                missing_texts = []
                for chunk in all_chunks:
                    if chunk['content'] not in self._embedding_cache:
                        missing_texts.append(chunk['content'])
                
                if missing_texts:
                    print(f"正在为 {len(missing_texts)} 个新片段生成向量...")
                    # 批量生成向量
                    new_embeddings = self.embeddings_model.embed_documents(missing_texts)
                    for i, text in enumerate(missing_texts):
                        self._embedding_cache[text] = new_embeddings[i]
                    self._save_cache()
                    print("向量生成完成")
                
                # 从缓存中填入所有向量
                for chunk in all_chunks:
                    chunk['embedding'] = self._embedding_cache[chunk['content']]
            
            self.knowledge_base = all_chunks
        except Exception as e:
            print(f"加载数据库文档失败: {e}")

    def _load_db_images(self):
        try:
            from admin_panel.models import KnowledgeImage
            db_images = KnowledgeImage.objects.all()
            all_images = []
            for img in db_images:
                text_to_embed = f"{img.title} {img.tags}".strip()
                if not text_to_embed:
                    text_to_embed = "图片"
                all_images.append({
                    'title': img.title,
                    'url': img.image.url,
                    'tags': img.tags,
                    'text': text_to_embed
                })
            
            if all_images:
                missing_texts = []
                for img in all_images:
                    if img['text'] not in self._embedding_cache:
                        missing_texts.append(img['text'])
                
                if missing_texts:
                    print(f"正在为 {len(missing_texts)} 个图片生成向量...")
                    new_embeddings = self.embeddings_model.embed_documents(missing_texts)
                    for i, text in enumerate(missing_texts):
                        self._embedding_cache[text] = new_embeddings[i]
                    self._save_cache()
                    print("图片向量生成完成")
                
                for img in all_images:
                    img['embedding'] = self._embedding_cache[img['text']]
            
            self.image_base = all_images
        except Exception as e:
            print(f"加载图片数据库失败: {e}")

    def search(self, query, top_k=5):
        if not query:
            return []

        if not self._loaded:
            self.load_documents()

        if not self.knowledge_base:
            return []

        # 1. 计算语义相似度
        try:
            query_embedding = self.embeddings_model.embed_query(query)
            chunk_embeddings = np.array([item['embedding'] for item in self.knowledge_base])
            query_vec = np.array(query_embedding)
            
            dot_product = np.dot(chunk_embeddings, query_vec)
            norm_a = np.linalg.norm(chunk_embeddings, axis=1)
            norm_b = np.linalg.norm(query_vec)
            similarities = dot_product / (norm_a * norm_b + 1e-9)
        except Exception as e:
            print(f"语义搜索失败: {e}")
            similarities = np.zeros(len(self.knowledge_base))

        # 2. 计算关键词得分
        keywords = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z0-9]+', query.lower())
        
        scored_results = []
        for i, item in enumerate(self.knowledge_base):
            content_lower = item['content'].lower()
            keyword_score = 0
            for kw in keywords:
                if kw in content_lower:
                    keyword_score += 1 + content_lower.count(kw) * 0.1
            
            normalized_kw_score = min(keyword_score / (len(keywords) + 0.1), 1.0) if keywords else 0
            
            # 混合得分
            final_score = similarities[i] * 0.85 + normalized_kw_score * 0.15
            
            if final_score > 0.25:
                scored_results.append({
                    'source': item['source'],
                    'content': item['content'],
                    'score': float(final_score),
                })

        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return scored_results[:top_k]

    def search_images(self, query, top_k=3):
        if not query:
            return []

        if not self._loaded:
            self.load_documents()

        if not self.image_base:
            return []

        try:
            query_embedding = self.embeddings_model.embed_query(query)
            img_embeddings = np.array([img['embedding'] for img in self.image_base])
            query_vec = np.array(query_embedding)
            
            dot_product = np.dot(img_embeddings, query_vec)
            norm_a = np.linalg.norm(img_embeddings, axis=1)
            norm_b = np.linalg.norm(query_vec)
            similarities = dot_product / (norm_a * norm_b + 1e-9)
            
            keywords = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z0-9]+', query.lower())
            
            scored_images = []
            for i, img in enumerate(self.image_base):
                text_lower = img['text'].lower()
                kw_score = 0
                for kw in keywords:
                    if kw in text_lower:
                        kw_score += 1
                
                norm_kw_score = min(kw_score / (len(keywords) + 0.1), 1.0) if keywords else 0
                final_score = similarities[i] * 0.7 + norm_kw_score * 0.3
                
                if final_score > 0.3:
                    scored_images.append({
                        'title': img['title'],
                        'url': img['url'],
                        'tags': img['tags'],
                        'score': float(final_score)
                    })
            
            scored_images.sort(key=lambda x: x['score'], reverse=True)
            return scored_images[:top_k]
            
        except Exception as e:
            print(f"图片搜索失败: {e}")
            return self._fallback_image_search(query, top_k)

    def _fallback_image_search(self, query, top_k):
        try:
            from admin_panel.models import KnowledgeImage
            from django.db.models import Q
            keywords = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z0-9]+', query.lower())
            if not keywords: return []
            q_obj = Q()
            for kw in keywords:
                q_obj |= Q(title__icontains=kw) | Q(tags__icontains=kw)
            images = KnowledgeImage.objects.filter(q_obj).distinct()[:top_k]
            return [{'title': img.title, 'url': img.image.url, 'tags': img.tags} for img in images]
        except:
            return []

    def list_documents(self):
        if not self._loaded:
            self.load_documents()

        doc_counts = {}
        for item in self.knowledge_base:
            source = item['source']
            doc_counts[source] = doc_counts.get(source, 0) + 1

        return [{'name': name, 'chunks': count} for name, count in doc_counts.items()]

    def refresh(self):
        self.load_documents()


knowledge_service = KnowledgeService()