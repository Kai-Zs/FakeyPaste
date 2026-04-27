<script setup>
import { ref } from 'vue'

const activeTab = ref('simple')

const modes = [
  { key: 'simple', label: '简要模式' },
  { key: 'advanced', label: '高级模式' },
]

const simpleSteps = [
  {
    num: '1',
    title: '复制本文',
    desc: '在任意位置复制需要模拟输入的文本内容，或使用 <kbd>Ctrl</kbd> + <kbd>C</kbd> 复制。',
  },
  {
    num: '2',
    title: '点击按钮或快捷键',
    desc: '点击「N秒后开始」按钮，或按下 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> 快捷键，自动载入剪贴板内容并准备输入。',
  },
  {
    num: '3',
    title: '切换窗口并定位光标',
    desc: '在倒计时的 N 秒内，迅速将焦点切换到目标输入窗口，并将光标置于需要输入的位置。',
  },
  {
    num: '4',
    title: '自动逐字输入',
    desc: '倒计时结束后，FakeyPaste 自动开始逐字符模拟键盘输入，真实还原手动打字效果。',
  },
]

const advancedSteps = [
  {
    num: '1',
    title: '载入内容',
    desc: '点击「从剪贴板粘贴」将剪贴板内容载入预览区，支持手动编辑。',
  },
  {
    num: '2',
    title: '配置参数',
    desc: '调整字符间隔（毫秒）、开始延时（秒）、智能缩进和缩进宽度。',
  },
  {
    num: '3',
    title: '开始输入',
    desc: '点击「开始」按钮或 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>，在延时内切到目标窗口。',
  },
  {
    num: '4',
    title: '灵活控制',
    desc: '输入中可「暂停」/「继续」，随时「停止」中止。暂停后快捷键 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> 可恢复。',
  },
]
</script>

<template>
  <section class="usage">
    <div class="container">
      <h2 class="section-title">使用说明</h2>

      <div class="usage-tabs glass">
        <button
          v-for="m in modes"
          :key="m.key"
          class="usage-tab"
          :class="{ 'usage-tab--active': activeTab === m.key }"
          @click="activeTab = m.key"
        >
          {{ m.label }}
        </button>
        <div class="usage-tab-slider" :style="{ transform: `translateX(${activeTab === 'simple' ? 0 : 100}%)` }"></div>
      </div>

      <div class="usage-steps">
        <template v-if="activeTab === 'simple'">
          <div v-for="(step, i) in simpleSteps" :key="i" class="usage-step glass-card">
            <div class="usage-step__num">{{ step.num }}</div>
            <div class="usage-step__body">
              <h3 class="usage-step__title">{{ step.title }}</h3>
              <p class="usage-step__desc" v-html="step.desc"></p>
            </div>
          </div>

          <div class="usage-tip glass-card">
            <div class="usage-tip__icon">💡</div>
            <div class="usage-tip__body">
              <strong>快捷操作：</strong><br />
              暂停输入：<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd><br />
              输入中的开始快捷键会自动忽略，防止误操作。
            </div>
          </div>

          <div class="usage-tip glass-card">
            <div class="usage-tip__icon">🔌</div>
            <div class="usage-tip__body">
              <strong>模式切换：</strong><br />
              点击标题栏的「简要模式 | 高级模式」分段开关即可切换。<br />
              切换到高级模式后，所有按钮恢复正常，可自由修改延迟等参数。
            </div>
          </div>
        </template>

        <template v-else>
          <div v-for="(step, i) in advancedSteps" :key="i" class="usage-step glass-card">
            <div class="usage-step__num">{{ step.num }}</div>
            <div class="usage-step__body">
              <h3 class="usage-step__title">{{ step.title }}</h3>
              <p class="usage-step__desc" v-html="step.desc"></p>
            </div>
          </div>

          <div class="usage-tip glass-card">
            <div class="usage-tip__icon">🔗</div>
            <div class="usage-tip__body">
              点击标题栏分段开关「简要模式」即可回到精简界面。
            </div>
          </div>
        </template>
      </div>
    </div>
  </section>
</template>

<style scoped>
.usage {
  padding: 4rem 0;
}

.usage-tabs {
  display: flex;
  position: relative;
  padding: 4px;
  margin-bottom: 2.5rem;
  max-width: 320px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 10px;
}

.usage-tab {
  flex: 1;
  padding: 0.6rem 0;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.95rem;
  font-weight: 600;
  font-family: var(--font-family);
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: color 0.3s;
  border-radius: 8px;
}

.usage-tab--active {
  color: var(--text-color);
}

.usage-tab-slider {
  position: absolute;
  top: 4px;
  bottom: 4px;
  width: calc(50% - 4px);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.usage-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.usage-step {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  align-items: flex-start;
}

.usage-step__num {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-color);
  flex-shrink: 0;
  box-shadow: 0 0 12px var(--primary-glow);
}

.usage-step__title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 0.35rem;
}

.usage-step__desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

.usage-tip {
  display: flex;
  gap: 1rem;
  padding: 1.2rem 1.5rem;
  align-items: flex-start;
}

.usage-tip__icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.usage-tip__body {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

@media (max-width: 768px) {
  .usage-step {
    flex-direction: column;
    gap: 0.8rem;
    text-align: center;
    align-items: center;
  }
}
</style>
