<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { getToastService } from '../core/toast';
import { useUserStore } from '../stores/userstore';
import { SERVER_URI, WISH_PATH } from '../core/constants';
import axios from 'axios';

const wishes: any = ref([]);
const wishlist: any = ref();
const expandedRows = ref([]);
const toast = getToastService(useToast());
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

async function getWishes() {
  if (!userStore.isAuthenticated) {
    toast.error('Authorize to see your wishlist');
    router.push({name: 'auth'})
  }
  const response = await axios.get(`${SERVER_URI}${WISH_PATH}${route.params.wishlistslug}`);
  wishlist.value = response.data.wishlist
  wishes.value = response.data.wishes
}

async function fetchHotline(page_url: string) {

}

onMounted(async () => {
    if (!userStore.isAuthenticated) {
    toast.error('Authorize to see wishlists');
    router.push({name: 'auth'})
  }
  await getWishes();
  fetchHotline(1);
});

const onRowExpand = (event) => {
};
const onRowCollapse = (event) => {
};
const expandAll = () => {
    expandedRows.value = wishes.value.filter((p) => p.id);
};
const collapseAll = () => {
    expandedRows.value = null;
};

</script>
<template>
  <DataTable v-model:expandedRows="expandedRows" :value="wishes" dataKey="id"
        @rowExpand="onRowExpand" @rowCollapse="onRowCollapse" tableStyle="min-width: 60rem">
    <template #header>
        <div class="flex flex-wrap justify-content-end gap-2">
            <Button text icon="pi pi-plus" label="Expand All" @click="expandAll" />
            <Button text icon="pi pi-minus" label="Collapse All" @click="collapseAll" />
        </div>
    </template>
    <Column expander style="width: 5rem" />
    <Column field="name" header="Name"></Column>
    <Column header="Image">
        <template #body="slotProps">
            <img :src="slotProps.data.image_link" :alt="slotProps.data.image" class="shadow-4" width="64" />
        </template>
    </Column>
    <Column field="price" header="Price">
        <template #body="slotProps">
          {{ slotProps.data.price + '₴'}}
        </template>
    </Column>
    <Column field="category" header=""></Column>
    <Column field="rating" header="Description">
        <template #body="slotProps">
          {{ slotProps.data.description }}
        </template>
    </Column>
    <Column header="Quantity">
        <template #body="slotProps">
          {{ slotProps.data.quantity }}
        </template>
    </Column>
    <template #expansion="slotProps">
      <form @submit.prevent="onSubmit">
        <div class="flex justify-content-center p-fluid user-profile">
          <div v-focustrap class="card">
            <div class="field">
              <InputText id="input" type="text" autofocus />
            </div>
            <div class="field">
              <InputText id="input" type="text" autofocus />
            </div>
            <div class="field">
              <div class="p-input-icon-right">
                <i class="pi pi-envelope" />
                <InputText id="email" type="email" />
              </div>
            </div>
            <Button type="submit" label="Update Wish" class="mt-2" />
          </div>
        </div>
      </form>
    </template>
  </DataTable>
 </template>
