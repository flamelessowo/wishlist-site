<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { getToastService } from '../core/toast';
import { useUserStore } from '../stores/userstore';
import { SERVER_URI, WISH_PATH } from '../core/constants';
import axios from 'axios';
import ConfettiExplosion from "vue-confetti-explosion";

const confettiRef = ref(null);

const wishes: any = ref([]);
const wishlist: any = ref();
const expandedRows = ref([]);
const toast = getToastService(useToast());
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const dialogVisible = ref(false)
const fetchUrl = ref('');
const visible = ref(false);

const user = ref('')
const users = ref([])


async function getWishes() {
  if (!userStore.isAuthenticated) {
    toast.error('Authorize to see your wishlist');
    router.push({name: 'auth'})
  }
  const response = await axios.get(`${SERVER_URI}${WISH_PATH}${route.params.wishlistslug}`);
  wishlist.value = response.data.wishlist
  wishes.value = response.data.wishes
}

const explode = () => {
  visible.value = true
};

async function fetchRozetka() {
  await axios.post(`${SERVER_URI}api/fetch/`, {uri: fetchUrl.value, wishlist_id: wishlist.value.id});
  toast.success('Successfully added item to your list');
  dialogVisible.value = false;
  fetchUrl.value = '';
  await getWishes();
}

onMounted(async () => {
    if (!userStore.isAuthenticated) {
    toast.error('Authorize to see wishlists');
    router.push({name: 'auth'})
  }
  await getWishes();
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

async function toggleWishBought(id: string, bought: boolean) {
  await axios.put(`${SERVER_URI}api/wish/update`, {id: id, bought: bought});
  await getWishes();
  if (wishes.value.every(el => el.bought))
    explode()
}

async function deleteWish(id: string) {
  await axios.delete(`${SERVER_URI}api/wish/delete/`+id);
  toast.success('Successfully deleted wish');
  await getWishes();
}

function redirectToRozetka(link) {
  window.open(link, '_blank');
}

</script>
<template>
    <ConfettiExplosion v-if="visible" :particleCount="300" :force="0.5" />
  <DataTable v-model:expandedRows="expandedRows" :value="wishes" dataKey="id"
        @rowExpand="onRowExpand" @rowCollapse="onRowCollapse" tableStyle="min-width: 60rem">
    <template #header>
        <div style="position: relative;" class="flex flex-wrap justify-content-end gap-2">
        <AvatarGroup>
    <Avatar image="/images/avatar/amyelsner.png" size="large" shape="circle" />
    <Avatar image="/images/avatar/asiyajavayant.png" size="large" shape="circle" />
    <Avatar image="/images/avatar/onyamalimba.png" size="large" shape="circle" />
    <Avatar image="/images/avatar/ionibowcher.png" size="large" shape="circle" />
    <Avatar image="/images/avatar/xuxuefeng.png" size="large" shape="circle" />
    <Avatar label="+2" shape="circle" size="large" style="background-color: '#9c27b0', color: '#ffffff'" />
</AvatarGroup>
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
    <Column header="Bought?">
        <template #body="slotProps">
          <Checkbox @change="toggleWishBought(slotProps.data.id, slotProps.data.bought)" v-model="slotProps.data.bought" :binary="true" />
        </template>
    </Column>
    <template #expansion="slotProps">
      <div class="p-3">
        <Button @click="redirectToRozetka(slotProps.data.link)" label="Link to buy" link />
        <Button label="Delete" severity="danger" @click="deleteWish(slotProps.data.id)"/>
      </div>
    </template>
  </DataTable>
  <Button label="Add wish" @click="dialogVisible = !dialogVisible" size="large" class="add-button" icon="pi pi-plus" severity="success" rounded aria-label="Search" />
  <Dialog v-model:visible="dialogVisible" modal :style="{ width: '50vw' }">
    <div style="display: flex; flex-direction: column;">
      <InputText @keyup.enter="fetchRozetka" class="field" placeholder="Rozetka Item URL" type="text" v-model="fetchUrl" />
    </div>
  </Dialog>
 </template>
<style>
.add-button {
  position: absolute;
  bottom: 0;
  right: 0;
  margin-bottom: 10px;
  margin-right: 10px;
}
</style>
