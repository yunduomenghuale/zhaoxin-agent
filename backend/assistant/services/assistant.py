from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from django.conf import settings
from .knowledge import knowledge_service
from .config import get_system_config

MASTER_PROMPT_TEMPLATE = """# 角色设定
{role}

## 技能描述
{skills}

## 核心行为准则 (系统约束)
1. **知识驱动**：必须且仅能根据提供的【相关资料】回答用户问题。如果资料中包含图片，请按需引用。
2. **诚实原则**：如果资料中无法找到答案，请明确告知用户，并根据你的角色背景给予合理的后续建议。
3. **对话边界**：严禁回答与当前角色职能及知识库内容无关的话题。
4. **输出规范**：使用清晰的 Markdown 格式，保持专业、亲和且有帮助的语气。
"""

DEFAULT_SYSTEM_PROMPT = MASTER_PROMPT_TEMPLATE.format(
    role="你是平顶山工业职业技术学院的招生智能体，是一位专业、耐心且知识渊博的高考与招生智能问答助手。",
    skills="1. 解答招生政策相关问题：详细、准确地回答招生政策。\n2. 介绍特色专业：清晰列举并介绍相关特色专业，包括专业优势、培养方向等。"
)


def _get_system_prompt():
    try:
        from admin_panel.models import SystemPrompt
        active_prompt = SystemPrompt.objects.filter(is_active=True).first()
        if active_prompt:
            if active_prompt.role and active_prompt.skills:
                return MASTER_PROMPT_TEMPLATE.format(
                    role=active_prompt.role,
                    skills=active_prompt.skills
                )
            return active_prompt.content
    except Exception:
        pass
    return DEFAULT_SYSTEM_PROMPT


def _build_messages(user_message, history=None):
    if history is None:
        history = []

    system_prompt = _get_system_prompt()

    relevant_knowledge = knowledge_service.search(user_message)
    knowledge_context = ""
    if relevant_knowledge:
        knowledge_context = "\n\n## 以下是从知识库中检索到的相关资料，请优先参考这些内容回答用户问题：\n"
        for idx, item in enumerate(relevant_knowledge, 1):
            knowledge_context += f"\n--- 资料片段 {idx} ---\n来源: {item['source']}\n内容: {item['content']}\n"
    else:
        knowledge_context = "\n\n注意：知识库中没有检索到与用户问题直接相关的资料，请根据你已有的关于平顶山工业职业技术学院的知识进行回答，并提醒用户建议咨询学校招生办公室获取更准确信息。"

    relevant_images = knowledge_service.search_images(user_message)
    image_context = ""
    if relevant_images:
        image_context = "\n\n## 以下是相关的图片资料，如果用户询问关于环境、宿舍、设施等视觉信息，请在回复中包含这些图片链接（使用标准Markdown格式：![描述](链接)）。你可以直接使用提供的图片链接。如果有多张相关图片，请连续放置它们（不要换行），以便它们能并排显示：\n"
        for img in relevant_images:
            image_context += f"- 图片标题: {img['title']}, 链接: {img['url']}\n"

    full_system_prompt = system_prompt + knowledge_context + image_context

    messages = [SystemMessage(content=full_system_prompt)]

    for msg in history:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'user':
            messages.append(HumanMessage(content=content))
        elif role == 'assistant':
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_message))
    return messages


def chat_with_assistant(user_message, history=None):
    messages = _build_messages(user_message, history)
    config = get_system_config()
    provider = config.get('llm_provider', 'aliyun')
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    if provider == 'deepseek':
        base_url = "https://api.deepseek.com"
    elif config.get('llm_base_url'):
        base_url = config.get('llm_base_url')

    llm = ChatOpenAI(
        model=config.get('llm_model', 'qwen-plus'),
        api_key=config.get('llm_api_key') or settings.DASHSCOPE_API_KEY,
        base_url=base_url,
        temperature=0.7,
        top_p=0.9,
        max_tokens=2000,
    )

    response = llm.invoke(messages)
    return response.content


def chat_with_assistant_stream(user_message, history=None):
    messages = _build_messages(user_message, history)
    config = get_system_config()
    provider = config.get('llm_provider', 'aliyun')
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    if provider == 'deepseek':
        base_url = "https://api.deepseek.com"
    elif config.get('llm_base_url'):
        base_url = config.get('llm_base_url')

    llm = ChatOpenAI(
        model=config.get('llm_model', 'qwen-plus'),
        api_key=config.get('llm_api_key') or settings.DASHSCOPE_API_KEY,
        base_url=base_url,
        temperature=0.7,
        top_p=0.9,
        max_tokens=2000,
        streaming=True,
    )

    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content