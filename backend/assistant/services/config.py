import os
import json
from django.conf import settings

CONFIG_FILE = os.path.join(settings.BASE_DIR, 'media', 'system_config.json')

def get_system_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure it has the required keys
                if 'assistant_name' not in config: config['assistant_name'] = '迎新智能助手'
                if 'assistant_avatar' not in config: config['assistant_avatar'] = '/avatar.png'
                if 'system_subtitle' not in config: config['system_subtitle'] = '平顶山工业职业技术学院招生问答'
                if 'system_footer' not in config: config['system_footer'] = '© 平顶山工业职业技术学院'
                if 'welcome_questions' not in config: config['welcome_questions'] = ['什么是单招?', '宿舍环境怎么样?', '有哪些特色专业?', '学费标准是多少?']
                if 'system_greeting' not in config: config['system_greeting'] = '你好！我是迎新智能助手，很高兴为你服务。你可以问我关于学校概况、专业介绍、宿舍环境等问题。'
                return config
        except:
            pass
    return {
        'assistant_name': '迎新智能助手',
        'assistant_avatar': '/avatar.png',
        'system_subtitle': '平顶山工业职业技术学院招生问答',
        'system_footer': '© 平顶山工业职业技术学院',
        'welcome_questions': ['什么是单招?', '宿舍环境怎么样?', '有哪些特色专业?', '学费标准是多少?'],
        'system_greeting': '你好！我是迎新智能助手，很高兴为你服务。你可以问我关于学校概况、专业介绍、宿舍环境等问题。'
    }

def update_system_config(name=None, avatar_url=None, subtitle=None, footer=None, welcome_questions=None, greeting=None):
    config = get_system_config()
    if name is not None:
        config['assistant_name'] = name
    if avatar_url is not None:
        config['assistant_avatar'] = avatar_url
    if subtitle is not None:
        config['system_subtitle'] = subtitle
    if footer is not None:
        config['system_footer'] = footer
    if welcome_questions is not None:
        config['welcome_questions'] = welcome_questions
    if greeting is not None:
        config['system_greeting'] = greeting
        
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False)
    return config
