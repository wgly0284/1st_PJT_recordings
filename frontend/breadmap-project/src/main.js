
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

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
app.use(router)
app.mount('#app')
