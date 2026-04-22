import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admin_panel.models import KnowledgeImage

images = [
    {'title': '宿舍实景 1', 'file': 'knowledge/images/b7de0cbb1140906934b499706c36062b.jpg', 'tags': '宿舍, 宿舍照片, 环境'},
    {'title': '宿舍实景 2', 'file': 'knowledge/images/ea0bfa6e78980dc3eb1e98106ad0cd4d.jpg', 'tags': '宿舍, 宿舍照片, 环境'},
]

for img_data in images:
    if not KnowledgeImage.objects.filter(image=img_data['file']).exists():
        KnowledgeImage.objects.create(
            title=img_data['title'],
            image=img_data['file'],
            tags=img_data['tags']
        )
        print(f"已导入图片: {img_data['title']}")
    else:
        print(f"图片已存在: {img_data['title']}")
