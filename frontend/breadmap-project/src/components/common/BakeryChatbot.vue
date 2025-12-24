<template>
  <!-- 플로팅 버튼 -->
  <div class="fixed bottom-6 right-6 z-50">
    <!-- 채팅 창 (열려있을 때) -->
    <Transition name="chat">
      <div
        v-if="isOpen"
        class="bg-white rounded-2xl shadow-2xl w-96 h-[600px] mb-4 flex flex-col overflow-hidden border-2 border-orange-100"
      >
        <!-- 헤더 -->
        <div class="bg-gradient-to-r from-[#F3B37A] to-[#C99768] p-4 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center overflow-hidden">
               <!-- 헤더 로고 -->
               <img src="@/assets/images/logo.png" alt="Logo" class="w-8 h-8 object-contain" />
            </div>
            <div>
              <h3 class="font-jua text-white text-lg">갓 구운 빵집 추천봇</h3>
              <p class="text-xs text-white/80">당신만의 빵집을 찾아드려요!</p>
            </div>
          </div>
          <button @click="closeChat" class="text-white hover:bg-white/20 rounded-full p-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Step 1: 지역 선택 -->
        <div v-if="step === 'location'" class="flex-1 flex flex-col justify-center p-6 space-y-4 bg-gradient-to-b from-[#FFF9F0] to-white">
          <div class="text-center space-y-2">
            <div class="w-16 h-16 bg-[#FFF3DD] rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">📍</span>
            </div>
            <h2 class="text-xl font-jua text-[#6B4A38]">어디에 계신가요?</h2>
            <p class="text-sm text-[#8B6A55]">빵집을 찾고 싶은 지역을 선택해주세요</p>
          </div>

          <select
            v-model="location"
            class="w-full p-3 border-2 border-[#FFE8CC] rounded-xl text-base focus:ring-2 focus:ring-[#F3B37A] outline-none font-jua"
          >
            <option value="" disabled>지역을 선택해주세요</option>
            <option v-for="loc in LOCATIONS" :key="loc" :value="loc">{{ loc }}</option>
          </select>

          <button
            @click="location && (step = 'preference')"
            :disabled="!location"
            class="w-full py-3 rounded-xl font-jua text-white transition-all"
            :class="location ? 'bg-[#F3B37A] hover:bg-[#C99768] shadow-md' : 'bg-gray-300 cursor-not-allowed'"
          >
            다음 단계
          </button>
        </div>

        <!-- Step 2: 취향 선택 -->
        <div v-if="step === 'preference'" class="flex-1 flex flex-col justify-center p-6 space-y-4 bg-gradient-to-b from-[#FFF9F0] to-white">
          <div class="text-center space-y-2">
            <div class="w-16 h-16 bg-[#FFF3DD] rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">💖</span>
            </div>
            <h2 class="text-xl font-jua text-[#6B4A38]">어떤 빵을 좋아하세요?</h2>
            <p class="text-sm text-[#8B6A55]">오늘 가장 먹고 싶은 스타일을 골라주세요</p>
          </div>

          <div class="space-y-2 max-h-60 overflow-y-auto pr-2">
            <button
              v-for="pref in PREFERENCES"
              :key="pref.id"
              @click="preference = pref.id"
              class="w-full p-3 rounded-xl text-left border-2 transition-all duration-200 font-jua text-sm"
              :class="preference === pref.id
                ? 'border-[#F3B37A] bg-[#FFF3DD] text-[#C99768] font-bold shadow-sm'
                : 'border-[#FFE8CC] hover:border-[#F3B37A] hover:bg-[#FFF9F0]'"
            >
              {{ pref.label }}
            </button>
          </div>

          <button
            @click="startChat"
            :disabled="!preference"
            class="w-full py-3 rounded-xl font-jua text-white transition-all"
            :class="preference ? 'bg-[#F3B37A] hover:bg-[#C99768] shadow-md' : 'bg-gray-300 cursor-not-allowed'"
          >
            맛집 추천 받기
          </button>
        </div>

        <!-- Step 3: 채팅 화면 -->
        <div v-if="step === 'chat'" class="flex-1 flex flex-col h-full">
          <!-- 상단 정보 바 -->
          <div class="bg-[#FFF3DD] px-4 py-2 text-xs text-[#C99768] flex justify-between items-center border-b border-[#FFE8CC] font-jua">
            <span>📍 {{ location }}</span>
            <span>🍞 {{ PREFERENCES.find(p => p.id === preference)?.label.split(' ')[1] }}</span>
            <button
              @click="resetChat"
              class="text-[#8B6A55] underline hover:text-[#C99768]"
            >
              다시 설정
            </button>
          </div>

          <!-- 메시지 리스트 -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3 bg-[#FFF9F0]">
            <div v-if="messages.length === 0 && !isLoading" class="text-center text-[#C99768] mt-10">
              <p class="font-jua">AI가 맞춤 빵집을 찾고 있습니다...</p>
            </div>

            <div
              v-for="(msg, idx) in messages"
              :key="idx"
              class="flex"
              :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm whitespace-pre-wrap font-jua"
                :class="msg.role === 'user'
                  ? 'bg-[#F3B37A] text-white rounded-tr-none'
                  : 'bg-white text-[#6B4A38] border border-[#FFE8CC] rounded-tl-none'"
              >
                {{ msg.content }}
              </div>
            </div>

            <div v-if="isLoading" class="flex justify-start">
              <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-[#FFE8CC] shadow-sm flex items-center space-x-2">
                <div class="w-4 h-4 border-2 border-[#F3B37A] border-t-transparent rounded-full animate-spin"></div>
                <span class="text-sm text-[#8B6A55] font-jua">열심히 빵 굽는 중...</span>
              </div>
            </div>
          </div>

          <!-- 입력창 -->
          <form @submit.prevent="handleSendMessage" class="p-3 bg-white border-t border-[#FFE8CC] flex gap-2">
            <input
              v-model="input"
              type="text"
              placeholder="추가로 궁금한 점을 물어보세요..."
              class="flex-1 p-2 border-2 border-[#FFE8CC] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#F3B37A] bg-[#FFF9F0] font-jua text-sm"
              :disabled="isLoading"
            />
            <button
              type="submit"
              :disabled="!input.trim() || isLoading"
              class="bg-[#F3B37A] text-white p-2 rounded-xl hover:bg-[#C99768] disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </Transition>

    <!-- 플로팅 버튼 (수정됨: 배경 제거, 로고 풀 채움, 크기 확대) -->
    <button
      @click="toggleChat"
      class="w-20 h-20 bg-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-all duration-300 overflow-hidden"
      :class="isOpen ? 'rotate-0' : 'animate-bounce'"
    >
      <img 
        v-if="!isOpen" 
        src="@/assets/images/logo.png" 
        alt="Chatbot Logo" 
        class="w-full h-full object-cover" 
      />
      
      <svg v-else class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- 뱃지 -->
    <div v-if="!isOpen && hasNewMessage" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full border-2 border-white animate-pulse"></div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

// 상태 관리
const isOpen = ref(false);
const step = ref('location'); // location 부터 시작
const location = ref('');
const preference = ref('');
const messages = ref([]);
const input = ref('');
const isLoading = ref(false);
const hasNewMessage = ref(false);
const messagesContainer = ref(null);

// 상수 데이터
const LOCATIONS = [
  "서울 강남구", "서울 성수동", "서울 연남동", "서울 한남동",
  "경기 분당", "경기 수원",
  "부산 해운대", "부산 전포동",
  "대구 동성로", "대전 성심당 인근", "광주 동명동",
  "제주도"
];

const PREFERENCES = [
  { id: 'hard', label: '🥖 겉바속촉 하드계열 (바게트/깜빠뉴)' },
  { id: 'sweet', label: '🍰 달콤한 디저트/케이크' },
  { id: 'trendy', label: '🍩 요즘 핫한 베이글/도넛/소금빵' },
  { id: 'vegan', label: '🥗 건강한 비건/쌀빵' },
  { id: 'date', label: '☕ 분위기 좋은 데이트 코스' },
];

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 백엔드(Django) 호출 함수 (URL 수정 포함)
const callOpenAI = async (currentMessages) => {
  isLoading.value = true;
  try {
    // Django urls.py 설정에 맞춘 경로 (stores/chatbot/)
    const response = await fetch("http://localhost:8000/stores/chatbot/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: currentMessages
      })
    });

    if (!response.ok) {
      throw new Error(`Server Error: ${response.status}`);
    }

    const data = await response.json();
    // Django 응답 구조 (role, content)에 맞춰 데이터 추출
    const botReply = data.content || data.choices?.[0]?.message?.content;

    messages.value.push({ role: 'assistant', content: botReply });
    
    if (!isOpen.value) {
      hasNewMessage.value = true;
    }
    scrollToBottom();
  } catch (error) {
    console.error("Error calling Backend:", error);
    messages.value.push({
      role: 'assistant',
      content: "죄송합니다. 서버와 통신 중 오류가 발생했습니다. (URL 및 서버 상태를 확인해주세요)"
    });
    scrollToBottom();
  } finally {
    isLoading.value = false;
  }
};

const startChat = () => {
  if (!location.value || !preference.value) return;

  step.value = 'chat';

  const initialSystemMessage = {
    role: 'system',
    content: `당신은 20년 경력의 빵집 전문 큐레이터 '브레드 봇'입니다.
    사용자는 현재 '${location.value}' 지역에 있으며, '${preference.value}' 스타일의 빵집을 찾고 있습니다.
    
    [지침]
    1. 항상 친절하고 전문적인 말투(해요체)를 사용하세요.
    2. 빵집 이름, 대표 메뉴, 그리고 추천 이유를 명확히 설명하세요.
    3. 정보가 불확실하면 추천하지 말고, 확실한 곳만 추천하세요.
    4. 이모티콘을 적절히 사용하여 가독성을 높이세요.`
  };

  const welcomeUserMessage = {
    role: 'user',
    content: `안녕! 나는 ${location.value}에 있고, ${PREFERENCES.find(p=>p.id === preference.value)?.label} 스타일을 좋아해. 추천해줄 만한 곳이 있어?`
  };

  const initialMessages = [initialSystemMessage, welcomeUserMessage];
  messages.value = [{
    role: 'user',
    content: `지역: ${location.value}, 취향: ${PREFERENCES.find(p=>p.id === preference.value)?.label} 선택 완료!`
  }];

  callOpenAI(initialMessages);
};

const handleSendMessage = () => {
  if (!input.value.trim() || isLoading.value) return;

  const userMsg = { role: 'user', content: input.value };
  messages.value.push(userMsg);

  const userInput = input.value;
  input.value = '';

  const apiMessages = [
    {
      role: 'system',
      content: `사용자는 '${location.value}' 지역, '${preference.value}' 취향입니다. 이 맥락을 유지하며 답변하세요.`
    },
    ...messages.value.filter(m => m.role !== 'system'),
  ];

  scrollToBottom();
  callOpenAI(apiMessages);
};

const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    hasNewMessage.value = false;
    scrollToBottom();
  }
};

const closeChat = () => {
  isOpen.value = false;
};

const resetChat = () => {
  step.value = 'location';
  messages.value = [];
  location.value = '';
  preference.value = '';
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

/* 채팅창 애니메이션 */
.chat-enter-active,
.chat-leave-active {
  transition: all 0.3s ease;
}

.chat-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.chat-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

/* 스크롤바 스타일 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #FFF9F0;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #F3B37A;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #C99768;
}
</style>