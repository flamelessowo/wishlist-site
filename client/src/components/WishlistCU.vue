<script setup lang="ts">
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { SERVER_URI, WISHLISTS_CU_PATH } from '../core/constants';
import { useUserStore } from '../stores/userstore'
import { getToastService } from '@/core/toast';
import { useToast } from 'primevue/usetoast';

const userStore = useUserStore()
const toast = getToastService(useToast())

interface WishListEditI {
  name: string;
  description: string | any;
}

async function onSubmit() {
  if (props.mode === 'Edit') {
    await axios.put(`${SERVER_URI}${WISHLISTS_CU_PATH}${userStore.username}`, {name: name.value, description: description.value, slug: props.slug})
    toast.success(`Successfully updated wishlist ${name.value}`);
    emits('reload');
    return;
  }
  await axios.post(`${SERVER_URI}${WISHLISTS_CU_PATH}${userStore.username}`, {name: name.value, description: description.value} as WishListEditI);
  toast.success(`Successfully created wishlist ${name.value}`);
  emits('reload');
}

const name = ref('');
const description = ref('');

const props = defineProps({
  mode: String,
  name: String,
  description: String,
  slug: String
})

onMounted(() => {
  if (props.mode === 'Edit') {
    name.value = props.name;
    description.value = props.description;
  }
})

const emits = defineEmits(['reload']);
</script>
<template>
  <Card>
    <template #title> {{ props.mode }} WishList</template>
    <template #content>
      <form @submit.prevent="onSubmit">
        <div style="display: flex; flex-direction: column;">
          <InputText class="field" placeholder="Input name" type="text" v-model="name" />
          <InputText class="field" placeholder="Input description" type="text" v-model="description"/>
          <Button :label="props.mode" type="submit"/>
        </div>
      </form>
    </template>
  </Card>
</template>

<style scoped>
.field {
  margin-top: 3px;

}
</style>
