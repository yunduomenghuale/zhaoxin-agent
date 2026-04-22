from django.urls import path
from .views import (
    AdminLoginView, AdminLogoutView, AdminCheckView,
    AdminUserListView, AdminUserDetailView,
    KnowledgeDocumentListView, KnowledgeDocumentDetailView,
    SystemPromptListView, SystemPromptDetailView, SystemPromptActivateView,
    KnowledgeImageListView, KnowledgeImageDetailView,
    SystemSettingsView,
    PromptTemplateListView, PromptTemplateDetailView
)

urlpatterns = [
    path('login', AdminLoginView.as_view()),
    path('logout', AdminLogoutView.as_view()),
    path('check', AdminCheckView.as_view()),
    path('settings', SystemSettingsView.as_view()),
    path('users', AdminUserListView.as_view()),
    path('users/<int:pk>', AdminUserDetailView.as_view()),
    path('knowledge', KnowledgeDocumentListView.as_view()),
    path('knowledge/<int:pk>', KnowledgeDocumentDetailView.as_view()),
    path('prompts', SystemPromptListView.as_view()),
    path('prompts/<int:pk>', SystemPromptDetailView.as_view()),
    path('prompts/<int:pk>/activate', SystemPromptActivateView.as_view()),
    path('images', KnowledgeImageListView.as_view()),
    path('images/<int:pk>', KnowledgeImageDetailView.as_view()),
    path('templates', PromptTemplateListView.as_view()),
    path('templates/<int:pk>', PromptTemplateDetailView.as_view()),
]