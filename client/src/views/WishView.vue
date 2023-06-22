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
const dialogVisible = ref(false);
const usersDialogVisible = ref(false);
const fetchUrl = ref('');
const visible = ref(false);

const user = ref('')
const users = ref([])
const profiles = ref([])
const sharedUsers = ref([])


async function getWishes() {
  if (!userStore.isAuthenticated) {
    toast.error('Authorize to see your wishlist');
    router.push({name: 'auth'})
  }
  const response = await axios.get(`${SERVER_URI}${WISH_PATH}${route.params.wishlistslug}`);
  wishlist.value = response.data.wishlist
  wishes.value = response.data.wishes
}

async function getUsers() {
  const response = await axios.get(`${SERVER_URI}users/all`);
  const usersToPush = [];
  response.data.forEach(el => usersToPush.push({name: el.username, code: el.id}))
  users.value = usersToPush;
}

async function getProfiles() {
  const response = await axios.get(`${SERVER_URI}users/profiles`);
  profiles.value = response.data;
}

function getSharedUsers() {
    sharedUsers.value = wishlist.value.shared_with.map(id => {
    const profile = profiles.value.find(el => el.id === id);
    const user = users.value.find(el => el.code === profile.owner);
    return {username: user.name, id: user.code, profile_id: profile.id, photo: profile.photo}
  })
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

function filterUsers() {
  users.value = users.value.filter(el => !sharedUsers.value.map(el => el.id).includes(el.code) && !(userStore.username === el.name))
}

async function reload() {
  await getWishes();
  await getProfiles();
  await getUsers();
  getSharedUsers();
  filterUsers();

}

onMounted(async () => {
  if (!userStore.isAuthenticated) {
    toast.error('Authorize to see wishlists');
    router.push({name: 'auth'})
  }
  await reload();
});

async function removeUserFromList(profile_id, list_id) {
  await axios.delete(`${SERVER_URI}api/wishlists/remove/${profile_id}/${list_id}`);
  await reload();
  toast.success('Removed user from list')
}

async function addToUserList() {
  const profile_id = profiles.value.find(el => el.owner === user.value.code).id;
  await axios.post(`${SERVER_URI}api/wishlists/add/${profile_id}/${wishlist.value.id}`)
  await reload();
  toast.success('Successfully shared list with user');

}

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
          <Avatar v-if="userStore.username === route.params.username" @click="usersDialogVisible = !usersDialogVisible" shape="circle" icon="pi pi-user" class="mr-2" size="large" />
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
        <Button v-if="userStore.username === route.params.username" label="Delete" severity="danger" @click="deleteWish(slotProps.data.id)"/>
      </div>
    </template>
  </DataTable>
  <Button v-if="userStore.username === route.params.username" label="Add wish" @click="dialogVisible = !dialogVisible" size="large" class="add-button" icon="pi pi-plus" severity="success" rounded aria-label="Search" />
  <Dialog v-model:visible="dialogVisible" modal :style="{ width: '50vw' }">
    <div style="display: flex; flex-direction: column;">
      <InputText @keyup.enter="fetchRozetka" class="field" placeholder="Rozetka Item URL" type="text" v-model="fetchUrl" />
    </div>
  </Dialog>
  <Dialog v-model:visible="usersDialogVisible" modal :style="{ width: '50vw' }">
    <div class="flex justify-content-start">
      <Chip v-for="user in sharedUsers" @remove="removeUserFromList(user.profile_id, wishlist.id)" :key="user.id" :label="user.username" :image="user.photo" removable />
    </div>
    <h1 class="flex justify-content-center">Add Users</h1>
    <div style="display: flex; flex-direction: column;">
      <div class="card flex justify-content-center">
        <Listbox @change="addToUserList" v-model="user" :options="users" filter optionLabel="name" class="w-full md:w-30rem">
          <template #option="slotProps">
            <div class="flex align-items-center">
              <div>{{ slotProps.option.name }}</div>
            </div>
          </template>
        </Listbox>
      </div>
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
