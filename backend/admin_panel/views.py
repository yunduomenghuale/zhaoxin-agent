import time
import os
import tempfile
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_community.document_loaders import Docx2txtLoader
from .models import AdminUser, KnowledgeDocument, SystemPrompt, KnowledgeImage, PromptTemplate
from assistant.services.knowledge import knowledge_service


def _check_login(request):
    return request.session.get('admin_user_id') is not None


def _get_current_user(request):
    user_id = request.session.get('admin_user_id')
    if user_id:
        try:
            return AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return None
    return None


class AdminLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        if not username or not password:
            return Response({'error': '请输入用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        request.session['admin_user_id'] = user.id

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
            }
        })


class AdminLogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        logout(request)
        request.session.flush()
        return Response({'message': '已退出登录'})


class AdminCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        user = _get_current_user(request)
        if user:
            return Response({
                'logged_in': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                }
            })
        return Response({'logged_in': False})


class AdminUserListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足，仅管理员可管理用户'}, status=status.HTTP_403_FORBIDDEN)

        users = AdminUser.objects.all()
        data = []
        for u in users:
            data.append({
                'id': u.id,
                'username': u.username,
                'role': u.role,
                'is_active': u.is_active,
                'date_joined': u.date_joined.strftime('%Y-%m-%d %H:%M'),
            })
        return Response({'users': data})

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足，仅管理员可创建用户'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username', '')
        password = request.data.get('password', '')
        role = request.data.get('role', 'editor')

        if not username or not password:
            return Response({'error': '请输入用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)

        if AdminUser.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

        user = AdminUser.objects.create_user(username=username, password=password, role=role)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
            }
        })


class AdminUserDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        current_user = _get_current_user(request)
        if current_user.role != 'admin':
            return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = AdminUser.objects.get(pk=pk)
        except AdminUser.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        new_password = request.data.get('password', '')
        role = request.data.get('role', user.role)
        is_active = request.data.get('is_active', user.is_active)

        if new_password:
            user.set_password(new_password)
        user.role = role
        user.is_active = is_active
        user.save()

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'is_active': user.is_active,
            }
        })

    def delete(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        current_user = _get_current_user(request)
        if current_user.role != 'admin':
            return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)

        if current_user and current_user.id == pk:
            return Response({'error': '不能删除当前登录用户'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AdminUser.objects.get(pk=pk)
            user.delete()
            return Response({'message': '用户已删除'})
        except AdminUser.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)


class KnowledgeDocumentListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        keyword = request.query_params.get('keyword', '')
        queryset = KnowledgeDocument.objects.all()
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))

        data = []
        for doc in queryset:
            data.append({
                'id': doc.id,
                'title': doc.title,
                'content': doc.content,
                'source_file': doc.source_file,
                'is_active': doc.is_active,
                'created_at': doc.created_at.strftime('%Y-%m-%d %H:%M'),
                'updated_at': doc.updated_at.strftime('%Y-%m-%d %H:%M'),
            })
        return Response({'documents': data, 'total': queryset.count()})

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        file_obj = request.FILES.get('file')
        title = request.data.get('title', '')
        is_active = request.data.get('is_active', 'true').lower() == 'true'

        if not file_obj:
            return Response({'error': '请选择要上传的文件'}, status=status.HTTP_400_BAD_REQUEST)

        filename = file_obj.name
        ext = os.path.splitext(filename)[1].lower()
        
        if not title:
            title = filename

        content = ""
        try:
            if ext == '.docx':
                with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                    for chunk in file_obj.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name
                
                try:
                    loader = Docx2txtLoader(tmp_path)
                    docs = loader.load()
                    content = "\n".join([doc.page_content for doc in docs])
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            
            elif ext == '.txt':
                content = file_obj.read().decode('utf-8')
            
            else:
                return Response({'error': '不支持的文件类型，仅支持 .docx 和 .txt'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'解析文件失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not content.strip():
            return Response({'error': '文档内容为空'}, status=status.HTTP_400_BAD_REQUEST)

        doc = KnowledgeDocument.objects.create(
            title=title,
            content=content,
            source_file=filename,
            is_active=is_active,
        )
        
        # 刷新知识库缓存
        knowledge_service.refresh()
        
        return Response({
            'document': {
                'id': doc.id,
                'title': doc.title,
                'source_file': doc.source_file,
                'is_active': doc.is_active,
                'created_at': doc.created_at.strftime('%Y-%m-%d %H:%M'),
            }
        })


class KnowledgeDocumentDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            doc = KnowledgeDocument.objects.get(pk=pk)
        except KnowledgeDocument.DoesNotExist:
            return Response({'error': '文档不存在'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'document': {
                'id': doc.id,
                'title': doc.title,
                'content': doc.content,
                'source_file': doc.source_file,
                'is_active': doc.is_active,
                'created_at': doc.created_at.strftime('%Y-%m-%d %H:%M'),
                'updated_at': doc.updated_at.strftime('%Y-%m-%d %H:%M'),
            }
        })

    def put(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            doc = KnowledgeDocument.objects.get(pk=pk)
        except KnowledgeDocument.DoesNotExist:
            return Response({'error': '文档不存在'}, status=status.HTTP_404_NOT_FOUND)

        doc.title = request.data.get('title', doc.title)
        doc.content = request.data.get('content', doc.content)
        doc.source_file = request.data.get('source_file', doc.source_file)
        doc.is_active = request.data.get('is_active', doc.is_active)
        doc.save()
        
        # 刷新知识库缓存
        knowledge_service.refresh()

        return Response({
            'document': {
                'id': doc.id,
                'title': doc.title,
                'content': doc.content,
                'source_file': doc.source_file,
                'is_active': doc.is_active,
                'updated_at': doc.updated_at.strftime('%Y-%m-%d %H:%M'),
            }
        })

    def delete(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            doc = KnowledgeDocument.objects.get(pk=pk)
            doc.delete()
            # 刷新知识库缓存
            knowledge_service.refresh()
            return Response({'message': '文档已删除'})
        except KnowledgeDocument.DoesNotExist:
            return Response({'error': '文档不存在'}, status=status.HTTP_404_NOT_FOUND)


class SystemPromptListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        prompts = SystemPrompt.objects.all()
        data = []
        for p in prompts:
            data.append({
                'id': p.id,
                'name': p.name,
                'role': p.role,
                'skills': p.skills,
                'content': p.content,
                'is_active': p.is_active,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M'),
                'updated_at': p.updated_at.strftime('%Y-%m-%d %H:%M'),
            })
        return Response({'prompts': data})

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name', '')
        role = request.data.get('role', '')
        skills = request.data.get('skills', '')
        is_active = request.data.get('is_active', False)

        if not name:
            return Response({'error': '请输入名称'}, status=status.HTTP_400_BAD_REQUEST)

        if is_active:
            SystemPrompt.objects.filter(is_active=True).update(is_active=False)

        prompt = SystemPrompt.objects.create(
            name=name,
            role=role,
            skills=skills,
            is_active=is_active,
        )
        return Response({
            'prompt': {
                'id': prompt.id,
                'name': prompt.name,
                'role': prompt.role,
                'skills': prompt.skills,
                'is_active': prompt.is_active,
                'created_at': prompt.created_at.strftime('%Y-%m-%d %H:%M'),
            }
        })


class SystemPromptDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            prompt = SystemPrompt.objects.get(pk=pk)
        except SystemPrompt.DoesNotExist:
            return Response({'error': '提示词不存在'}, status=status.HTTP_404_NOT_FOUND)

        prompt.name = request.data.get('name', prompt.name)
        prompt.role = request.data.get('role', prompt.role)
        prompt.skills = request.data.get('skills', prompt.skills)
        is_active = request.data.get('is_active', prompt.is_active)

        if is_active and not prompt.is_active:
            SystemPrompt.objects.filter(is_active=True).update(is_active=False)

        prompt.is_active = is_active
        prompt.save()

        return Response({
            'prompt': {
                'id': prompt.id,
                'name': prompt.name,
                'role': prompt.role,
                'skills': prompt.skills,
                'is_active': prompt.is_active,
                'updated_at': prompt.updated_at.strftime('%Y-%m-%d %H:%M'),
            }
        })

    def delete(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            prompt = SystemPrompt.objects.get(pk=pk)
            prompt.delete()
            return Response({'message': '提示词已删除'})
        except SystemPrompt.DoesNotExist:
            return Response({'error': '提示词不存在'}, status=status.HTTP_404_NOT_FOUND)


class SystemPromptActivateView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            SystemPrompt.objects.filter(is_active=True).update(is_active=False)
            prompt = SystemPrompt.objects.get(pk=pk)
            prompt.is_active = True
            prompt.save()
            return Response({'message': '提示词已激活'})
        except SystemPrompt.DoesNotExist:
            return Response({'error': '提示词不存在'}, status=status.HTTP_404_NOT_FOUND)


class KnowledgeImageListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        images = KnowledgeImage.objects.all()
        data = []
        for img in images:
            data.append({
                'id': img.id,
                'title': img.title,
                'url': request.build_absolute_uri(img.image.url),
                'tags': img.tags,
                'created_at': img.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        return Response({'images': data})

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        title = request.data.get('title', '')
        image_file = request.FILES.get('image')
        tags = request.data.get('tags', '')

        if not image_file:
            return Response({'error': '请选择图片文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not title:
            title = image_file.name

        img = KnowledgeImage.objects.create(
            title=title,
            image=image_file,
            tags=tags
        )
        # 刷新知识库缓存
        knowledge_service.refresh()
        return Response({
            'image': {
                'id': img.id,
                'title': img.title,
                'url': request.build_absolute_uri(img.image.url),
                'tags': img.tags,
            }
        })


class KnowledgeImageDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def delete(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            img = KnowledgeImage.objects.get(pk=pk)
            if img.image:
                if os.path.exists(img.image.path):
                    os.remove(img.image.path)
            img.delete()
            # 刷新知识库缓存
            knowledge_service.refresh()
            return Response({'message': '图片已删除'})
        except KnowledgeImage.DoesNotExist:
            return Response({'error': '图片不存在'}, status=status.HTTP_404_NOT_FOUND)


class SystemSettingsView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        from assistant.services.config import get_system_config
        config = get_system_config()
        # Make avatar URL absolute for admin panel preview
        if config['assistant_avatar'] and config['assistant_avatar'].startswith('/media/'):
             config['assistant_avatar'] = request.build_absolute_uri(config['assistant_avatar'])
        return Response(config)

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足，仅管理员可修改系统设置'}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('assistant_name')
        subtitle = request.data.get('assistant_subtitle')
        footer = request.data.get('assistant_footer')
        welcome_questions_raw = request.data.get('welcome_questions')
        greeting = request.data.get('system_greeting')
        
        welcome_questions = None
        if welcome_questions_raw:
            import json
            try:
                welcome_questions = json.loads(welcome_questions_raw) if isinstance(welcome_questions_raw, str) else welcome_questions_raw
            except:
                pass

        avatar_file = request.FILES.get('assistant_avatar')
        
        avatar_url = None
        if avatar_file:
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            # Use assistant/avatar_filename to store
            path = default_storage.save(f'system/assistant_{int(time.time())}{os.path.splitext(avatar_file.name)[1]}', ContentFile(avatar_file.read()))
            avatar_url = settings.MEDIA_URL + path
            
        from assistant.services.config import update_system_config
        config = update_system_config(
            name=name, 
            avatar_url=avatar_url, 
            subtitle=subtitle, 
            footer=footer, 
            welcome_questions=welcome_questions, 
            greeting=greeting,
            llm_model=request.data.get('llm_model'),
            llm_api_key=request.data.get('llm_api_key'),
            llm_provider=request.data.get('llm_provider'),
            llm_base_url=request.data.get('llm_base_url')
        )
        # Make avatar URL absolute for immediate frontend update
        if config['assistant_avatar'] and config['assistant_avatar'].startswith('/media/'):
             config['assistant_avatar'] = request.build_absolute_uri(config['assistant_avatar'])
        return Response(config)


class PromptTemplateListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        
        templates = PromptTemplate.objects.all()
        data = []
        for t in templates:
            data.append({
                'id': t.id,
                'name': t.name,
                'role': t.role,
                'skills': t.skills,
                'created_at': t.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        return Response({'templates': data})

    def post(self, request):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足，仅管理员可创建模板'}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name', '')
        role = request.data.get('role', '')
        skills = request.data.get('skills', '')

        if not name or not role or not skills:
            return Response({'error': '名称、角色设定和技能描述均为必填项'}, status=status.HTTP_400_BAD_REQUEST)

        template = PromptTemplate.objects.create(
            name=name,
            role=role,
            skills=skills
        )
        return Response({
            'template': {
                'id': template.id,
                'name': template.name,
                'role': template.role,
                'skills': template.skills,
            }
        })


class PromptTemplateDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)

        try:
            template = PromptTemplate.objects.get(pk=pk)
        except PromptTemplate.DoesNotExist:
            return Response({'error': '模板不存在'}, status=status.HTTP_404_NOT_FOUND)

        template.name = request.data.get('name', template.name)
        template.role = request.data.get('role', template.role)
        template.skills = request.data.get('skills', template.skills)
        template.save()

        return Response({'message': '更新成功'})

    def delete(self, request, pk):
        if not _check_login(request):
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

        user = _get_current_user(request)
        if user.role != 'admin':
            return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)

        try:
            template = PromptTemplate.objects.get(pk=pk)
            template.delete()
            return Response({'message': '模板已删除'})
        except PromptTemplate.DoesNotExist:
            return Response({'error': '模板不存在'}, status=status.HTTP_404_NOT_FOUND)
