<script setup>
import { ref } from 'vue'

const features = ref([
  {
    icon: '⌨️',
    title: '逐字符模拟输入',
    desc: '使用底层键盘接口模拟真实击键，绕过一切粘贴限制。支持所有字符和特殊键。',
    color: 'var(--primary)',
  },
  {
    icon: '🧠',
    title: '智能缩进还原',
    desc: '自动检测并保留代码原始缩进层级，精确还原每一行的缩进深度。无需手动处理。',
    color: 'var(--secondary)',
  },
  {
    icon: '⚡',
    title: '一键快捷操作',
    desc: '简要模式下一键清空+粘贴+开始输入，配合全局快捷键操作如飞。',
    color: 'var(--accent)',
  },
  {
    icon: '🪟',
    title: '迷你置顶窗口',
    desc: '一键缩为迷你窗口并置顶显示，不挡视线，做题时自由切换。',
    color: 'var(--green)',
  },
  {
    icon: '🎛️',
    title: '双模式自由切换',
    desc: '简要模式4按钮精简操作，高级模式完整功能面板，标题栏分段开关一键切换。',
    color: 'var(--code-keyword)',
  },
  {
    icon: '🎨',
    title: '玻璃拟态美学',
    desc: '源自 Phycat 主题的 Dracula 配色，毛玻璃卡片设计，暗色护眼。',
    color: 'var(--code-function)',
  },
])
</script>

<template>
  <section class="features">
    <div class="container">
      <h2 class="section-title">核心特性</h2>
      <div class="features-grid">
        <div
          v-for="(feat, i) in features"
          :key="i"
          class="feature-card glass-card"
          :style="{ '--feat-color': feat.color }"
        >
          <div class="feature-card__icon" :style="{ color: feat.color }">
            {{ feat.icon }}
          </div>
          <h3 class="feature-card__title">{{ feat.title }}</h3>
          <p class="feature-card__desc">{{ feat.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.features {
  padding: 4rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.feature-card {
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--feat-color), transparent);
  opacity: 0.6;
}

.feature-card__icon {
  font-size: 2.4rem;
  margin-bottom: 1rem;
}

.feature-card__title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 0.6rem;
}

.feature-card__desc {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.7;
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
