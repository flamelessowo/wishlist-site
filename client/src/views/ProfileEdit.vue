<script setup lang="ts">

interface UserEditI {
  name: string;
  surname: string;
  birthDate: Date | any;
  email: string;
  description: string | any;
  image: string;
  photo: string;
}

import { useUserStore } from '@/stores/userstore';
import { onMounted, ref } from 'vue';
import { SERVER_URI, USER_PROFILE_PATH, UPLOAD_PATH } from '@/core/constants';
import { useRoute, useRouter } from 'vue-router';
import { getToastService } from '@/core/toast';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';

const userstore = useUserStore();
const route = useRoute();
const router = useRouter();
const toast = getToastService(useToast());

const user = ref({} as UserEditI);
const uploadedImg = ref('');
const imgFile = ref();

onMounted(() => {
  user.value.name = userstore.first_name;
  user.value.surname = userstore.last_name;
  user.value.birthDate = userstore.birth_date;
  user.value.email = userstore.email;
  user.value.description = userstore.description;
  user.value.photo = userstore.photo;
})

async function onUpload(event: any) {
  const formData = new FormData();
  formData.append('image', event.target.files[0])
  const response = await axios.post(`${SERVER_URI}${UPLOAD_PATH}${userstore.username}`, formData)
}

async function onSubmit() {
  try {
    await axios.put(`${SERVER_URI}${USER_PROFILE_PATH}${userstore.username}/edit`, {
      name: user.value.name,
      surname: user.value.surname,
      birthDate: new Date(user.value.birthDate).toISOString().split('T')[0],
      email: user.value.email,
      description: user.value.description})
    toast.success('Successfully updated profile');
    router.push({name: 'profile', params: {user: userstore.username}})

  } catch(err: any) {

  }
}

</script>
<template>
  <form @submit.prevent="onSubmit">
    <div class="flex justify-content-center p-fluid user-profile">
      <div v-focustrap class="card">
        <div class="field">
          <Image ref="imgInput" :src="user.photo ? user.photo : '/def-usr-image.jpg'" alt="Image"
            width="250" height="250" />
          <input type="file" @change="onUpload" accept="image/*">
        </div>
        <div class="field">
          <InputText id="input" v-model="user.name" type="text" placeholder="Name" autofocus />
        </div>
        <div class="field">
          <InputText id="input" v-model="user.surname" type="text" placeholder="Surname" autofocus />
        </div>
        <div class="field">
          <Calendar placeholder="Enter birth date" v-model="user.birthDate" />
        </div>
        <div class="field">
          <div class="p-input-icon-right">
            <i class="pi pi-envelope" />
            <InputText id="email" v-model="user.email" type="email" placeholder="Email" />
          </div>
        </div>
        <div class="field">
          <Textarea v-model="user.description" placeholder="Enter description" />
        </div>
        <Button type="submit" label="Update Profile" class="mt-2" />
      </div>
    </div>
  </form>
</template>
<style scoped>
img {
  border: 5px solid #555;
}

.user-profile {
  max-width: 1000px;
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
