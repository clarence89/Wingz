export const autoFetch = async (url: string, options: RequestInit = {}) => {
  const config = useRuntimeConfig();
  const store = await useAuthStore();
  const maxTries = 3; // Set your desired maximum number of tries
  let tries = 0;
  let res;
  var processed_access_token = store.accessToken;
  do {
    const headers = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${processed_access_token}`,
      },
    };
    let processedOptions = {
      ...options,
      ...headers,
    };
    res = await fetch(config.public.baseURL + url, processedOptions);

    if (!res.ok) {
      // If fetch fails, execute store.getTokens() and then retry
      processed_access_token = await store.getTokens();
      tries++;
    }
  } while (!res.ok && tries < maxTries);

  if (!res.ok) {
    console.log(`Failed to fetch ${url} after ${maxTries} retries`);
  }

  return res;
};

export const normalFetch = async (url: string, options: RequestInit = {}) => {
  const config = useRuntimeConfig();
  const res = await fetch(config.public.baseURL + url, options);
  return res;
};

export const windowRedirect = async (url: string) => {
  const config = useRuntimeConfig();
  const redirectUrl = config.public.baseURL + url;
  window.open(redirectUrl, "_blank");
};
