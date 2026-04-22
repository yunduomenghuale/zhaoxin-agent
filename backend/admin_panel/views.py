import time
import os
import tempfile
import logging
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_community.document_loaders import Docx2txtLoader
from .models import AdminUser, KnowledgeDocument, SystemPrompt, KnowledgeImage, PromptTemplate
from assistant.services.knowledge import knowledge_service

logger = logging.getLogger(__name__)


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


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class RateLimiter:
    _storage = {}
    _window = 60
    _max_attempts = 5

    @classmethod
    def is_allowed(cls, key):
        now = time.time()
        if key not in cls._storage:
            cls._storage[key] = []
        cls._storage[key] = [t for t in cls._storage[key] if now - t < cls._window]
        if len(cls._storage[key]) >= cls._max_attempts:
            return False
        cls._storage[key].append(now)
        return True


def _validate_password(password):
    if len(password) < 6:
        return '密码长度不能少于 6 位'
    return None


class AdminLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        ip = _get_client_ip(request)

        if not RateLimiter.is_allowed(f'login:{ip}'):
            logger.warning(f'Login rate limit exceeded for IP: {ip}')
            return Response({'error': '登录尝试过于频繁，请稍后再试'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if not username or not password:
            return Response({'error': '请输入用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            logger.warning(f'Failed login attempt for username: {username} from IP: {ip}')
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': '该账号已被禁用'}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)
        request.session['admin_user_id'] = user.id
        logger.info(f'User {username} logged in from IP: {ip}')

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

        pwd_error = _validate_password(password)
        if pwd_error:
            return Response({'error': pwd_error}, status=status.HTTP_400_BAD_REQUEST)

        if AdminUser.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = AdminUser.objects.create_user(username=username, password=password, role=role)
        logger.info(f'Admin {user.username} created new user {username} with role {role}')
        return Response({
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'role': new_user.role,
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

        username = request.data.get('username', '').strip()
        new_password = request.data.get('password', '')
        role = request.data.get('role', user.role)
        is_active_raw = request.data.get('is_active', user.is_active)
        # 处理字符串类型的布尔值（前端 select 可能传递字符串）
        if isinstance(is_active_raw, str):
            is_active = is_active_raw.lower() in ('true', '1', 'yes', 'on')
        else:
            is_active = bool(is_active_raw)

        if not username:
            return Response({'error': '用户名不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查用户名是否被其他用户使用
        if username != user.username and AdminUser.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password:
            pwd_error = _validate_password(new_password)
            if pwd_error:
                return Response({'error': pwd_error}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
        user.username = username
        user.role = role
        user.is_active = is_active
        user.save()
        logger.info(f'Admin {current_user.username} updated user {user.username}')

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
            username = user.username
            user.delete()
            logger.info(f'Admin {current_user.username} deleted user {username}')
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

        # 检查文档数量上限
        current_count = KnowledgeDocument.objects.count()
        if current_count >= settings.MAX_KNOWLEDGE_DOCS:
            return Response(
                {'error': f'知识库文档数量已达上限（{settings.MAX_KNOWLEDGE_DOCS} 篇），请先删除部分文档后再上传'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES.get('file')
        title = request.data.get('title', '')
        is_active = request.data.get('is_active', 'true').lower() == 'true'

        if not file_obj:
            return Response({'error': '请选择要上传的文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查文件大小
        if file_obj.size > settings.MAX_UPLOAD_SIZE:
            return Response(
                {'error': f'文件大小超过限制（最大 {settings.MAX_UPLOAD_SIZE_MB}MB）'},
                status=status.HTTP_400_BAD_REQUEST
            )

        filename = file_obj.name
        ext = os.path.splitext(filename)[1].lower()

        # 检查文件扩展名
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            return Response(
                {'error': f'不支持的文件类型，仅支持 {", ".join(settings.ALLOWED_UPLOAD_EXTENSIONS)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

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

        except Exception as e:
            logger.error(f'Parse document failed: {str(e)}', exc_info=True)
            return Response({'error': '解析文件失败，请检查文件格式是否正确'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not content.strip():
            return Response({'error': '文档内容为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查内容长度（防止超大文本）
        if len(content) > 500000:
            return Response(
                {'error': '文档内容过长（超过 50 万字符），请拆分为多个文档上传'},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc = KnowledgeDocument.objects.create(
            title=title,
            content=content,
            source_file=filename,
            is_active=is_active,
        )

        # 刷新知识库缓存
        knowledge_service.refresh()
        logger.info(f'User {_get_current_user(request).username} uploaded document: {filename} ({file_obj.size} bytes)')

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

        # 检查图片数量上限
        current_count = KnowledgeImage.objects.count()
        if current_count >= settings.MAX_KNOWLEDGE_IMAGES:
            return Response(
                {'error': f'知识库图片数量已达上限（{settings.MAX_KNOWLEDGE_IMAGES} 张），请先删除部分图片后再上传'},
                status=status.HTTP_400_BAD_REQUEST
            )

        title = request.data.get('title', '')
        image_file = request.FILES.get('image')
        tags = request.data.get('tags', '')

        if not image_file:
            return Response({'error': '请选择图片文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查文件大小
        if image_file.size > settings.MAX_UPLOAD_SIZE:
            return Response(
                {'error': f'图片大小超过限制（最大 {settings.MAX_UPLOAD_SIZE_MB}MB）'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 检查文件扩展名
        ext = os.path.splitext(image_file.name)[1].lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            return Response(
                {'error': f'不支持的图片格式，仅支持 {", ".join(settings.ALLOWED_IMAGE_EXTENSIONS)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not title:
            title = image_file.name

        img = KnowledgeImage.objects.create(
            title=title,
            image=image_file,
            tags=tags
        )
        # 刷新知识库缓存
        knowledge_service.refresh()
        logger.info(f'User {_get_current_user(request).username} uploaded image: {image_file.name} ({image_file.size} bytes)')
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
