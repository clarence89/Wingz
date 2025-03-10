export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = await useAuthStore();
  if (!authStore.user_data) {
    await authStore.getTokens();
  }
  if (!authStore.isAuthenticated && to.fullPath != "/") {
    return navigateTo("/");
  } else if (authStore.isAuthenticated && to.fullPath == "/") {
    return navigateTo("/dashboard");
  }
});
