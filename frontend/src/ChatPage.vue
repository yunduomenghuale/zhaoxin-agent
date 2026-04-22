<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <div :class="['sidebar', { 'mobile-open': isSidebarOpen }]">
      <div class="sidebar-header">
        <div class="logo-box">
          <img :src="assistantAvatar || '/avatar.png'" alt="Logo" class="logo-img" @error="e => e.target.src='https://api.dicebear.com/7.x/bottts/svg?seed=Enrollee&backgroundColor=6366f1'" />
          <span>{{ assistantName || '迎新助手' }}</span>
        </div>
        <button class="new-chat-btn" @click="createNewChat">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        </button>
      </div>
      
      <div class="history-label">历史记录</div>
      <div class="chat-list">
        <div v-for="chat in chatList" :key="chat.id" :class="['chat-item', { active: currentChatId === chat.id }]" @click="switchChat(chat.id)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chat-icon"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          <span class="chat-title">{{ chat.title }}</span>
            <button class="delete-chat-btn" @click.stop="deleteChat(chat.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg></button>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="footer-tag">{{ assistantFooter || '© 平顶山工业职业技术学院' }}</div>
      </div>
    </div>

    <!-- Main Chat -->
    <div class="chat-main">
      <div class="chat-header">
        <div class="mobile-menu-btn" @click="isSidebarOpen = !isSidebarOpen">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </div>
        <div class="header-info">
          <h1>{{ assistantName || '迎新智能助手' }}</h1>
          <p>{{ assistantSubtitle || '平顶山工业职业技术学院招生问答' }}</p>
        </div>
        <div class="header-actions">
          <button class="export-btn" @click="exportToWord" title="导出为Word">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <span>导出 Word</span>
          </button>
          <button class="export-btn" @click="exportToPDF" title="导出为PDF">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15h3a2 2 0 0 1 0 4H9v-4z"></path><path d="M17 15v4"></path></svg>
            <span>导出 PDF</span>
          </button>
        </div>
      </div>

      <div class="chat-body" ref="messagesContainer">
        <div class="messages-list">
          <div v-for="(msg, index) in currentMessages" :key="index" :class="['message-row', msg.role === 'user' ? 'msg-user' : 'msg-assistant']">
            <!-- Avatar removed per user request -->
            
              <div class="message-column">
                <div :class="['msg-bubble-sm', msg.role === 'user' ? 'user-bubble-card' : 'assistant-bubble', { 'typing-bubble': !msg.content && isTyping && isLastAssistant(msg) && !typingText }]">
                  <div class="message-content" v-if="msg.content || (isTyping && isLastAssistant(msg) && typingText)" v-html="renderContent(msg.content || typingText)"></div>
                  <div v-if="isTyping && isLastAssistant(msg) && !msg.content && !typingText" class="typing-dots">
                    <span></span><span></span><span></span>
                  </div>
                </div>

                <!-- Action Buttons (Moved outside, hidden for greeting) -->
                <div :class="['message-actions', { 'always-visible': isLastAssistant(msg) }]" v-if="msg.content && msg.role === 'assistant' && !isTyping && index !== 0">
                  <button class="feedback-btn action-icon" @click="copyMessage(msg.content)" title="复制内容">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                  </button>
                  <button class="feedback-btn action-icon" @click="regenerateMessage(msg)" title="重新生成" v-if="isLastAssistant(msg)">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>
                  </button>
                  <button :class="['feedback-btn action-icon', { 'active': msg.feedback === 'up' }]" @click="rateMessage(msg, 'up')" title="有帮助">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
                  </button>
                  <button :class="['feedback-btn action-icon', { 'active': msg.feedback === 'down' }]" @click="rateMessage(msg, 'down')" title="无帮助">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-2"></path></svg>
                  </button>
                </div>

              <div v-if="msg.role === 'assistant' && currentMessages.indexOf(msg) === 0" class="preset-card-list">
                <div v-for="q in presetQuestions" :key="q" class="preset-list-item" @click="sendPreset(q)">
                  <span>{{ q }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-container">
          <div class="chat-input-card">
            <textarea 
              v-model="inputText" 
              @keydown.enter.prevent="handleEnter"
              placeholder="请输入您的问题..." 
              class="chat-textarea" 
              :disabled="loading"
              rows="1"
            ></textarea>
            <button @click="sendMessage" class="send-btn-new" :disabled="loading || !inputText.trim()">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import html2pdf from 'html2pdf.js'
import { marked } from 'marked'

const DEFAULT_GREETING = '您好，我是迎新智能小助手，您可以向我提出招生相关问题哦。'
const PRESET_QUESTIONS = ['什么是单招？', '宿舍环境怎么样？', '有哪些特色专业？', '学费标准是多少？']

export default {
  name: 'ChatPage',
  data() {
    return {
      chatList: [],
      currentChatId: null,
      inputText: '',
      loading: false,
      presetQuestions: [],
      typingText: '',
      isTyping: false,
      isSidebarOpen: false,
      assistantName: '迎新智能助手',
      assistantAvatar: '/avatar.png',
      assistantSubtitle: '平顶山工业职业技术学院招生问答',
      assistantFooter: '© 平顶山工业职业技术学院',
    }
  },
  computed: {
    currentChat() { return this.chatList.find(c => c.id === this.currentChatId) },
    currentMessages() { return this.currentChat ? this.currentChat.messages : [] }
  },
  mounted() {
    try {
      this.loadFromStorage()
    } catch (e) {
      console.error('Initial load failed:', e)
      this.chatList = []
    }
    
    if (!Array.isArray(this.chatList) || this.chatList.length === 0) {
      this.createNewChat()
    }
    this.loadSystemConfig()
    this.scrollToBottom()
  },
  methods: {
    renderContent(content) {
      if (!content) return ''
      try {
        // Create a custom renderer that only overrides what we need
        const renderer = new marked.Renderer()
        renderer.image = ({ href, title, text }) => {
          return `<div class="message-image-wrapper">
            <img src="${href}" alt="${text || title || ''}" class="message-image" loading="lazy"
              style="max-width: 480px; width: 100%; height: auto; border-radius: 16px; margin: 12px 0; display: block; background: #f8fafc; cursor: zoom-in; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s;"
              onclick="window.open(this.src, '_blank')"
              onmouseover="this.style.transform='scale(1.01)'"
              onmouseout="this.style.transform='scale(1)'"
              onerror="this.style.display='none'" />
          </div>`
        }
        return marked.parse(content, {
          breaks: true,
          gfm: true,
          renderer: renderer
        })
      } catch (e) {
        console.error('Marked parsing error:', e)
        return content // Fallback to plain text
      }
    },
    createNewChat() {
      const greeting = this.assistantName ? `您好，我是${this.assistantName}，您可以向我提出招生相关问题哦。` : DEFAULT_GREETING
      const chat = {
        id: Date.now().toString(),
        title: '新对话',
        messages: [{ role: 'assistant', content: greeting, feedback: null }],
        history: [],
      }
      this.chatList.unshift(chat)
      this.currentChatId = chat.id
      this.isSidebarOpen = false
      this.saveToStorage()
      this.$nextTick(() => this.scrollToBottom())
    },
    async loadSystemConfig() {
      try {
        const res = await fetch('/api/config')
        const data = await res.json()
        if (res.ok) {
          this.assistantName = data.assistant_name
          this.assistantAvatar = data.assistant_avatar
          this.assistantSubtitle = data.system_subtitle
          this.assistantFooter = data.system_footer
          if (data.welcome_questions && data.welcome_questions.length > 0) {
            this.presetQuestions = data.welcome_questions
          } else {
            this.presetQuestions = ['什么是单招?', '宿舍环境怎么样?', '有哪些特色专业?', '学费标准是多少?']
          }
          
          const greeting = data.system_greeting || '你好！我是迎新智能助手，很高兴为你服务。你可以问我关于学校概况、专业介绍、宿舍环境等问题。'
          // Update first message if it's a default greeting
          if (this.currentMessages.length > 0 && this.currentMessages[0].role === 'assistant' && idx === 0) {
              // This part is tricky if they already started a chat. 
              // Usually we only want to update the VERY FIRST greeting if it hasn't been changed.
          }
          
          // Simplified: Just update the reference for future chats and the first message of current chat if it matches a default pattern
          if (this.currentMessages.length === 1 && this.currentMessages[0].role === 'assistant') {
             this.currentMessages[0].content = greeting
          }
          this.updatePageConfig()
        }
      } catch (e) {}
    },
    updatePageConfig() {
      if (this.assistantName) {
        document.title = `${this.assistantName} - 平顶山工业职业技术学院招生问答`
      }
      if (this.assistantAvatar) {
        let link = document.querySelector("link[rel~='icon']")
        if (!link) {
          link = document.createElement('link')
          link.rel = 'icon'
          document.head.appendChild(link)
        }
        link.href = this.assistantAvatar
      }
    },
    switchChat(id) {
      this.currentChatId = id
      this.isSidebarOpen = false
      this.$nextTick(() => this.scrollToBottom())
    },
    deleteChat(id) {
      this.chatList = this.chatList.filter(c => c.id !== id)
      if (this.currentChatId === id) {
        if (this.chatList.length > 0) this.currentChatId = this.chatList[0].id
        else this.createNewChat()
      }
      this.saveToStorage()
    },
    async sendMessage() {
      if (this.loading) return
      const text = this.inputText.trim()
      if (!text) return
      
      let chat = this.currentChat
      if (!chat) {
        // If no current chat, try to use the first one or create a new one
        if (this.chatList.length > 0) {
          this.currentChatId = this.chatList[0].id
          chat = this.currentChat
        } else {
          this.createNewChat()
          chat = this.currentChat
        }
      }
      
      if (!chat) {
        console.error('Could not identify active chat')
        return
      }

      this.loading = true
      
      // Update chat title if it's still the default
      if (chat.title === '新对话') {
        chat.title = text.length > 12 ? text.slice(0, 12) + '...' : text
      }
      
      if (!Array.isArray(chat.messages)) chat.messages = []
      chat.messages.push({ role: 'user', content: text })
      this.inputText = ''
      this.isTyping = true
      this.typingText = ''
      
      const assistantMsg = { role: 'assistant', content: '', feedback: null }
      chat.messages.push(assistantMsg)
      this.scrollToBottom()

      const historyBeforeSend = Array.isArray(chat.history) ? [...chat.history] : []
      
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, history: historyBeforeSend }),
        })
        const data = await res.json()
        const fullReply = data.reply || data.error || '抱歉，服务暂时不可用。'
        
        if (!Array.isArray(chat.history)) chat.history = []
        chat.history.push({ role: 'user', content: text })
        chat.history.push({ role: 'assistant', content: fullReply })
        this.saveToStorage()
        
        await this.typeWriter(fullReply)
        assistantMsg.content = fullReply
      } catch (e) { 
        assistantMsg.content = '网络连接失败，请稍后再试。'
        if (!Array.isArray(chat.history)) chat.history = []
        chat.history.push({ role: 'user', content: text })
        chat.history.push({ role: 'assistant', content: assistantMsg.content })
        this.saveToStorage()
      }
      this.loading = false; this.isTyping = false; this.saveToStorage(); this.scrollToBottom()
    },
    async typeWriter(text) {
      for (let i = 0; i <= text.length; i++) {
        this.typingText = text.slice(0, i)
        this.scrollToBottom()
        await new Promise(r => setTimeout(r, 20))
      }
    },
    async convertImagesToBase64(htmlContent) {
      const imgRegex = /<img\s+[^>]*src=["']([^"']+)["'][^>]*>/gi
      let result = htmlContent
      const matches = [...htmlContent.matchAll(imgRegex)]
      for (const match of matches) {
        const [originalTag, src] = match
        if (src.startsWith('data:')) continue
        try {
          const res = await fetch(src)
          const blob = await res.blob()
          const base64 = await new Promise(resolve => {
            const reader = new FileReader()
            reader.onloadend = () => resolve(reader.result)
            reader.readAsDataURL(blob)
          })
          result = result.replace(src, base64)
        } catch (e) { console.warn('Image convert failed:', src) }
      }
      return result
    },
    async exportToWord() {
      if (this.currentMessages.length === 0) return
      let content = `
        <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
        <head><meta charset='utf-8'>
        <style>
          table { border-collapse: collapse; width: 100%; margin: 10px 0; }
          th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 12px; }
          th { background: #f2f2f2; font-weight: bold; }
          img { max-width: 300px; border-radius: 8px; margin: 10px 0; display: block; }
        </style>
        </head>
        <body style="font-family: 'Microsoft YaHei', sans-serif; padding: 20px;">
          <h2 style="text-align: center; color: #1e293b;">招生问答记录</h2><hr/>
      `;
      for (const msg of this.currentMessages) {
        const isUser = msg.role === 'user'
        let msgHtml = this.renderContent(msg.content || '')
        msgHtml = await this.convertImagesToBase64(msgHtml)
        content += `
          <div style="margin-bottom: 20px;">
            <strong style="color: ${isUser ? '#3b82f6' : '#1e293b'}; font-size: 14px;">${isUser ? '考生' : '迎新助手'}：</strong>
            <div style="margin-top: 5px; font-size: 14px; line-height: 1.6; color: #334155;">${msgHtml}</div>
          </div>
        `
      }
      content += '</body></html>'
      const blob = new Blob(['\ufeff', content], { type: 'application/msword;charset=utf-8' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `聊天记录_${Date.now()}.doc`
      link.click()
    },
    async exportToPDF() {
      if (this.currentMessages.length === 0) return
      const tempDiv = document.createElement('div')
      tempDiv.style.padding = '30px'
      tempDiv.style.background = '#fff'
      let html = `<h2 style="text-align: center; color: #1e293b; margin-bottom: 25px;">招生问答记录</h2><hr style="margin-bottom: 25px; border: 0; border-top: 1px solid #eee;"/>
        <style>
          table { width: 100%; border-collapse: collapse; margin: 15px 0; }
          th, td { border: 1px solid #e2e8f0; padding: 10px 14px; text-align: left; font-size: 12px; }
          th { background: #f8fafc; font-weight: bold; }
          .message-image { max-width: 320px; border-radius: 10px; margin-top: 10px; border: 1px solid #eee; }
        </style>
      `
      for (const msg of this.currentMessages) {
        const isUser = msg.role === 'user'
        let msgHtml = this.renderContent(msg.content || '')
        msgHtml = await this.convertImagesToBase64(msgHtml)
        html += `
          <div style="margin-bottom: 20px; padding: 15px; border-radius: 10px; background: ${isUser ? '#f8fafc' : '#fff'}; border: 1px solid #eee; page-break-inside: avoid;">
            <strong style="color: ${isUser ? '#3b82f6' : '#1e293b'}; font-size: 14px;">${isUser ? '考生' : '迎新助手'}：</strong>
            <div style="margin-top: 8px; font-size: 13px; line-height: 1.6; color: #334155;">${msgHtml}</div>
          </div>
        `
      }
      tempDiv.innerHTML = html
      html2pdf().set({
        margin: 10,
        filename: `聊天记录_${Date.now()}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, letterRendering: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      }).from(tempDiv).save()
    },
    sendPreset(q) { this.inputText = q; this.sendMessage() },
    scrollToBottom() {
      this.$nextTick(() => {
        const c = this.$refs.messagesContainer
        if (c) c.scrollTop = c.scrollHeight
      })
    },
    saveToStorage() {
      localStorage.setItem('chatList', JSON.stringify(this.chatList))
      localStorage.setItem('currentChatId', this.currentChatId)
    },
    loadFromStorage() {
      try {
        const saved = localStorage.getItem('chatList')
        if (saved) {
          const parsed = JSON.parse(saved)
          if (Array.isArray(parsed)) {
            this.chatList = parsed.map(chat => ({
              ...chat,
              messages: Array.isArray(chat.messages) ? chat.messages.filter(m => m && (m.content || m.role === 'user')) : [],
              history: Array.isArray(chat.history) ? chat.history : []
            }))
          } else {
            this.chatList = []
          }
        }
        
        const savedId = localStorage.getItem('currentChatId')
        const exists = Array.isArray(this.chatList) && this.chatList.some(c => c.id === savedId)
        if (exists) {
          this.currentChatId = savedId
        } else {
          this.currentChatId = (Array.isArray(this.chatList) && this.chatList.length > 0) ? this.chatList[0].id : null
        }
      } catch (e) {
        console.error('Failed to load chats:', e)
        this.chatList = []
        this.currentChatId = null
      }
    },
    isLastAssistant(msg) {
      const msgs = this.currentMessages
      return msgs[msgs.length - 1] === msg
    },
    async copyMessage(text) { await navigator.clipboard.writeText(text) },
    async regenerateMessage(msg) {
      const chat = this.currentChat
      if (!chat) return
      const idx = chat.messages.indexOf(msg)
      if (idx <= 0) return
      
      // Find the user message that triggered this assistant response
      let userIdx = -1
      for (let i = idx - 1; i >= 0; i--) {
        if (chat.messages[i].role === 'user') {
          userIdx = i
          break
        }
      }
      
      if (userIdx === -1) return
      
      const lastText = chat.messages[userIdx].content
      
      // Remove the old user message and assistant message from the list
      // This prevents duplication since sendMessage will re-add the user message
      chat.messages.splice(userIdx, chat.messages.length - userIdx)
      
      // Also remove from chat.history if it matches the last pair
      if (chat.history.length >= 2) {
        chat.history.splice(-2, 2)
      }
      
      this.inputText = lastText
      this.sendMessage()
    },
    rateMessage(msg, type) {
      msg.feedback = msg.feedback === type ? null : type
      this.saveToStorage()
    },
    handleEnter(e) {
      if (e.shiftKey) return
      this.sendMessage()
    }
  }
}
</script>

<style>
:root {
  --primary: #6366f1;
  --primary-light: #818cf8;
  --primary-dark: #4f46e5;
  --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  --bg: #f0f2f5;
  --sidebar-bg: #1e293b;
  --sidebar-width: 280px;
  --border: #e2e8f0;
  --text-main: #1e293b;
  --text-muted: #64748b;
  --radius-lg: 24px;
  --radius-md: 16px;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.04);
  --shadow-md: 0 10px 25px rgba(0,0,0,0.08);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

<style scoped>
.app-layout {
  width: 100%;
  height: 100vh;
  display: flex;
  overflow: hidden;
  background: #f8fafc;
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--sidebar-bg);
  backdrop-filter: blur(20px);
  color: #f1f5f9;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  transition: var(--transition);
  z-index: 100;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fcfdfe;
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--sidebar-bg);
  backdrop-filter: blur(20px);
  color: #f1f5f9;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  transition: var(--transition);
  z-index: 100;
}

.sidebar-header {
  padding: 32px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-box {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.logo-img {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.new-chat-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.new-chat-btn:hover {
  background: var(--primary);
  transform: scale(1.05);
}

.history-label {
  padding: 0 24px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: #94a3b8;
  margin-bottom: 4px;
  position: relative;
}

.chat-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f1f5f9;
}

.chat-item.active {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
}

.chat-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-chat-btn {
  opacity: 0;
  background: transparent;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 4px;
  transition: opacity 0.2s;
}

.chat-item:hover .delete-chat-btn {
  opacity: 0.6;
}

.delete-chat-btn:hover {
  opacity: 1 !important;
}

.sidebar-footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-tag {
  font-size: 11px;
  color: #475569;
  text-align: center;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fcfdfe;
}

.chat-header {
  height: 80px;
  padding: 0 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.markdown-body {
  font-size: 15px;
  line-height: 1.8;
  color: #1e293b;
}

.header-info h1 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.header-info p {
  font-size: 12px;
  color: #64748b;
  margin: 4px 0 0 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid var(--border);
  color: #475569;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #f8fafc;
  border-color: var(--primary-light);
  color: var(--primary);
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  scrollbar-gutter: stable;
}

.messages-list {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding-bottom: 120px;
}

.message-row {
  display: flex;
  gap: 16px;
  width: 100%;
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.msg-user {
  flex-direction: row-reverse;
}

.message-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.message-column {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.msg-user .message-column { align-items: flex-end; }
.msg-assistant .message-column { align-items: flex-start; }

.msg-bubble-sm {
  max-width: 100%;
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 2.2;
  position: relative;
  word-break: break-word;
}

.user-bubble-card {
  background: var(--primary-gradient);
  color: #fff;
  border-radius: 24px;
}

.assistant-bubble {
  color: #1e293b;
  padding: 8px 0;
  position: relative;
}

.typing-bubble {
  padding: 6px 12px !important;
  display: flex !important;
  align-items: center;
  justify-content: center;
  min-width: 50px;
  min-height: 32px;
}

.message-content {
  width: 100%;
}
.message-content p {
  margin-bottom: 12px;
}
.message-content p:last-child {
  margin-bottom: 0;
}
.message-content :where(table, pre) {
  overflow-x: auto;
  max-width: 100%;
}

.message-actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
  justify-content: flex-start;
  opacity: 0;
  transition: opacity 0.2s;
}

.message-row:hover .message-actions,
.message-actions.always-visible {
  opacity: 1;
}

.action-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  border: 1px solid #eef2f6;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

.action-icon:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: #fdfdff;
  transform: translateY(-1px);
}

.action-icon.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.preset-card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}

.preset-list-item {
  padding: 10px 20px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 14px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.preset-list-item:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.12);
  background: #fdfdff;
}

.chat-input-container {
  position: fixed;
  bottom: 0;
  right: 0;
  width: calc(100% - var(--sidebar-width));
  padding: 20px 40px 40px;
  background: linear-gradient(to top, #fcfdfe 80%, transparent);
  z-index: 50;
}

.chat-input-card {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  background: #fff;
  border-radius: 28px;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04), 0 2px 10px rgba(99, 102, 241, 0.03);
  padding: 10px 16px 10px 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  gap: 12px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -100%;
    height: 100%;
    box-shadow: 20px 0 50px rgba(0,0,0,0.1);
  }
  .sidebar.mobile-open {
    left: 0;
  }
  .chat-input-container {
    width: 100%;
    padding: 10px 15px 25px;
  }
  .chat-header {
    padding: 0 20px;
  }
  .mobile-menu-btn {
    display: flex !important;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    margin-right: 10px;
    color: var(--text-main);
    cursor: pointer;
  }
  .chat-body {
    padding: 20px 15px;
  }
  .message-column {
    max-width: 90%;
  }
  .header-actions span {
    display: none;
  }
}

@media (min-width: 769px) {
  .mobile-menu-btn {
    display: none !important;
  }
}

.chat-input-card:focus-within {
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 15px 50px rgba(99, 102, 241, 0.08), 0 4px 15px rgba(99, 102, 241, 0.05);
  transform: translateY(-2px);
}

.chat-textarea {
  width: 100%;
  border: none;
  background: transparent;
  padding: 8px 4px;
  font-size: 16px;
  line-height: 1.6;
  outline: none;
  resize: none;
  color: #1e293b;
  min-height: 44px;
  max-height: 200px;
  font-family: inherit;
}

.send-btn-new {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #0066ff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.2);
  margin-bottom: 2px;
}

.send-btn-new:hover:not(:disabled) {
  transform: scale(1.08);
  background: #005ce6;
  box-shadow: 0 6px 16px rgba(0, 102, 255, 0.3);
}

.send-btn-new:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

.typing-dots {
  display: flex !important;
  gap: 6px;
  padding: 4px 8px;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  min-height: 24px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
  animation: jump 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes jump {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
}

.message-image-wrapper {
  margin: 8px 8px 4px 0;
  display: inline-block;
  vertical-align: top;
  max-width: 100%;
}

.message-image {
  max-width: 320px;
  width: auto;
  height: auto;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  display: block;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  font-size: 14px;
}

th, td {
  padding: 12px 16px;
  border: 1px solid var(--border);
  text-align: left;
  line-height: 1.5;
}

th {
  background: #f8fafc;
  font-weight: 700;
  color: var(--text-main);
  border-bottom: 2px solid var(--border);
}

tr:nth-child(even) {
  background: #fcfdfe;
}

tr:hover {
  background: #f1f5f9;
}
</style>
