<script setup lang="ts">
import { useUserStore } from '@/stores/userstore';
import { onMounted, ref } from 'vue';
import { post, get } from '@/core/httpservice';
import { SERVER_URI, USER_PROFILE_PATH } from '@/core/constants';
import { useRoute, useRouter } from 'vue-router';
import { getToastService } from '@/core/toast';
import { useToast } from 'primevue/usetoast';

const userstore = useUserStore();
let user = ref();
const route = useRoute();
const router = useRouter();
const toast = getToastService(useToast());

onMounted(async () => {
  try {
      user.value = (await get(USER_PROFILE_PATH + route.params.user)).data;
  } catch(err: any) {
    toast.error('This profile may not exist', 'Profile not found!');
    router.push('/');
  }
})

function redirectToEdit() {
  router.push({name: 'profile-edit', params: {user: userstore.username}})
}
</script>
<template>
  <div class="user-profile">
    <h1>User Profile</h1>
    <Card style="height: 30rem;" class="shadow-8 border-round"> <template #header> <div class="flex flex-row wrap"> <img v-if="user?.photo" width="200" height="200" alt="user header" :src="SERVER_URI + user?.photo.substring(1)" /> <img v-else="user?.photo" width="200" height="200" alt="user header" src="/def_user_image.jpg" /> <div class="flex flex-column info">
            <span>{{ user?.date_joined ? `Date joined: ${(new Date(user?.date_joined)).toLocaleDateString()}` : '' }}</span>
            <span v-if="user?.email">Email: {{ user?.email }}</span>
            <span v-if="user?.birth_date">{{ `Birth date: ${(new Date(user?.birth_date)).toLocaleDateString()}`}}</span>
        </div>
      </div>
        
    </template>
    <template #title> {{ user?.username }} </template>
    <template #subtitle><span v-if="user?.first_name">{{ user?.first_name }}</span>&nbsp;<span v-if="user?.last_name">{{ user?.last_name }}</span></template>
    <template #content>
      <div>
         {{ user?.description ? user?.description : `We don't know much about ${user?.username}. But we sure he's a good person.` }}
      </div>
    </template>
    <template #footer>
        <Button @click="redirectToEdit" v-if="user?.username == userstore.username" icon="pi pi-check" label="Edit" />
    </template>
</Card>
  </div>
</template>
<style scoped>
img {
  border: 5px solid #555;
}
.user-profile {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.info span {
  margin-left: 5px;
  margin-top: 5px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
  font-size: 16px;
}
</style>
