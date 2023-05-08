<template>
  <div class="profile-page">
    <h1>Profile Page</h1>
    <div class="form">
      <div class="p-field">
        <label for="name">Name</label>
        <InputText id="name" v-model="user.name" />
      </div>
      <div class="p-field">
        <label for="surname">Surname</label>
        <InputText id="surname" v-model="user.surname" />
      </div>
      <div class="p-field">
        <label for="dob">Date of Birth</label>
        <Calendar id="dob" v-model="user.dateOfBirth" :dateFormat="dateFormat" :inputStyle="{width: '100%'}" />
      </div>
      <div class="p-field">
        <label for="image">Image</label>
        <FileUpload id="image" mode="basic" customUpload @upload="handleImageUpload" />
      </div>
      <div class="p-field">
        <img v-if="user.image" :src="user.image" alt="User Image" class="user-image" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const user = ref({
  name: '',
  surname: '',
  dateOfBirth: null,
  image: null,
});

const dateFormat = 'dd/mm/yy';

const handleImageUpload = (event) => {
  const file = event.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    user.value.image = reader.result;
  };
  reader.readAsDataURL(file);
};
</script>

<style scoped>
.profile-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.form {
  display: flex;
  flex-direction: column;
}

.p-field {
  margin-bottom: 20px;
}

.user-image {
  max-width: 200px;
  margin-top: 10px;
}
</style>