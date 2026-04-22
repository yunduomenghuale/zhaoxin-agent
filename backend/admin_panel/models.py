from django.db import models
from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    role = models.CharField(max_length=20, default='admin', choices=[('admin', '管理员'), ('editor', '编辑者')])

    class Meta:
        db_table = 'admin_user'
        verbose_name = '后台用户'


class KnowledgeDocument(models.Model):
    title = models.CharField(max_length=200, verbose_name='文档标题')
    content = models.TextField(verbose_name='文档内容')
    source_file = models.CharField(max_length=200, blank=True, default='', verbose_name='来源文件名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'knowledge_document'
        verbose_name = '知识库文档'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class SystemPrompt(models.Model):
    name = models.CharField(max_length=100, verbose_name='提示词名称')
    content = models.TextField(verbose_name='提示词内容')
    is_active = models.BooleanField(default=False, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_prompt'
        verbose_name = '系统提示词'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class KnowledgeImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='图片标题')
    image = models.ImageField(upload_to='knowledge/images/', verbose_name='图片文件')
    tags = models.CharField(max_length=200, blank=True, help_text='用逗号分隔，如：宿舍, 环境', verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'knowledge_image'
        verbose_name = '知识库图片'
        ordering = ['-created_at']

    def __str__(self):
        return self.title