import json
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.assistant import chat_with_assistant, chat_with_assistant_stream
from .services.knowledge import knowledge_service


class HealthView(APIView):
    def get(self, request):
        return Response({'status': 'ok', 'message': '迎新智能助手服务运行正常'})


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        message = request.data.get('message', '')
        history = request.data.get('history', [])

        if not message:
            return Response(
                {'error': '请提供消息内容'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reply = chat_with_assistant(message, history)
            return Response({'reply': reply})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': '服务暂时不可用，请稍后再试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SystemConfigView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        from .services.config import get_system_config
        config = get_system_config()
        # Make avatar URL absolute if it's a media path
        if config['assistant_avatar'] and config['assistant_avatar'].startswith('/media/'):
            config['assistant_avatar'] = request.build_absolute_uri(config['assistant_avatar'])
        return Response(config)


@method_decorator(csrf_exempt, name='dispatch')
class ChatStreamView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        message = request.data.get('message', '')
        history = request.data.get('history', [])

        if not message:
            return Response(
                {'error': '请提供消息内容'},
                status=status.HTTP_400_BAD_REQUEST
            )

        def event_stream():
            try:
                for chunk in chat_with_assistant_stream(message, history):
                    data = json.dumps({'content': chunk}, ensure_ascii=False)
                    yield f"data: {data}\n\n"
                yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
            except Exception as e:
                import traceback
                traceback.print_exc()
                error_data = json.dumps({'error': str(e)}, ensure_ascii=False)
                yield f"data: {error_data}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class KnowledgeListView(APIView):
    def get(self, request):
        documents = knowledge_service.list_documents()
        return Response({'documents': documents})


class KnowledgeSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response(
                {'error': '请提供搜索关键词'},
                status=status.HTTP_400_BAD_REQUEST
            )
        results = knowledge_service.search(keyword)
        return Response({'results': results})


@method_decorator(csrf_exempt, name='dispatch')
class KnowledgeReloadView(APIView):
    def post(self, request):
        try:
            knowledge_service.load_documents()
            return Response({'message': '知识库已重新加载'})
        except Exception as e:
            return Response(
                {'error': '重新加载知识库失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )