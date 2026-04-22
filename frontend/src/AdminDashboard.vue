<template>
  <div v-if="currentUser" class="admin-layout">
    <div class="admin-sidebar">
      <div class="admin-sidebar-header">
        <img :src="systemSettings.assistant_avatar || '/avatar.png'" alt="logo" class="admin-logo" @error="e => e.target.src='https://api.dicebear.com/7.x/bottts/svg?seed=Enrollee&backgroundColor=6366f1'" />
        <span>后台管理</span>
      </div>
      <div class="admin-nav">
        <div :class="['nav-item', activeTab === 'users' ? 'active' : '']" @click="activeTab = 'users'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          用户管理
        </div>
        <div :class="['nav-item', activeTab === 'knowledge' ? 'active' : '']" @click="activeTab = 'knowledge'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
          知识库管理
        </div>
        <div :class="['nav-item', activeTab === 'images' ? 'active' : '']" @click="activeTab = 'images'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          媒体库管理
        </div>
        <div :class="['nav-item', activeTab === 'prompts' ? 'active' : '']" @click="activeTab = 'prompts'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          提示词管理
        </div>
        <div :class="['nav-item', activeTab === 'questions' ? 'active' : '']" @click="activeTab = 'questions'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          对话管理
        </div>
        <div :class="['nav-item', activeTab === 'brand' ? 'active' : '']" @click="activeTab = 'brand'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>
          品牌化配置
        </div>
        <div :class="['nav-item', activeTab === 'settings' ? 'active' : '']" @click="activeTab = 'settings'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          系统设置
        </div>
        <div class="sidebar-divider"></div>
        <div :class="['nav-item', activeTab === 'chat' ? 'active' : '']" @click="activeTab = 'chat'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          对话测试
        </div>
      </div>
      <div class="admin-sidebar-footer">
        <div class="nav-item" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          退出登录
        </div>
      </div>
    </div>

    <div class="admin-main">
      <div class="admin-header">
        <h2>{{ tabTitle }}</h2>
        <span class="user-info">{{ currentUser?.username }}</span>
      </div>

      <div class="admin-content">
        <div v-if="activeTab === 'users'" class="tab-content">
          <div class="action-bar">
            <button class="primary-btn" @click="showUserForm = true; editingUser = null; userForm = { username: '', password: '', role: 'editor' }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              新增用户
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>ID</th><th>用户名</th><th>角色</th><th>状态</th><th>创建时间</th><th>操作</th></tr>
              </thead>
              <tbody>
                <tr v-for="u in users" :key="u.id">
                  <td>{{ u.id }}</td>
                  <td>{{ u.username }}</td>
                  <td>{{ u.role === 'admin' ? '管理员' : '编辑者' }}</td>
                  <td>{{ u.is_active ? '启用' : '禁用' }}</td>
                  <td>{{ u.date_joined }}</td>
                  <td class="action-cell">
                    <button class="edit-btn" @click="editingUser = u; showUserForm = true; userForm = { username: u.username, password: '', role: u.role, is_active: u.is_active }">编辑</button>
                    <button class="delete-btn" @click="deleteUser(u.id)">删除</button>
                  </td>
                </tr>
                <tr v-if="users.length === 0"><td colspan="6" class="empty-row">暂无数据</td></tr>
              </tbody>
            </table>
          </div>

          <div v-if="showUserForm" class="modal-overlay" @click.self="showUserForm = false">
            <div class="modal-card">
              <h3>{{ editingUser ? '编辑用户' : '新增用户' }}</h3>
              <div class="form-group">
                <label>用户名</label>
                <input v-model="userForm.username" type="text" placeholder="请输入用户名" />
              </div>
              <div class="form-group">
                <label>密码{{ editingUser ? '（留空则不修改）' : '' }}</label>
                <input v-model="userForm.password" type="password" placeholder="请输入密码" />
              </div>
              <div class="form-group">
                <label>角色</label>
                <select v-model="userForm.role">
                  <option value="admin">管理员</option>
                  <option value="editor">编辑者</option>
                </select>
              </div>
              <div v-if="editingUser" class="form-group">
                <label>状态</label>
                <select v-model="userForm.is_active">
                  <option :value="true">启用</option>
                  <option :value="false">禁用</option>
                </select>
              </div>
              <div v-if="formError" class="form-error">{{ formError }}</div>
              <div class="modal-actions">
                <button class="cancel-btn" @click="showUserForm = false">取消</button>
                <button class="primary-btn" @click="saveUser">保存</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'knowledge'" class="tab-content">
          <div class="action-bar">
            <button class="primary-btn" @click="showKnowledgeForm = true; editingDoc = null; knowledgeForm = { title: '', content: '', source_file: '', is_active: true }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              新增文档
            </button>
            <input v-model="knowledgeKeyword" placeholder="搜索文档..." class="search-input" @keyup.enter="loadKnowledge" />
            <button class="secondary-btn" @click="loadKnowledge">搜索</button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>ID</th><th>标题</th><th>来源文件</th><th>状态</th><th>创建时间</th><th>更新时间</th><th>操作</th></tr>
              </thead>
              <tbody>
                <tr v-for="d in knowledgeDocs" :key="d.id">
                  <td>{{ d.id }}</td>
                  <td>{{ d.title }}</td>
                  <td>{{ d.source_file || '-' }}</td>
                  <td>{{ d.is_active ? '启用' : '禁用' }}</td>
                  <td>{{ d.created_at }}</td>
                  <td>{{ d.updated_at }}</td>
                  <td class="action-cell">
                    <button class="edit-btn" @click="editingDoc = d; showKnowledgeForm = true; knowledgeForm = { title: d.title, content: d.content, source_file: d.source_file, is_active: d.is_active }">编辑</button>
                    <button class="delete-btn" @click="deleteKnowledge(d.id)">删除</button>
                  </td>
                </tr>
                <tr v-if="knowledgeDocs.length === 0"><td colspan="7" class="empty-row">暂无数据</td></tr>
              </tbody>
            </table>
          </div>

          <div v-if="showKnowledgeForm" class="modal-overlay" @click.self="showKnowledgeForm = false">
            <div class="modal-card modal-card-lg">
              <h3>{{ editingDoc ? '编辑文档' : '上传并新增文档' }}</h3>
              
              <div v-if="!editingDoc" class="form-group">
                <label>选择文件</label>
                <div class="file-upload-wrapper" @click="$refs.fileInput.click()">
                  <input type="file" ref="fileInput" @change="handleKnowledgeFileUpload" accept=".docx,.txt" class="hidden-file-input" />
                  <div class="upload-content">
                    <div class="upload-icon">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                      </svg>
                    </div>
                    <div class="upload-text">
                      <span v-if="!selectedFile">点击选择或拖拽文件到此处</span>
                      <span v-else class="selected-filename">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
                        {{ selectedFile.name }}
                      </span>
                    </div>
                    <div class="file-tip">支持 .docx, .txt 格式文档</div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>标题</label>
                <input v-model="knowledgeForm.title" type="text" :placeholder="editingDoc ? '请输入文档标题' : '可选，不填则使用文件名'" />
              </div>

              <div v-if="editingDoc" class="form-group">
                <label>内容</label>
                <textarea v-model="knowledgeForm.content" placeholder="请输入文档内容" @input="autoResize" class="auto-height-textarea" style="min-height: 200px;"></textarea>
              </div>

              <div class="form-group">
                <label>状态</label>
                <select v-model="knowledgeForm.is_active">
                  <option :value="true">启用</option>
                  <option :value="false">禁用</option>
                </select>
              </div>

              <div v-if="formError" class="form-error">{{ formError }}</div>
              <div class="modal-actions">
                <button class="cancel-btn" @click="showKnowledgeForm = false">取消</button>
                <button class="primary-btn" @click="saveKnowledge" :disabled="loading">
                  <span v-if="loading">处理中...</span>
                  <span v-else>{{ editingDoc ? '保存修改' : '立即上传' }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'images'" class="tab-content">
          <div class="action-bar">
            <button class="primary-btn" @click="showImageForm = true; imageForm = { title: '', tags: '' }; selectedImageFile = null">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              上传图片
            </button>
          </div>
          <div class="image-grid">
            <div v-for="img in images" :key="img.id" class="image-card">
              <div class="image-preview">
                <img :src="img.url" :alt="img.title" />
              </div>
              <div class="image-info">
                <div class="image-title">{{ img.title }}</div>
                <div class="image-tags">
                  <span v-for="tag in (img.tags ? img.tags.split(',') : [])" :key="tag" class="tag">{{ tag.trim() }}</span>
                </div>
                <div class="image-actions">
                  <button class="delete-btn" @click="deleteImage(img.id)">删除</button>
                </div>
              </div>
            </div>
            <div v-if="images.length === 0" class="empty-state">
              暂无媒体文件，点击“上传图片”开始。
            </div>
          </div>

          <div v-if="showImageForm" class="modal-overlay" @click.self="showImageForm = false">
            <div class="modal-card">
              <h3>上传图片</h3>
              <div class="form-group">
                <label>选择图片</label>
                <div class="file-upload-wrapper" @click="$refs.imgFileInput.click()">
                  <input type="file" ref="imgFileInput" @change="handleImageFileUpload" accept="image/*" class="hidden-file-input" />
                  <div class="upload-content">
                    <div class="upload-icon">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                    </div>
                    <div class="upload-text">
                      <span v-if="!selectedImageFile">点击选择图片</span>
                      <span v-else class="selected-filename">{{ selectedImageFile.name }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>标题</label>
                <input v-model="imageForm.title" type="text" placeholder="图片标题，不填则使用文件名" />
              </div>
              <div class="form-group">
                <label>标签（用逗号分隔，AI会根据标签搜索图片）</label>
                <input v-model="imageForm.tags" type="text" placeholder="例如：宿舍, 环境, 设施" />
              </div>
              <div v-if="formError" class="form-error">{{ formError }}</div>
              <div class="modal-actions">
                <button class="cancel-btn" @click="showImageForm = false">取消</button>
                <button class="primary-btn" @click="saveImage" :disabled="loading">
                  <span v-if="loading">处理中...</span>
                  <span v-else>开始上传</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'prompts'" class="tab-content">
          <div class="action-bar">
            <button class="primary-btn" @click="showPromptForm = true; editingPrompt = null; promptForm = { name: '', content: '', is_active: false }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              新增提示词
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>ID</th><th>名称</th><th>状态</th><th>创建时间</th><th>更新时间</th><th>操作</th></tr>
              </thead>
              <tbody>
                <tr v-for="p in prompts" :key="p.id">
                  <td>{{ p.id }}</td>
                  <td>{{ p.name }}</td>
                  <td>
                    <span :class="['status-tag', p.is_active ? 'active-tag' : 'inactive-tag']">{{ p.is_active ? '已激活' : '未激活' }}</span>
                  </td>
                  <td>{{ p.created_at }}</td>
                  <td>{{ p.updated_at }}</td>
                  <td class="action-cell">
                    <button v-if="!p.is_active" class="activate-btn" @click="activatePrompt(p.id)">激活</button>
                    <button class="edit-btn" @click="editingPrompt = p; showPromptForm = true; promptForm = { name: p.name, content: p.content, is_active: p.is_active }; triggerAllAutoResize()">编辑</button>
                    <button class="delete-btn" @click="deletePrompt(p.id)">删除</button>
                  </td>
                </tr>
                <tr v-if="prompts.length === 0"><td colspan="6" class="empty-row">暂无数据</td></tr>
              </tbody>
            </table>
          </div>

          <div v-if="showPromptForm" class="modal-overlay" @click.self="showPromptForm = false">
            <div class="modal-card modal-card-lg">
              <h3>{{ editingPrompt ? '编辑提示词' : '新增提示词' }}</h3>
              <div class="form-group">
                <label>名称</label>
                <input v-model="promptForm.name" type="text" placeholder="请输入提示词名称" />
              </div>
              <div class="form-group">
                <label>内容</label>
                <textarea v-model="promptForm.content" placeholder="请输入提示词内容" @input="autoResize" class="auto-height-textarea" style="min-height: 300px;"></textarea>
              </div>
              <div class="form-group">
                <label>是否激活（激活后将作为当前使用的系统提示词）</label>
                <select v-model="promptForm.is_active">
                  <option :value="true">激活</option>
                  <option :value="false">不激活</option>
                </select>
              </div>
              <div v-if="formError" class="form-error">{{ formError }}</div>
              <div class="modal-actions">
                <button class="cancel-btn" @click="showPromptForm = false">取消</button>
                <button class="primary-btn" @click="savePrompt">保存</button>
              </div>
            </div>
          </div>
        </div>



        <div v-if="activeTab === 'questions'" class="tab-content">
          <div class="settings-container-beauty">
            <div class="settings-main-card">
              <div class="settings-header">
                <div class="settings-header-icon">
                  <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                </div>
                <div>
                  <h3>对话管理</h3>
                  <p>配置机器人欢迎语后的引导问题，帮助用户快速开始对话</p>
                </div>
              </div>

              <div class="settings-grid" style="grid-template-columns: 1fr;">
                <div class="settings-form-section" style="max-width: 800px; margin: 0 auto; width: 100%;">
                  <div class="beauty-form-group">
                    <label style="font-size: 16px;"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg> 招呼语（机器人开场白）</label>
                    <div class="input-wrapper" style="margin-top: 12px;">
                      <textarea v-model="systemSettings.system_greeting" placeholder="输入助手发送的第一句话..." @input="autoResize" class="auto-height-textarea" style="width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; font-family: inherit;"></textarea>
                    </div>
                  </div>

                  <div class="beauty-form-group" style="margin-top: 24px;">
                    <label style="font-size: 16px;"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg> 预设问题（欢迎语快捷提问）</label>
                    <div class="welcome-questions-list" style="margin-top: 20px;">
                      <div v-for="(q, index) in systemSettings.welcome_questions" :key="index" class="question-input-card-item">
                        <div class="q-item-header">
                          <span class="q-item-index">引导项 #{{ index + 1 }}</span>
                          <button class="remove-q-btn-beauty" @click="systemSettings.welcome_questions.splice(index, 1)" title="删除此项">
                            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                          </button>
                        </div>
                        <div class="q-item-body">
                          <div class="input-wrapper">
                            <input v-model="systemSettings.welcome_questions[index].question" type="text" placeholder="输入引导性问题内容..." />
                          </div>
                          <div class="input-wrapper" style="margin-top: 10px;">
                            <textarea v-model="systemSettings.welcome_questions[index].answer" placeholder="预设回答内容 (可选，填入后将立即回复此内容)" @input="autoResize" class="auto-height-textarea"></textarea>
                          </div>
                        </div>
                      </div>
                      <button v-if="systemSettings.welcome_questions.length < 6" class="add-q-btn" @click="systemSettings.welcome_questions.push({ question: '', answer: '' }); triggerAllAutoResize()">
                        <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                        添加预设问题与快速回答
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="settings-footer" style="border-top: 1px solid #f1f5f9; padding-top: 20px;">
                <button class="beauty-save-btn" @click="saveSystemSettings" :disabled="loading">
                  <span v-if="!loading">保存对话配置</span>
                  <div v-else class="btn-spinner"></div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'brand'" class="tab-content">
          <div class="settings-container-beauty">
            <div class="settings-main-card">
              <div class="settings-header">
                <div class="settings-header-icon">
                  <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>
                </div>
                <div>
                  <h3>品牌形象设置</h3>
                  <p>在这里自定义您招新助手的全站品牌视觉与基础信息</p>
                </div>
              </div>

              <div class="settings-grid">
                <div class="settings-form-section">
                  <div class="beauty-form-group">
                    <label><svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg> 助手显示名称</label>
                    <div class="input-wrapper">
                      <input v-model="systemSettings.assistant_name" type="text" placeholder="例如：迎新智能助手" />
                    </div>
                  </div>

                  <div class="beauty-form-group">
                    <label><svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><path d="M17 18a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2"></path><rect x="3" y="4" width="18" height="18" rx="2"></rect><circle cx="12" cy="10" r="2"></circle><line x1="7" y1="8" x2="7" y2="8"></line><line x1="17" y1="8" x2="17" y2="8"></line></svg> 助手副标题</label>
                    <div class="input-wrapper">
                      <input v-model="systemSettings.system_subtitle" type="text" placeholder="设置助手下方的描述文字" />
                    </div>
                  </div>

                  <div class="beauty-form-group">
                    <label><svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg> 底部版权信息</label>
                    <div class="input-wrapper">
                      <input v-model="systemSettings.system_footer" type="text" placeholder="例如：© 平顶山工业职业技术学院" />
                    </div>
                  </div>
                </div>

                <div class="settings-avatar-section">
                  <label class="section-label">助手头像</label>
                  <div class="avatar-upload-beauty" @click="$refs.avatarInput.click()">
                    <div class="avatar-preview-wrapper">
                      <img :src="systemSettings.assistant_avatar || '/avatar.png'" alt="头像" @error="e => e.target.src='https://api.dicebear.com/7.x/bottts/svg?seed=Enrollee&backgroundColor=6366f1'" />
                      <div class="avatar-overlay">
                        <svg viewBox="0 0 24 24" width="24" height="24" stroke="white" stroke-width="2" fill="none"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                        <span>点击上传</span>
                      </div>
                    </div>
                    <input type="file" ref="avatarInput" @change="handleAvatarUpload" accept="image/*" class="hidden-input" />
                    <div class="upload-hint">建议尺寸 200x200，支持 JPG, PNG</div>
                  </div>
                </div>
              </div>

              <div class="settings-footer">
                <button class="beauty-save-btn" @click="saveSystemSettings" :disabled="loading">
                  <span v-if="!loading">保存品牌配置</span>
                  <div v-else class="btn-spinner"></div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'settings'" class="tab-content">
          <div class="settings-container-beauty">
            <div class="settings-main-card">
              <div class="settings-header">
                <div class="settings-header-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                </div>
                <div>
                  <h3>系统高级设置</h3>
                  <p>配置系统底层参数与技术选项（即将推出）</p>
                </div>
              </div>
              <div class="settings-grid" style="padding: 100px; text-align: center; color: var(--text-light); border-top: 1px solid #f1f5f9;">
                暂无高级配置项
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'chat'" class="tab-content">
          <div class="chat-test-container">
            <div class="chat-test-messages" ref="chatContainer">
              <div v-if="chatMessages.length === 0" class="chat-test-empty">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                <p>输入问题测试当前激活的提示词效果</p>
              </div>
              <div v-for="(msg, idx) in chatMessages" :key="idx" :class="['chat-test-msg', msg.role === 'user' ? 'msg-user' : 'msg-assistant']">
                <!-- Avatar removed per user request -->
                <div class="msg-bubble-sm" v-html="renderChatContent(msg.content)"></div>
              </div>
              <div v-if="chatLoading && !chatStreamText" class="chat-test-msg msg-assistant">
                <!-- Avatar removed per user request -->
                <div class="typing-indicator-sm"><span></span><span></span><span></span></div>
              </div>
              <div v-if="chatLoading && chatStreamText" class="chat-test-msg msg-assistant">
                <!-- Avatar removed per user request -->
                <div class="msg-bubble-sm" v-html="renderChatContent(chatStreamText)"></div>
              </div>
            </div>
            <div class="chat-test-input">
              <input v-model="chatInput" @keyup.enter="sendChatTest" placeholder="输入测试问题..." :disabled="chatLoading" />
              <button @click="sendChatTest" :disabled="chatLoading || !chatInput.trim()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              </button>
              <button @click="clearChatTest" title="清空对话" class="clear-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              </button>
            </div>
          </div>
        </div>
      </div> <!-- Closes admin-content -->
    </div> <!-- Closes admin-main -->
  </div> <!-- Closes admin-layout -->
</template>

<script>
import { marked } from 'marked'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'users',
      currentUser: null,
      users: [],
      knowledgeDocs: [],
      prompts: [],
      knowledgeKeyword: '',
      showUserForm: false,
      showKnowledgeForm: false,
      showPromptForm: false,
      editingUser: null,
      editingDoc: null,
      editingPrompt: null,
      userForm: { username: '', password: '', role: 'editor' },
      knowledgeForm: { title: '', content: '', is_active: true },
      selectedFile: null,
      loading: false,
      images: [],
      showImageForm: false,
      imageForm: { title: '', tags: '' },
      selectedImageFile: null,
      promptForm: { name: '', content: '', is_active: false },
      formError: '',
      chatMessages: [],
      chatInput: '',
      chatLoading: false,
      chatStreamText: '',
      systemSettings: {
        assistant_name: '',
        assistant_avatar: '',
        system_subtitle: '',
        system_footer: '',
        welcome_questions: [],
        system_greeting: ''
      },
      selectedAvatarFile: null,
    }
  },
  computed: {
    tabTitle() {
      const titles = { users: '用户管理', knowledge: '知识库管理', images: '媒体库管理', prompts: '提示词管理', questions: '对话管理', brand: '品牌化配置', chat: '对话测试', settings: '系统设置' }
      return titles[this.activeTab] || ''
    },
  },
  watch: {
    activeTab(val) {
      if (['questions', 'brand', 'knowledge', 'prompts'].includes(val)) {
        this.triggerAllAutoResize()
      }
    }
  },
  async mounted() {
    await this.checkLogin()
    await this.loadUsers()
    await this.loadKnowledge()
    await this.loadImages()
    await this.loadPrompts()
    await this.loadSystemSettings()
  },
  methods: {
    async checkLogin() {
      try {
        const res = await fetch('/api/admin/check')
        const data = await res.json()
        if (!data.logged_in) {
          this.$router.push('/admin/login')
          return
        }
        this.currentUser = data.user
      } catch (e) {
        this.$router.push('/admin/login')
      }
    },
    async loadUsers() {
      try {
        const res = await fetch('/api/admin/users')
        const data = await res.json()
        if (res.ok) this.users = data.users
      } catch (e) {}
    },
    async loadKnowledge() {
      try {
        const url = this.knowledgeKeyword ? `/api/admin/knowledge?keyword=${encodeURIComponent(this.knowledgeKeyword)}` : '/api/admin/knowledge'
        const res = await fetch(url)
        const data = await res.json()
        if (res.ok) this.knowledgeDocs = data.documents
      } catch (e) {}
    },
    async loadImages() {
      try {
        const res = await fetch('/api/admin/images')
        const data = await res.json()
        if (res.ok) this.images = data.images
      } catch (e) {}
    },
    handleImageFileUpload(e) {
      this.selectedImageFile = e.target.files[0]
      if (this.selectedImageFile && !this.imageForm.title) {
        const name = this.selectedImageFile.name
        this.imageForm.title = name.substring(0, name.lastIndexOf('.')) || name
      }
    },
    async saveImage() {
      this.formError = ''
      if (!this.selectedImageFile) {
        this.formError = '请选择要上传的图片'
        return
      }

      this.loading = true
      try {
        const formData = new FormData()
        formData.append('image', this.selectedImageFile)
        formData.append('title', this.imageForm.title)
        formData.append('tags', this.imageForm.tags)

        const res = await fetch('/api/admin/images', {
          method: 'POST',
          body: formData,
        })
        const data = await res.json()
        if (res.ok) {
          this.showImageForm = false
          this.selectedImageFile = null
          await this.loadImages()
        } else {
          this.formError = data.error || '上传失败'
        }
      } catch (e) {
        this.formError = '网络连接失败'
      } finally {
        this.loading = false
      }
    },
    async deleteImage(id) {
      if (!confirm('确定删除该图片？')) return
      try {
        const res = await fetch(`/api/admin/images/${id}`, { method: 'DELETE' })
        if (res.ok) await this.loadImages()
      } catch (e) {}
    },
    async loadPrompts() {
      try {
        const res = await fetch('/api/admin/prompts')
        const data = await res.json()
        if (res.ok) this.prompts = data.prompts
      } catch (e) {}
    },
    async loadSystemSettings() {
      try {
        const res = await fetch('/api/admin/settings')
        const data = await res.json()
        if (res.ok) {
          // Migrate welcome_questions if they are strings
          if (data.welcome_questions && Array.isArray(data.welcome_questions)) {
            data.welcome_questions = data.welcome_questions.map(q => {
              if (typeof q === 'string') return { question: q, answer: '' }
              return q
            })
          }
          this.systemSettings = data
          this.updateFavicon()
          this.triggerAllAutoResize()
        }
      } catch (e) {}
    },
    updateFavicon() {
      if (this.systemSettings.assistant_avatar) {
        let link = document.querySelector("link[rel~='icon']")
        if (!link) {
          link = document.createElement('link')
          link.rel = 'icon'
          document.head.appendChild(link)
        }
        link.href = this.systemSettings.assistant_avatar
      }
    },
    handleAvatarUpload(e) {
      const file = e.target.files[0]
      if (file) {
        this.selectedAvatarFile = file
        // Preview
        const reader = new FileReader()
        reader.onload = (e) => {
          this.systemSettings.assistant_avatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    async saveSystemSettings() {
      this.loading = true
      try {
        const formData = new FormData()
        formData.append('assistant_name', this.systemSettings.assistant_name)
        formData.append('assistant_subtitle', this.systemSettings.system_subtitle)
        formData.append('assistant_footer', this.systemSettings.system_footer)
        const validQuestions = this.systemSettings.welcome_questions.filter(q => {
          if (typeof q === 'string') return q.trim() !== ''
          return q.question && q.question.trim() !== ''
        })
        formData.append('welcome_questions', JSON.stringify(validQuestions))
        formData.append('system_greeting', this.systemSettings.system_greeting)
        if (this.selectedAvatarFile) {
          formData.append('assistant_avatar', this.selectedAvatarFile)
        }
        
        const res = await fetch('/api/admin/settings', {
          method: 'POST',
          body: formData
        })
        const data = await res.json()
        if (res.ok) {
          this.systemSettings = data
          this.selectedAvatarFile = null
          this.updateFavicon()
          alert('设置保存成功')
        }
      } catch (e) {
        alert('保存失败')
      } finally {
        this.loading = false
      }
    },
    async saveUser() {
      this.formError = ''
      if (!this.userForm.username) {
        this.formError = '请输入用户名'
        return
      }
      if (!this.editingUser && !this.userForm.password) {
        this.formError = '请输入密码'
        return
      }

      try {
        let res
        if (this.editingUser) {
          res = await fetch(`/api/admin/users/${this.editingUser.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.userForm),
          })
        } else {
          res = await fetch('/api/admin/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.userForm),
          })
        }
        const data = await res.json()
        if (res.ok) {
          this.showUserForm = false
          await this.loadUsers()
        } else {
          this.formError = data.error || '操作失败'
        }
      } catch (e) {
        this.formError = '网络连接失败'
      }
    },
    async deleteUser(id) {
      if (!confirm('确定删除该用户？')) return
      try {
        const res = await fetch(`/api/admin/users/${id}`, { method: 'DELETE' })
        if (res.ok) await this.loadUsers()
      } catch (e) {}
    },
    handleKnowledgeFileUpload(e) {
      this.selectedFile = e.target.files[0]
      if (this.selectedFile && !this.knowledgeForm.title) {
        // Auto fill title with filename (without extension)
        const name = this.selectedFile.name
        this.knowledgeForm.title = name.substring(0, name.lastIndexOf('.')) || name
      }
    },
    async saveKnowledge() {
      this.formError = ''
      
      if (!this.editingDoc && !this.selectedFile) {
        this.formError = '请选择要上传的文件'
        return
      }

      this.loading = true
      try {
        let res
        if (this.editingDoc) {
          // Editing existing doc (content update)
          res = await fetch(`/api/admin/knowledge/${this.editingDoc.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.knowledgeForm),
          })
        } else {
          // New doc upload
          const formData = new FormData()
          formData.append('file', this.selectedFile)
          formData.append('title', this.knowledgeForm.title)
          formData.append('is_active', this.knowledgeForm.is_active)
          
          res = await fetch('/api/admin/knowledge', {
            method: 'POST',
            body: formData,
          })
        }
        const data = await res.json()
        if (res.ok) {
          this.showKnowledgeForm = false
          this.selectedFile = null
          await this.loadKnowledge()
        } else {
          this.formError = data.error || '操作失败'
        }
      } catch (e) {
        this.formError = '网络连接失败'
      }
    },
    async deleteKnowledge(id) {
      if (!confirm('确定删除该文档？')) return
      try {
        const res = await fetch(`/api/admin/knowledge/${id}`, { method: 'DELETE' })
        if (res.ok) await this.loadKnowledge()
      } catch (e) {}
    },
    async savePrompt() {
      this.formError = ''
      if (!this.promptForm.name || !this.promptForm.content) {
        this.formError = '请输入名称和内容'
        return
      }

      try {
        let res
        if (this.editingPrompt) {
          res = await fetch(`/api/admin/prompts/${this.editingPrompt.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.promptForm),
          })
        } else {
          res = await fetch('/api/admin/prompts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.promptForm),
          })
        }
        const data = await res.json()
        if (res.ok) {
          this.showPromptForm = false
          await this.loadPrompts()
        } else {
          this.formError = data.error || '操作失败'
        }
      } catch (e) {
        this.formError = '网络连接失败'
      }
    },
    autoResize(e) {
      const el = e.target || e;
      if (!el || !el.style) return;
      el.style.height = 'auto';
      el.style.height = el.scrollHeight + 'px';
    },
    triggerAllAutoResize() {
      this.$nextTick(() => {
        const textareas = document.querySelectorAll('.auto-height-textarea');
        textareas.forEach(ta => this.autoResize(ta));
      });
    },
    async deletePrompt(id) {
      if (!confirm('确定删除该提示词？')) return
      try {
        const res = await fetch(`/api/admin/prompts/${id}`, { method: 'DELETE' })
        if (res.ok) await this.loadPrompts()
      } catch (e) {}
    },
    async activatePrompt(id) {
      try {
        const res = await fetch(`/api/admin/prompts/${id}/activate`, { method: 'POST' })
        if (res.ok) await this.loadPrompts()
      } catch (e) {}
    },
    renderChatContent(content) {
      if (!content) return ''
      
      const renderer = new marked.Renderer()
      renderer.image = (href, title, text) => {
        return `<div class="message-image-wrapper"><img src="${href}" alt="${text || ''}" class="message-image" /></div>`
      }
      
      marked.setOptions({
        renderer: renderer,
        breaks: true,
        gfm: true
      })
      
      return marked.parse(content)
    },
    async sendChatTest() {
      const text = this.chatInput.trim()
      if (!text || this.chatLoading) return

      this.chatMessages.push({ role: 'user', content: text })
      this.chatInput = ''
      this.chatLoading = true
      this.chatStreamText = ''
      this.scrollChat()

      const history = this.chatMessages.slice(0, -1).slice(-10)

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            history: history,
          }),
        })
        const data = await res.json()
        let reply = data.reply || data.error || '服务暂时不可用'
        this.chatMessages.push({ role: 'assistant', content: reply })
      } catch (e) {
        this.chatMessages.push({ role: 'assistant', content: '网络连接出现问题' })
      }

      this.chatLoading = false
      this.chatStreamText = ''
      this.scrollChat()
    },
    clearChatTest() {
      this.chatMessages = []
      this.chatStreamText = ''
    },
    scrollChat() {
      this.$nextTick(() => {
        const c = this.$refs.chatContainer
        if (c) c.scrollTop = c.scrollHeight
      })
    },
    async handleLogout() {
      try {
        await fetch('/api/admin/logout', { method: 'POST' })
      } catch (e) {}
      this.$router.push('/admin/login')
    },
  },
}
</script>

<style scoped>
.admin-layout {
  width: 100%;
  height: 100vh;
  display: flex;
  background: #f8fafc;
}

.admin-sidebar {
  width: var(--sidebar-width);
  background: var(--sidebar-bg);
  color: #f1f5f9;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  transition: var(--transition);
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 20;
}



.admin-sidebar-header {
  padding: 32px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-logo {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.admin-sidebar-header span {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #fff;
}

.admin-nav {
  flex: 1;
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 500;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  margin: 2px 0;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.04);
  color: #fff;
  transform: translateX(4px);
}

.nav-item.active {
  background: var(--primary-gradient);
  color: #fff;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
  font-weight: 600;
}

.nav-item.active svg {
  filter: drop-shadow(0 0 4px rgba(255,255,255,0.4));
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.05);
  margin: 16px 24px;
}

.admin-sidebar-footer {
  padding: 24px 12px;
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.admin-header {
  padding: 0 40px;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border-bottom: 1px solid var(--border);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}



.admin-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -0.5px;
  margin: 0;
}

.user-info {
  font-size: 14px;
  color: var(--text-light);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg);
  border-radius: 20px;
  border: 1px solid var(--border);
}

.admin-content {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  position: relative;
  background: var(--bg);
}

.tab-content {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.primary-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.primary-btn:active {
  transform: translateY(0);
}

.secondary-btn {
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text-light);
  padding: 10px 24px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.secondary-btn:hover {
  background: var(--bg);
  color: var(--primary);
  border-color: var(--primary-light);
}

.search-input {
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text-main);
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-size: 14px;
  outline: none;
  transition: var(--transition);
  width: 280px;
  box-shadow: var(--shadow-sm);
}

.search-input:focus {
  background: var(--card-bg);
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.data-table {
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.05);
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  padding: 24px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-light);
  text-align: left;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

td {
  padding: 22px 24px;
  font-size: 14px;
  color: var(--text-main);
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s;
}

tr:hover td {
  background: #fcfdfe;
}

.empty-row {
  text-align: center;
  color: var(--text-light);
  padding: 60px 0;
  font-style: italic;
}

.status-tag {
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
}

.active-tag {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.inactive-tag {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.action-cell {
  display: flex;
  gap: 12px;
}

.edit-btn, .delete-btn, .activate-btn {
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.edit-btn {
  background: var(--bg);
  color: var(--primary);
  border: 1px solid var(--border);
}

.edit-btn:hover {
  background: var(--primary);
  color: #fff;
}

.delete-btn {
  background: #fff1f2;
  color: #ef4444;
  border: 1px solid #fecdd3;
}

.delete-btn:hover {
  background: #ef4444;
  color: #fff;
}

.activate-btn {
  background: #f0fdf4;
  color: #10b981;
  border: 1px solid #bbf7d0;
}

.activate-btn:hover {
  background: #10b981;
  color: #fff;
}

/* Chat Test Specific Styles */
.chat-test-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 220px);
  background: var(--card-bg);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.chat-test-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: #fcfdfe;
}

.chat-test-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: #94a3b8;
  padding-bottom: 10%; /* Slightly offset upwards for better visual balance */
}

.chat-test-empty p {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

.chat-test-messages::-webkit-scrollbar {
  width: 5px;
}

.chat-test-messages::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 10px;
}

.chat-test-msg {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 85%;
  animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.msg-user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-assistant {
  align-self: flex-start;
}

.msg-avatar-sm {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: #f8fafc;
  margin-right: 12px;
  flex-shrink: 0;
}

.msg-avatar-sm img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.msg-bubble-sm {
  padding: 14px 20px;
  border-radius: 20px;
  font-size: 16px;
  line-height: 2.2;
  position: relative;
  box-shadow: var(--shadow-sm);
}

.msg-bubble-sm :deep(p) {
  margin-bottom: 12px;
}

.msg-bubble-sm :deep(p:last-child) {
  margin-bottom: 0;
}

.msg-user .msg-bubble-sm {
  background: var(--primary);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: none;
}

.msg-assistant .msg-bubble-sm {
  background: var(--card-bg);
  color: var(--text-main);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--border);
}

.chat-test-input {
  padding: 24px 32px;
  background: var(--card-bg);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 16px;
}

.chat-test-input input {
  flex: 1;
  background: var(--bg);
  border: 1px solid var(--border);
  padding: 14px 24px;
  border-radius: var(--radius-lg);
  color: var(--text-main);
  font-size: 15px;
  outline: none;
  transition: var(--transition);
}

.chat-test-input input:focus {
  background: var(--card-bg);
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.05);
}

.chat-test-input button {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
}

.chat-test-input button:first-of-type {
  background: var(--primary-gradient);
  color: #fff;
  border: none;
  box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
}

.chat-test-input button:first-of-type:hover {
  transform: translateY(-2px);
}

.chat-test-input .clear-btn {
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text-light);
}

.chat-test-input .clear-btn:hover {
  background: #fff1f2;
  color: #ef4444;
  border-color: #fecdd3;
}

/* Settings Styling */
.settings-container {
  padding: 20px;
  max-width: 800px;
}

.settings-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 32px;
  box-shadow: var(--shadow-md);
}

.settings-card h3 {
  margin-bottom: 24px;
  color: var(--text-main);
  font-size: 20px;
}

.avatar-setting {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 16px;
  background: var(--bg);
  border-radius: var(--radius-lg);
}

.avatar-preview-lg {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  overflow: hidden;
  border: 2px solid #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.avatar-preview-lg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-upload .tip {
  font-size: 12px;
  color: var(--text-light);
  margin-top: 8px;
}

.settings-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 40px;
  width: 500px;
  max-width: 90%;
  box-shadow: var(--shadow-2xl);
  position: relative;
  animation: modalEnter 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-card-lg {
  width: 850px;
}

@keyframes modalEnter {
  from { transform: scale(0.9) translateY(20px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}

.modal-card h3 {
  color: var(--text-main);
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 32px;
  letter-spacing: -0.5px;
}

.form-group {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-light);
  display: block;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text-main);
  border-radius: var(--radius-md);
  font-size: 15px;
  transition: var(--transition);
  outline: none;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  border-color: var(--primary);
  background: var(--card-bg);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.form-error {
  background: #fff1f2;
  color: #e11d48;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  margin-bottom: 20px;
  border: 1px solid #ffe4e6;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 40px;
}

.cancel-btn {
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text-light);
  padding: 10px 24px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.cancel-btn:hover {
  background: #f1f5f9;
  color: var(--text-main);
}

.typing-indicator-sm {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: var(--bg);
  border-radius: 20px;
  border: 1px solid var(--border);
}

.typing-indicator-sm span {
  width: 5px;
  height: 5px;
  background: var(--primary);
  border-radius: 50%;
  animation: typing 1.2s infinite ease-in-out;
}

.typing-indicator-sm span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator-sm span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 100% { transform: translateY(0); opacity: 0.3; }
  50% { transform: translateY(-4px); opacity: 1; }
}

.file-upload-wrapper {
  border: 2px dashed #e2e8f0;
  border-radius: var(--radius-lg);
  padding: 32px;
  text-align: center;
  background: #f8fafc;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.file-upload-wrapper:hover {
  border-color: var(--primary);
  background: var(--primary-soft);
  transform: translateY(-2px);
}

.hidden-file-input {
  display: none;
}

.upload-icon {
  color: var(--primary);
  margin-bottom: 12px;
  opacity: 0.8;
}

.upload-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 8px;
}

.selected-filename {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--primary);
  background: white;
  padding: 6px 12px;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.file-tip {
  font-size: 12px;
  color: var(--text-muted);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.image-card {
  background: white;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: var(--transition);
}

.image-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.image-preview {
  width: 100%;
  aspect-ratio: 16/9;
  background: #f1f5f9;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-info {
  padding: 12px;
}

.image-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
  min-height: 24px;
}

.tag {
  font-size: 11px;
  background: var(--primary-soft);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 4px;
}

.image-actions {
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
  background: var(--bg-soft);
  border-radius: var(--radius-md);
  border: 2px dashed var(--border);
}

:deep(.message-image-wrapper) {
  margin: 8px 8px 4px 0;
  display: inline-block;
  vertical-align: top;
  max-width: 100%;
}

:deep(.message-image) {
  max-width: 320px;
  width: auto;
  height: auto;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  display: block;
}

.msg-bubble-sm :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  font-size: 14px;
}

.msg-bubble-sm :deep(th), .msg-bubble-sm :deep(td) {
  padding: 12px 16px;
  border: 1px solid var(--border);
  text-align: left;
  line-height: 1.5;
}

.msg-bubble-sm :deep(th) {
  background: #f8fafc;
  font-weight: 700;
  color: var(--text-main);
  border-bottom: 2px solid var(--border);
}

.msg-bubble-sm :deep(tr:nth-child(even)) {
  background: #fcfdfe;
}

.msg-bubble-sm :deep(tr:hover) {
  background: #f1f5f9;
}

/* Settings Beautification */
.settings-container-beauty {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.settings-main-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.03), 0 4px 20px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.settings-header {
  padding: 20px 32px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 20px;
}

.settings-header-icon {
  width: 48px;
  height: 48px;
  background: var(--primary-gradient);
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 24px rgba(99, 102, 241, 0.2);
}

.settings-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main);
  margin: 0 0 4px 0;
}

.settings-header p {
  font-size: 14px;
  color: var(--text-light);
  margin: 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 40px;
  padding: 24px 40px;
}

.beauty-form-group {
  margin-bottom: 20px;
}

.beauty-form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 10px;
}

.beauty-form-group .input-wrapper {
  position: relative;
}

.beauty-form-group textarea, .beauty-form-group input {
  width: 100%;
  padding: 12px 20px;
  background: #f8fafc;
  border: 2px solid transparent;
  border-radius: 14px;
  font-size: 15px;
  line-height: 1.5;
  color: var(--text-main);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);
}

.beauty-form-group textarea:focus, .beauty-form-group input:focus {
  background: white;
  border-color: var(--primary-light);
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.08);
  outline: none;
  transform: translateY(-2px);
}

.settings-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #fcfdfe;
  border-radius: 20px;
  border: 1px dashed #e2e8f0;
}

.section-label {
  font-size: 14px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 24px;
}

.avatar-upload-beauty {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.avatar-preview-wrapper {
  width: 140px;
  height: 140px;
  border-radius: 30px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  border: 4px solid white;
}

.avatar-preview-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  gap: 8px;
}

.avatar-upload-beauty:hover .avatar-overlay {
  opacity: 1;
}

.avatar-overlay span {
  font-size: 12px;
  font-weight: 600;
}

.upload-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 16px;
  text-align: center;
}

.hidden-input {
  display: none;
}

.settings-footer {
  padding: 20px 40px;
  background: #f8fafc;
  display: flex;
  justify-content: center;
  border-top: 1px solid #f1f5f9;
}

.beauty-save-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  padding: 14px 40px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
}

.beauty-save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px rgba(99, 102, 241, 0.3);
}

.beauty-save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

.question-input-card-item {
  background: #f8fafc;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.question-input-card-item:hover {
  border-color: var(--primary-light);
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.q-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #e2e8f0;
}

.q-item-index {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.remove-q-btn-beauty {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: #fef2f2;
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-q-btn-beauty:hover {
  background: #fee2e2;
  color: #dc2626;
  transform: scale(1.1);
}

.q-item-body .input-wrapper input {
  width: 100%;
  padding: 10px 14px !important;
  background: white !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 10px !important;
  font-size: 14px !important;
}

.q-item-body .input-wrapper textarea {
  width: 100%;
  padding: 10px 14px !important;
  background: white !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 10px !important;
  font-size: 14px !important;
  resize: none;
}

.q-item-body .input-wrapper input:focus, .q-item-body .input-wrapper textarea:focus {
  border-color: var(--primary) !important;
  outline: none;
}

.add-q-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 2px dashed #e2e8f0;
  background: #fcfdfe;
  color: #64748b;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 8px;
}

.add-q-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.05);
}
.auto-height-textarea {
  overflow: hidden;
  resize: none;
  min-height: 46px;
  line-height: 1.6;
}
</style>