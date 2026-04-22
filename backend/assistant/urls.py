from django.urls import path
from .views import ChatView, ChatStreamView, KnowledgeListView, KnowledgeSearchView, KnowledgeReloadView, HealthView, SystemConfigView

urlpatterns = [
    path('config', SystemConfigView.as_view()),
    path('chat', ChatView.as_view()),
    path('chat/stream', ChatStreamView.as_view()),
    path('knowledge/list', KnowledgeListView.as_view()),
    path('knowledge/search', KnowledgeSearchView.as_view()),
    path('knowledge/reload', KnowledgeReloadView.as_view()),
    path('health', HealthView.as_view()),
]