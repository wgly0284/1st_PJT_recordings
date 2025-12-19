
import { createApp } from 'vue'
import { createPinia } from 'pinia' // Pinia import
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth' // Auth store import

// Tailwind CDN (전역 설정)
const tailwindScript = document.createElement('script')
tailwindScript.src = 'https://cdn.tailwindcss.com'
tailwindScript.onload = () => {
  window.tailwind.config = {
    theme: {
      extend: {
        colors: {
          cream: { 50: '#FFFEFA', 100: '#F9F7F2', 200: '#F0EBE0' },
          teal: { 800: '#1D4E45', 900: '#12352E' },
          brown: { text: '#4A4036' }
        },
        fontFamily: {
          sans: ['Noto Sans KR', 'sans-serif'],
          serif: ['Playfair Display', 'serif']
        },
        boxShadow: {
          'soft': '0 30px 60px -15px rgba(29, 78, 69, 0.15)',
          'glow': '0 0 20px rgba(255, 255, 255, 0.5)'
        },
        animation: {
          'float': 'float 6s ease-in-out infinite',
          'scroll-down': 'scrollDown 2s infinite'
        },
        keyframes: {
          float: {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-10px)' }
          },
          scrollDown: {
            '0%': { transform: 'translateY(0)', opacity: '1' },
            '100%': { transform: 'translateY(10px)', opacity: '0' }
          }
        }
      }
    }
  }
}
document.head.appendChild(tailwindScript)

// Lucide Icons
const lucideScript = document.createElement('script')
lucideScript.src = 'https://unpkg.com/lucide@latest'
document.head.appendChild(lucideScript)

const app = createApp(App)
const pinia = createPinia() // Pinia 인스턴스 생성

app.use(pinia) // 앱에 Pinia 등록

// Pinia 스토어가 라우터 인스턴스를 사용할 수 있도록 설정
// app.use(router)보다 먼저 실행되어야 함
const authStore = useAuthStore()
authStore.setRouter(router)

app.use(router) // 앱에 라우터 등록
app.mount('#app')
