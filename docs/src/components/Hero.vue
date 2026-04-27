<script setup>
</script>

<template>
  <section class="hero">
    <div class="hero-bg-orb hero-bg-orb--red"></div>
    <div class="hero-bg-orb hero-bg-orb--cyan"></div>
    <div class="hero-bg-orb hero-bg-orb--purple"></div>

    <div class="container hero-inner">
      <div class="hero-badge glass">v1.2.1 · 完全免费</div>

      <h1 class="hero-title">
        Fakey<span class="hero-title__accent">Paste</span>
      </h1>

      <p class="hero-desc">
        轻量级模拟键盘输入工具<br />
        解决网页 IDE、受限系统无法粘贴代码的难题
      </p>

      <div class="hero-actions">
        <a href="https://github.com/Kai-Zs/FakeyPaste" target="_blank" rel="noopener" class="hero-btn glass-card">
          <svg class="hero-btn__icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.73.083-.73 1.205.085 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12 24 5.37 18.63 0 12 0z"/></svg>
          GitHub
        </a>
        <a href="https://github.com/Kai-Zs/FakeyPaste/releases" target="_blank" rel="noopener" class="hero-btn hero-btn--download glass-card">
          ⬇️ 下载最新版
        </a>
      </div>

      <div class="hero-modes">
        <div class="hero-mode glass-card">
          <div class="hero-mode__icon">⚡</div>
          <div class="hero-mode__name">简要模式</div>
          <div class="hero-mode__desc">一键开始，极致精简</div>
        </div>
        <div class="hero-mode glass-card">
          <div class="hero-mode__icon">🔧</div>
          <div class="hero-mode__name">高级模式</div>
          <div class="hero-mode__desc">完整控制，随心所欲</div>
        </div>
        <div class="hero-mode glass-card">
          <div class="hero-mode__icon">📌</div>
          <div class="hero-mode__name">迷你模式</div>
          <div class="hero-mode__desc">置顶小窗，做题利器</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 6rem 0 4rem;
  text-align: center;
  overflow: hidden;
}

.hero-bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
}

.hero-bg-orb--red {
  width: 420px;
  height: 420px;
  background: var(--primary);
  top: -80px;
  left: -60px;
}

.hero-bg-orb--cyan {
  width: 300px;
  height: 300px;
  background: var(--accent);
  top: 80px;
  right: -80px;
}

.hero-bg-orb--purple {
  width: 240px;
  height: 240px;
  background: var(--secondary);
  bottom: -40px;
  left: 60%;
}

.hero-inner {
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-block;
  padding: 0.35em 1.2em;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
  color: var(--text-color);
  text-shadow: 0 0 40px var(--primary-glow), 0 0 80px var(--primary-glow);
}

.hero-title__accent {
  color: var(--primary);
}

.hero-desc {
  font-size: 1.2rem;
  color: var(--text-secondary);
  line-height: 1.9;
  margin-bottom: 1.5rem;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-color);
  text-decoration: none;
  cursor: pointer;
}

.hero-btn__icon {
  width: 20px;
  height: 20px;
}

.hero-btn--download {
  color: var(--accent);
}

.hero-modes {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.hero-mode {
  width: 220px;
  padding: 1.8rem 1.5rem;
  text-align: center;
}

.hero-mode__icon {
  font-size: 2rem;
  margin-bottom: 0.8rem;
}

.hero-mode__name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 0.4rem;
}

.hero-mode__desc {
  font-size: 0.85rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.8rem;
  }
  .hero-modes {
    flex-direction: column;
    align-items: center;
  }
  .hero-mode {
    width: 100%;
    max-width: 280px;
  }
}
</style>
