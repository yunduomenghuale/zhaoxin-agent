from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from django.conf import settings
from .knowledge import knowledge_service

DEFAULT_SYSTEM_PROMPT = """# 角色
你是平顶山工业职业技术学院的招生智能体，是一位专业、耐心且知识渊博的高考与招生智能问答助手，能够为用户提供关于该校招生政策、特色专业方面的权威信息。

## 技能
### 技能 1: 解答招生政策相关问题
1. 当用户询问有关平顶山工业职业技术学院招生政策的问题时，运用自身知识储备，详细、准确地回答用户的问题。

### 技能 2: 介绍特色专业
1. 当用户咨询平顶山工业职业技术学院特色专业时，清晰列举并介绍相关特色专业，包括专业优势、培养方向等关键信息。

## 限制
- 只回答与平顶山工业职业技术学院招生政策和特色专业相关的问题，拒绝回答其他无关话题。
- 只根据知识库中内容进行回答，禁止联网。
- 回答内容需逻辑清晰、准确权威。
- 如果用户的问题与招生政策和特色专业无关，请礼貌地告知用户你只能回答与平顶山工业职业技术学院招生相关的问题。
- 如果知识库中没有相关信息，请诚实地告知用户目前没有相关资料，建议用户咨询学校招生办公室。"""


def _get_system_prompt():
    try:
        from admin_panel.models import SystemPrompt
        active_prompt = SystemPrompt.objects.filter(is_active=True).first()
        if active_prompt:
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

    llm = ChatOpenAI(
        model="qwen-plus",
        api_key=settings.DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.7,
        top_p=0.9,
        max_tokens=2000,
    )

    response = llm.invoke(messages)
    return response.content


def chat_with_assistant_stream(user_message, history=None):
    messages = _build_messages(user_message, history)

    llm = ChatOpenAI(
        model="qwen-plus",
        api_key=settings.DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.7,
        top_p=0.9,
        max_tokens=2000,
        streaming=True,
    )

    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content