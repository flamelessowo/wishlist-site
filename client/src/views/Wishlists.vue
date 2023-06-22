<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useUserStore } from '../stores/userstore'
import WishlistCU from '../components/WishlistCU.vue'
import axios from 'axios'
import { SERVER_URI, WISHLISTS_PATH, WISHLISTS_D_PATH } from '../core/constants';
import { useToast } from 'primevue/usetoast';
import { getToastService } from '@/core/toast';
import { useRoute, useRouter } from 'vue-router';

const userStore = useUserStore();
const chosenObj = ref({} as any);
const toast = getToastService(useToast());
const router = useRouter();
const shareVisible = ref(false);

function enterEditMode(obj: any) {
  chosenObj.value = obj;
  wishListMode.value = 'Edit';
  dialogVisible.value = !dialogVisible.value;
}

function enterAddMode() {
  wishListMode.value = 'Add';
  dialogVisible.value = !dialogVisible.value;
}

async function getWishLists() {
  dialogVisible.value = false;
  const wishLists = await axios(`${SERVER_URI}${WISHLISTS_PATH}${userStore.username}`);
  wishes.value = wishLists.data.reverse();
}

async function getSharedWishLists() {
  const wishLists = await axios.get(`${SERVER_URI}api/wishlists/get_shared_wishlists/${userStore.username}`);
  sharedWishLists.value= wishLists.data;
  console.log(sharedWishLists.value)
}

async function redirectToWish(slug) {
  router.push({name: 'wishview', params: {username: userStore.username, wishlistslug: slug}})

}

function redirectToOtherWishlist(wlslug, username) {
  router.push({name: 'wishview', params: {username, wishlistslug: wlslug}});
}

onMounted(async () => {
  if (!userStore.isAuthenticated) {
    toast.error('Authorize to see wishlists');
    router.push({name: 'auth'})
  }
  await getWishLists();
  await getSharedWishLists();
});

const wishes = ref([]);
const dialogVisible = ref(false);
const wishListMode = ref('Add')
const sharedWishLists = ref([])

async function deleteWishlist(slug: any) {
  await axios.delete(`${SERVER_URI}${WISHLISTS_D_PATH}${slug}`);
  toast.success('Successfully deleted wishlist');
  getWishLists();
}


</script>
<template>
  <div v-if="wishes.length" class="card">
    <DataView :value="wishes" paginator :rows="5">
      <template #list="slotProps">
        <div class="col-12">
          <div class="flex flex-column xl:flex-row xl:align-items-start p-4 gap-4">
            <div class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
              <div class="flex flex-column align-items-center sm:align-items-start gap-3">
                <div class="text-2xl font-bold text-900">{{ slotProps.data.name }}</div>
                {{ slotProps.data.description }}
                <div class="flex align-items-center gap-3">
                  <span class="flex align-items-center gap-2">
                    <i class="pi pi-tag"></i>
                    <span class="font-semibold">{{ slotProps.data.category }}</span>
                  </span>
                  <Tag :value="slotProps.data.inventoryStatus"></Tag>
                </div>
              </div>
              <div class="flex sm:flex-row align-items-center sm:align-items-end gap-3 sm:gap-2">
                <ConfirmPopup class="p-confirm-popup"></ConfirmPopup>
                <Button @click="deleteWishlist(slotProps.data.slug)" title="Delete" severity="danger" icon="pi pi-times" rounded></Button>
                <Button @click="enterEditMode({name: slotProps.data.name, description: slotProps.data.description, slug: slotProps.data.slug})" severity="warning" title="Edit" icon="pi pi-file-edit" rounded></Button>
                <Button @click="redirectToWish(slotProps.data.slug)" title="Wishes" icon="pi pi-list" rounded></Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </div>
  <div v-else>
    Oops nothing here....
  </div>
  <Button label="Add wishlist" @click="enterAddMode" size="large" class="add-button" icon="pi pi-plus" severity="success" rounded aria-label="Search" />
  <Button style="margin-right: 185px;" label="Shared with me" @click="shareVisible = !shareVisible" size="large" class="add-button" icon="pi pi-heart" severity="" rounded aria-label="Search" />
  <Dialog v-model:visible="dialogVisible" modal :style="{ width: '50vw' }">
    <WishlistCU @reload="getWishLists()" :name="chosenObj.name" :description="chosenObj.description" :slug="chosenObj.slug" :mode="wishListMode"/>
  </Dialog>
  <Dialog v-model:visible="shareVisible" modal :style="{ width: '50vw' }">
    <Card v-for="el in sharedWishLists" @click="redirectToOtherWishlist(el.slug, el.username)" :key="el.id">
      <template #title> {{ el.name }} </template>
      <template #content> {{ `Author: ${el.username}` }} </template>
    </Card>
  </Dialog>
</template>
<style scoped>
.add-button {
  position: absolute;
  bottom: 0;
  right: 0;
  margin-bottom: 10px;
  margin-right: 10px;
}

.p-confirm-popup-overlay {
  box-shadow: none !important;
}
</style>
