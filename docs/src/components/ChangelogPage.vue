<script setup>
const releases = [
  {
    version: 'v1.2.1',
    date: '2026-04-26',
    tag: 'v1.2.1',
    type: 'fix',
    title: '修复打包后自定义字体在未安装字体电脑上显示为宋体的问题',
    changes: [
      '新增 FontManager 字体注册模块，使用 Windows API 动态注册 Maple Mono 字体',
      '解决 Tkinter 在未安装字体环境下回退为宋体的兼容性问题',
      '重写字体管理逻辑，分离字体注册与字体对象创建',
    ],
  },
  {
    version: 'v1.2',
    date: '2026-04-25',
    tag: 'v1.2',
    type: 'feat',
    title: '新增迷你模式与智能缩进功能，全面优化 UI 和交互体验',
    changes: [
      '新增迷你模式：隐藏预览区和提示区，仅保留核心操作按钮，自动置顶',
      '新增智能缩进功能：保留代码原始缩进，精确还原每一行缩进层级',
      '优化 UI 组件模块化：拆分 TitleFrame、ToolbarFrame、ConfigFrame、TextPreviewFrame 等独立组件',
      '改进工具栏布局和按钮状态管理',
    ],
  },
  {
    version: 'v1.0 (Beta)',
    date: '2026-04-25',
    tag: 'v1.0_beta',
    type: 'feat',
    title: '实现智能缩进功能并优化代码结构',
    changes: [
      '引入智能缩进引擎，Shift+Enter 换行跳过 IDE 自动缩进',
      '新增缩进宽度可配置（默认 4 空格）',
      '重构 TypingEngine，分离普通模式和智能缩进模式的输入逻辑',
      '优化代码组织结构，提升可维护性',
    ],
  },
  {
    version: '项目初始化',
    date: '2026-04-21',
    tag: null,
    type: 'chore',
    title: 'FakeyPaste 模拟键盘输入工具初始提交',
    changes: [
      '实现核心模拟键盘输入功能，逐字符模拟真实击键',
      '支持全局快捷键 Ctrl+Shift+P 开始、Ctrl+Shift+L 暂停',
      '剪贴板集成，一键从剪贴板导入内容',
      '可配置字符间隔和开始延时',
      '现代化暗色主题 UI 界面',
      '添加 README.md 项目说明文档',
    ],
  },
]
</script>

<template>
  <div class="page">
    <header class="page-header glass">
      <div class="container page-header-inner">
        <a href="./index.html" class="back-link">← 返回使用说明</a>
        <h1 class="page-title">更新历史</h1>
        <span class="page-sub">FakeyPaste Changelog</span>
      </div>
    </header>

    <main class="container">
      <div class="timeline">
        <div
          v-for="(rel, i) in releases"
          :key="i"
          class="release glass-card"
          :class="{ 'release--latest': i === 0 }"
        >
          <div class="release-badge" :class="`release-badge--${rel.type}`">
            {{ rel.type === 'feat' ? '✨ 新功能' : rel.type === 'fix' ? '🐛 修复' : '🎉 初始' }}
          </div>

          <div class="release-body">
            <div class="release-head">
              <h2 class="release-version">
                {{ rel.version }}
                <span v-if="i === 0" class="release-latest-tag">最新</span>
              </h2>
              <span class="release-date">{{ rel.date }}</span>
            </div>

            <h3 class="release-title">{{ rel.title }}</h3>

            <ul class="release-changes">
              <li v-for="(c, j) in rel.changes" :key="j">{{ c }}</li>
            </ul>

            <div v-if="rel.tag" class="release-links">
              <a :href="`https://github.com/Kai-Zs/FakeyPaste/releases/tag/${rel.tag}`" target="_blank" rel="noopener">
                查看 Release →
              </a>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="page-footer">
      <div class="container">
        <p>© 2026 凯Z闪 (KaiZs) · <a href="https://github.com/Kai-Zs/FakeyPaste" target="_blank" rel="noopener">GitHub</a></p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
}

.page-header {
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
  padding: 3rem 0 2rem;
}

.page-header-inner {
  text-align: center;
}

.back-link {
  display: inline-block;
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.back-link:hover {
  color: var(--accent);
}

.page-title {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--text-color);
  text-shadow: 0 0 30px var(--primary-glow);
}

.page-sub {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 0.5rem;
}

.timeline {
  padding: 3rem 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 40px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--primary), var(--secondary), transparent);
  opacity: 0.3;
}

.release {
  position: relative;
  padding: 1.8rem 1.8rem 1.8rem 7rem;
  margin-bottom: 1.5rem;
}

.release--latest {
  border-color: rgba(255, 85, 85, 0.3);
  box-shadow: 0 0 30px rgba(255, 85, 85, 0.08);
}

.release-badge {
  position: absolute;
  left: -6px;
  top: 1.8rem;
  width: 90px;
  padding: 0.3em 0;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-align: center;
  z-index: 2;
}

.release-badge--feat {
  background: rgba(139, 233, 253, 0.15);
  color: var(--accent);
  border: 1px solid rgba(139, 233, 253, 0.3);
}

.release-badge--fix {
  background: rgba(255, 85, 85, 0.15);
  color: var(--primary);
  border: 1px solid rgba(255, 85, 85, 0.3);
}

.release-badge--chore {
  background: rgba(80, 250, 123, 0.12);
  color: var(--green);
  border: 1px solid rgba(80, 250, 123, 0.25);
}

.release-head {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.release-version {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.release-latest-tag {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15em 0.6em;
  border-radius: 4px;
  background: rgba(255, 85, 85, 0.15);
  color: var(--primary);
}

.release-date {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.release-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.8rem;
}

.release-changes {
  list-style: none;
  padding: 0;
}

.release-changes li {
  position: relative;
  padding-left: 1.2rem;
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.9;
}

.release-changes li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.7em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
  opacity: 0.5;
}

.release-links {
  margin-top: 1rem;
}

.release-links a {
  font-size: 0.85rem;
  color: var(--accent);
}

.release-links a:hover {
  color: var(--secondary);
}

.page-footer {
  padding: 2rem 0;
  border-top: 1px solid var(--border-glass);
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.page-footer a {
  color: var(--text-muted);
}

.page-footer a:hover {
  color: var(--accent);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.8rem;
  }
  .release {
    padding: 1.5rem 1rem 1.5rem 5.5rem;
  }
  .release-badge {
    left: 0;
    width: 70px;
    font-size: 0.7rem;
  }
  .timeline::before {
    left: 24px;
  }
}
</style>
