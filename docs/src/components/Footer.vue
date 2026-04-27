<script setup>
</script>

<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <div class="footer-brand__name">FakeyPaste</div>
        <div class="footer-brand__ver">v1.2.1</div>
      </div>

      <div class="footer-links">
        <a href="https://www.kaizs.cn" target="_blank" rel="noopener">作者主页</a>
        <a href="https://www.kaizs.cn/fakeypastehelp.html" target="_blank" rel="noopener">在线帮助</a>
        <a href="https://github.com/Kai-Zs/FakeyPaste" target="_blank" rel="noopener">GitHub</a>
      </div>

      <div class="footer-copy">
        © 2026 凯Z闪 (KaiZs) · Powered by Python & CustomTkinter
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 4rem;
  padding: 3rem 0;
  border-top: 1px solid var(--border-glass);
}

.footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.footer-brand__name {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--primary);
}

.footer-brand__ver {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-links a {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.footer-links a:hover {
  color: var(--accent);
}

.footer-copy {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.5rem;
}
</style>
