<template>
  <div>
    <div class="grid grid-cols-3 gap-4 my-4">
      <div class="flex flex-col">
        <label for="email" class="text-gray-600 text-sm font-medium">Rider Email</label>
        <UInput id="email" v-model="state.filters.email" placeholder="Email" />
      </div>
      <div class="flex flex-col">
        <label for="latitude" class="text-gray-600 text-sm font-medium">Pickup Latitude</label>
        <UInput id="latitude" v-model="state.filters.latitude" type="number" placeholder="Latitude" />
      </div>
      <div class="flex flex-col">
        <label for="longitude" class="text-gray-600 text-sm font-medium">Pickup Longitude</label>
        <UInput id="longitude" v-model="state.filters.longitude" type="number" placeholder="Longitude" />
      </div>
    </div>
    <div class="flex items-center justify-center my-4">
      <UButton
        class="bg-blue-500 hover:bg-blue-700"
        @click="fetchPageData()"
      >Search</UButton>
    </div>
    
    <UTable :columns="columns" :rows="state.paginationData.results" >
      <template #status-data="{ row }">
          <p>{{ row.status.charAt(0).toUpperCase() + row.status.slice(1) }}</p>
        </template>
      <template #pickup-data="{ row }">
        <!-- Can Add modal for a Map -->
          <p>({{ row.pickup_latitude }}, {{ row.pickup_longitude }})</p>
        </template>
      <template #dropoff-data="{ row }">
                <!-- Can Add modal for a Map -->
          <p>({{ row.dropoff_latitude }}, {{ row.dropoff_longitude }})</p>
        </template>
      <template #rider-data="{ row }">
          <p>{{ row.rider.first_name ? row.rider.first_name + " " + row.rider.last_name  : row.rider.email }}</p>
        </template>
      <template #driver-data="{ row }">
          <p>{{ row.rider.first_name ? row.rider.first_name + " " + row.rider.last_name  : row.rider.email }}</p>
        </template>
      <template #pickup_time-data="{ row }">
          <p>{{ new Intl.DateTimeFormat('en-US', { weekday: 'long', hour: 'numeric', minute: 'numeric', year: 'numeric', month: 'long', day: 'numeric'  }).format(new Date(row.pickup_time)) }}</p>
        </template>
    </UTable>
    <div class="flex items-center justify-center my-4">
      <UButton
        class="bg-blue-500 hover:bg-blue-700"
        :disabled="state.paginationData.previous == null"
        @click="loadData(state.paginationData.previous)"
      >Prev</UButton>

      <p class="px-4">
       Total results: {{ state.paginationData.count }}
      </p>
      <UButton
        class="bg-green-500 hover:bg-green-700"
        :disabled="state.paginationData.next == null"
        @click="loadData(state.paginationData.next)"
      >Next</UButton>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
import { reactive } from "vue";
const columns = [
  { key: "status", label: "Status" },
  { key: "pickup", label: "Pickup Coordinates" },
  { key: "dropoff", label: "Dropoff Coordinates" },
  { key: "rider", label: "Rider" },
  { key: "driver", label: "Driver" },
  { key: "pickup_time", label: "Pickup Time" },
];

const store = useAuthStore();
const state = reactive({
  paginationData: {
    count: 0,
    next: null,
    previous: null,
    results: [],
  },
  filters: {
    email: "",
    latitude: "",
    longitude: "",
  }
})
const config = useRuntimeConfig();
onMounted(() => {
  fetchPageData();
})
const getUrlParams = (url) => {
  let parsed_url = url.replace(config.public.baseURL, "");
  const urlParams = new URLSearchParams();
  if (state.filters.email) urlParams.set("rider_email", state.filters.email);
  if (state.filters.latitude && state.filters.longitude) {
    urlParams.set("latitude", parseFloat(state.filters.latitude));
    urlParams.set("longitude", parseFloat(state.filters.longitude));
  }
  const urls = urlParams.toString() ? `${parsed_url}${parsed_url.includes('?') ? '&' : '?'}${urlParams.toString()}` : parsed_url;
  return urls
}
const fetchPageData = async () => {
  const url = getUrlParams(`/api/rides/`);
  const ridesResponse = await autoFetch(url, {
    method: "GET",
  });
  if (!ridesResponse.ok) {
    const errorText = await ridesResponse.text();
    console.log(`User request failed: ${errorText}`);
  }
  state.paginationData = await ridesResponse.json();
}

const loadData = async (url) => {
  const urls = getUrlParams(url);
  const ridesResponse = await autoFetch(urls, {
    method: "GET",
  });
  if (!ridesResponse.ok) {
    const errorText = await ridesResponse.text();
    console.log(`User request failed: ${errorText}`);
  }
  state.paginationData = await ridesResponse.json();
}

</script>
