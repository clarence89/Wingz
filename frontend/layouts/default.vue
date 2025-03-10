<template>
  <div class="flex flex-col min-h-screen">
    <!-- Navbar -->
    <nav class="bg-mmwgh p-4 text-white">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-semibold">{{appName}}</h1>
        <!-- Hamburger menu for mobile -->

        <button @click="toggleMobileMenu" class="lg:hidden">
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16m-7 6h7"
            ></path>
          </svg>
        </button>
        <!-- Navigation links for desktop -->
        <div class="hidden lg:flex space-x-4">
          <NuxtLink
            v-if="colorMode.preference == 'light'"
            @click="colorMode.preference = 'dark'"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z"
              />
            </svg>
          </NuxtLink>
          <NuxtLink
            v-if="colorMode.preference == 'dark'"
            @click="colorMode.preference = 'light'"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"
              />
            </svg>
          </NuxtLink>
          <NuxtLink v-if="!authenticated" to="/" class="text-white"
            >Login</NuxtLink
          >
          <!-- <NuxtLink v-if="authenticated()" to="/dashboard" class="text-white">Dashboard</NuxtLink>
          <NuxtLink v-if="authenticated()" to="/contact" class="text-white">Contact</NuxtLink> -->
          <NuxtLink
            v-if="authenticated"
            @click="handleLogout()"
            class="text-white"
            >Logout</NuxtLink
          >
        </div>
      </div>
    </nav>

    <!-- Mobile navigation menu -->
    <div v-if="isMobileMenuOpen" class="lg:hidden">
      <div class="bg-gray-800 p-4">
        <NuxtLink
          v-if="colorMode.preference == 'light'"
          @click="colorMode.preference = 'dark'"
          class="block text-white mb-2"
          ><svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z"
            />
          </svg>
        </NuxtLink>
        <NuxtLink
          v-if="colorMode.preference == 'dark'"
          @click="colorMode.preference = 'light'"
          class="block text-white mb-2"
          ><svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"
            />
          </svg>
        </NuxtLink>
        <NuxtLink v-if="!authenticated" to="/" class="text-white"
          >Login</NuxtLink
        >
        <!-- <NuxtLink v-if="authenticated()" to="/dashboard" class="block text-white mb-2"
          >Dashboard</NuxtLink
        >
        <NuxtLink v-if="authenticated()" to="/contact" class="block text-white">Contact</NuxtLink> -->
        <NuxtLink
          v-if="authenticated"
          @click="handleLogout()"
          class="text-white"
          >Logout</NuxtLink
        >
      </div>
    </div>

    <!-- Main content -->
    <main class="container mx-auto mt-6 mb-6 flex-1">
      <slot />
    </main>

    <!-- Sticky bottom footer -->
    <footer class="bg-mmwgh p-4 text-white">
      <div class="container mx-auto">
        <p>&copy; 2023 My Nuxt App. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";

const appConfig = useAppConfig();
const colorMode = useColorMode();
const store = useAuthStore();
const config = useRuntimeConfig();
const isMobileMenuOpen = ref(false);
const appName = config.public.appName;
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const handleLogout = () => {
  store.logout();
};

const authenticated = computed(() => {
  return store.isAuthenticated;
});
onMounted(() => {
  const handleKeyPress = (event) => {
    if (event.ctrlKey && event.shiftKey && event.altKey && event.key === "F1") {
      revealName();
    }
  };

  window.addEventListener("keydown", handleKeyPress);

  const revealName = () => {
    alert("Creator/Developer: Clarence Advincula Baluyot");
  };
});

</script>
