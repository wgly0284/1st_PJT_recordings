<template>
  <div class="bg-white rounded-[2.5rem] shadow-soft p-8 md:p-16 border border-gray-100" v-scroll>
    <div class="flex flex-col md:flex-row gap-12 items-center md:items-start">
      <!-- Profile Left -->
      <div class="md:w-1/3 flex flex-col items-center text-center">
        <div class="relative w-40 h-40 mb-6 group">
          <div class="absolute inset-0 bg-teal-800 rounded-full opacity-0 group-hover:opacity-10 transition-opacity"></div>
          
          <!-- Profile Image or Default Icon -->
          <img v-if="authStore.currentUser?.profile_image_url" :src="authStore.currentUser.profile_image_url" class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg object-cover">
          <div v-else class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg bg-gray-200 flex items-center justify-center text-5xl">
            🥖
          </div>
          
          <button class="absolute bottom-0 right-0 w-10 h-10 bg-teal-800 text-white rounded-full flex items-center justify-center border-4 border-white">
            <i data-lucide="camera" class="w-4 h-4"></i>
          </button>
        </div>
        <h2 class="text-3xl font-bold text-teal-900 mb-1">{{ authStore.currentUser?.nickname || 'Guest' }}</h2>
        <p class="text-gray-400 mb-8">{{ authStore.currentUser?.email || 'Not logged in' }}</p>
        <router-link :to="{ name: 'editprofile' }" class="w-full py-4 border-2 border-gray-100 rounded-2xl font-bold text-gray-600 hover:bg-teal-50 hover:border-teal-100 hover:text-teal-800 transition-colors text-center">
          Edit Profile
        </router-link>
      </div>
      
      <!-- Stats Right -->
      <div class="flex-1 w-full space-y-10">
        <!-- Bread Preferences -->
        <div v-if="authStore.currentUser?.bread_preferences" class="bg-[#F9F7F2] p-8 rounded-[2rem]">
          <p class="text-xs font-bold text-orange-600 uppercase tracking-widest mb-1">My Bread Preferences</p>
          <div class="flex flex-wrap gap-2">
            <span v-for="pref in authStore.currentUser.bread_preferences.split(',')" :key="pref" class="px-3 py-1 bg-teal-800 text-white text-sm rounded-full">
              {{ pref }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <router-link :to="{ name: 'myreview' }" class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all cursor-pointer block">
            <div class="text-3xl font-bold text-teal-900 mb-1">{{ userReviews.length }}</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Reviews</div>
          </router-link>
          <div class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all">
            <div class="text-3xl font-bold text-teal-900 mb-1">{{ userBookmarks.length }}</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Bookmarks</div>
          </div>
          <div class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all">
            <div class="text-3xl font-bold text-teal-900 mb-1">8</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Badges</div>
          </div>
        </div>

        <!-- User Reviews Section -->
        <div>
          <h4 class="font-bold text-teal-900 mb-6 text-lg">My Reviews</h4>
          <div v-if="userReviews.length > 0" class="space-y-4">
            <div v-for="review in userReviews" :key="review.id" class="p-4 bg-cream-50 rounded-lg shadow-sm">
              <p class="font-semibold text-teal-800">{{ review.store.name }}</p>
              <p class="text-gray-700 text-sm">{{ review.content }}</p>
              <div class="text-yellow-500 text-sm">Rating: {{ review.rating }} / 5</div>
            </div>
          </div>
          <p v-else class="text-gray-500">아직 작성한 리뷰가 없습니다.</p>
        </div>

        <!-- User Bookmarks Section -->
        <div>
          <h4 class="font-bold text-teal-900 mb-6 text-lg">My Bookmarks</h4>
          <div v-if="userBookmarks.length > 0" class="space-y-4">
            <div v-for="bookmark in userBookmarks" :key="bookmark.id" class="p-4 bg-cream-50 rounded-lg shadow-sm">
              <p class="font-semibold text-teal-800">{{ bookmark.name }}</p>
              <p class="text-gray-700 text-sm">{{ bookmark.address }}</p>
            </div>
          </div>
          <p v-else class="text-gray-500">아직 북마크한 가게가 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/api/axios'; // apiClient import

const authStore = useAuthStore();
const userReviews = ref([]);
const userBookmarks = ref([]);

onMounted(async () => {
  if (authStore.isAuthenticated) {
    // Fetch user reviews
    try {
      const reviewsResponse = await apiClient.get('/reviews/my/');
      userReviews.value = reviewsResponse.data;
    } catch (error) {
      console.error('Failed to fetch user reviews:', error);
    }

    // Fetch user bookmarks
    try {
      const bookmarksResponse = await apiClient.get('/stores/my_bookmarks/');
      userBookmarks.value = bookmarksResponse.data;
    } catch (error) {
      console.error('Failed to fetch user bookmarks:', error);
    }
  }
});
</script>