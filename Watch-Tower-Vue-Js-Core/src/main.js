import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// Surface unexpected render errors instead of leaving a blank page.
function showFatalError(error) {
  console.error(error)
  if (!import.meta.env.DEV) return

  const box = document.createElement('pre')
  box.style.cssText =
    'position:fixed;inset:16px;z-index:99999;overflow:auto;margin:0;padding:16px;border:1px solid #f87171;border-radius:12px;background:#0b0f14;color:#fca5a5;font:12px/1.6 monospace;white-space:pre-wrap'
  box.textContent = `Watch Tower failed to start\n\n${error?.stack || error}`
  document.body.appendChild(box)
}

app.config.errorHandler = (error) => showFatalError(error)

window.addEventListener('error', (event) => {
  if (event?.error) showFatalError(event.error)
})

try {
  app.use(router)
  app.mount('#app')
} catch (error) {
  showFatalError(error)
}
