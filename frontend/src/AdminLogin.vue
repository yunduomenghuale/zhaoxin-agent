<template>
  <div class="login-page">
    <div class="background-decor">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>
    
    <div class="login-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <img :src="assistantAvatar || '/avatar.png'" alt="logo" class="login-logo" @error="e => e.target.src='https://api.dicebear.com/7.x/bottts/svg?seed=Enrollee&backgroundColor=6366f1'" />
        </div>
        <h2>后台管理系统</h2>
        <p>{{ assistantName || '迎新智能助手' }}管理平台</p>
      </div>
      
      <div class="login-form">
        <div class="form-group">
          <label>用户名</label>
          <div class="input-wrapper">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <input v-model="username" type="text" placeholder="请输入用户名" @keyup.enter="handleLogin" />
          </div>
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <div class="input-wrapper">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            <input v-model="password" type="password" placeholder="请输入密码" @keyup.enter="handleLogin" />
          </div>
        </div>
        
        <Transition name="fade">
          <div v-if="errorMsg" class="error-msg">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            {{ errorMsg }}
          </div>
        </Transition>
        
        <button class="login-btn" @click="handleLogin" :disabled="loading">
          <span v-if="!loading">立即登录</span>
          <div v-else class="loader"></div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      username: '',
      password: '',
      errorMsg: '',
      loading: false,
      assistantName: '',
      assistantAvatar: '',
    }
  },
  async mounted() {
    this.loadSystemConfig()
    try {
      const res = await fetch('/api/admin/check')
      const data = await res.json()
      if (data.logged_in) {
        this.$router.push('/admin')
      }
    } catch (e) {}
  },
  methods: {
    async loadSystemConfig() {
      try {
        const res = await fetch('/api/config')
        const data = await res.json()
        if (res.ok) {
          this.assistantName = data.assistant_name
          this.assistantAvatar = data.assistant_avatar
        }
      } catch (e) {}
    },
    async handleLogin() {
      if (!this.username || !this.password) {
        this.errorMsg = '请输入用户名和密码'
        return
      }
      this.loading = true
      this.errorMsg = ''
      try {
        const res = await fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password }),
        })
        const data = await res.json()
        if (res.ok && data.user) {
          this.$router.push('/admin')
        } else {
          this.errorMsg = data.error || '登录信息有误，请重新输入'
        }
      } catch (e) {
        this.errorMsg = '无法连接到服务器，请检查网络'
      }
      this.loading = false
    },
  },
}
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  position: relative;
  overflow: hidden;
}

.background-decor {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.blob {
  position: absolute;
  filter: blur(80px);
  opacity: 0.4;
  border-radius: 50%;
  animation: blobFloat 20s infinite alternate;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: #6366f1;
  top: -100px;
  left: -100px;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: #8b5cf6;
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: #ec4899;
  top: 40%;
  right: 15%;
  animation-delay: -10s;
}

@keyframes blobFloat {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(40px, 40px) scale(1.1); }
}

.login-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 32px;
  padding: 56px;
  width: 460px;
  max-width: 90%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
  animation: cardShow 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes cardShow {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.login-header {
  text-align: center;
  margin-bottom: 48px;
}

.logo-wrapper {
  display: inline-block;
  padding: 4px;
  background: white;
  border-radius: 22px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.login-logo {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  display: block;
}

.login-header h2 {
  font-size: 32px;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.login-header p {
  font-size: 16px;
  color: #64748b;
  font-weight: 500;
}

.form-group {
  margin-bottom: 28px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 12px;
  margin-left: 4px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 18px;
  color: #94a3b8;
  transition: color 0.3s;
}

.input-wrapper input {
  width: 100%;
  padding: 16px 20px 16px 52px;
  background: rgba(248, 250, 252, 0.8);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  color: #1e293b;
  font-size: 16px;
  outline: none;
  transition: all 0.3s;
}

.input-wrapper input:focus {
  background: #ffffff;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.input-wrapper input:focus + .input-icon {
  color: #6366f1;
}

.error-msg {
  color: #e11d48;
  font-size: 14px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff1f2;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #ffe4e6;
}

.login-btn {
  width: 100%;
  padding: 18px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 20px 30px -10px rgba(79, 70, 229, 0.5);
  filter: brightness(1.1);
}

.login-btn:active {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loader {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>