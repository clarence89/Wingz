<!-- components/LoginComponent.vue -->
<template>
  <div class="h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded shadow-md w-96">
      <h2 class="text-2xl font-semibold mb-4">Login</h2>
      <!-- Login Form -->
      <form @submit.prevent="handleLogin()">
        <div class="mb-4">
          <label for="username" class="block text-gray-600 text-sm font-medium"
            >Username</label
          >
          <input
            v-model="username"
            type="text"
            id="username"
            name="username"
            class="mt-1 p-2 w-full border border-gray-300 rounded"
          />
        </div>

        <div class="mb-4">
          <label for="password" class="block text-gray-600 text-sm font-medium"
            >Password</label
          >
          <input
            v-model="password"
            type="password"
            id="password"
            name="password"
            class="mt-1 p-2 w-full border border-gray-300 rounded"
          />
        </div>
        <p class="text-red-900 my-3">{{ err_message }}</p>
        <button type="submit" class="bg-blue-500 text-white p-2 rounded w-full">
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "~/stores/auth";

const store = useAuthStore();

const username = ref("");
const password = ref("");
var err_message = null;
const isAuthenticated = computed(() => store.isAuthenticated);

const handleLogin = async () => {
  err_message = null;
  const login = await store.login({
    username: username.value,
    password: password.value,
  });
  password.value = "";
  if (login && login.status !== undefined) {
    if (!login.status) {
      err_message = login.message;
    }
  }
};

const handleLogout = () => {
  store.logout();
};
</script>
