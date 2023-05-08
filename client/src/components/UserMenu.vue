<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/stores/userstore";
import { getToastService } from '@/core/toast';
import { useToast } from 'primevue/usetoast';
import router from "@/router";

const menu = ref();
const items = ref([
    { label: 'Profile', icon: 'pi pi-fw pi-user' },
    { separator: true }
]);

const userstore = useUserStore();
const toast = getToastService(useToast());

const toggle = (event) => {
    menu.value.toggle(event);
};

function logout() {
    toast.success(`Successfully logout from account: ${userstore.username}`)
    userstore.logout();
    router.push('/');
}

</script>
<template>
    <div v-if="userstore.isAuthenticated" class="flex justify-content-center">
            <button @click="toggle" class="w-full p-link flex align-items-center p-2 pl-3 text-color hover:surface-200 border-noround">
                        <Avatar :image="userstore.photo ? userstore.photo : 'def_user_image.jpg'" class="mr-2" shape="circle" />
                        <div class="flex flex-column align">
                            <span class="font-bold">{{ userstore.username }}</span>
                        </div>
        </button>
        <Menu ref="menu" :model="items" popup>
                <template #end>
                    <button @click="logout" class="w-full p-link flex align-items-center p-2 pl-4 text-color hover:surface-200 border-noround">
                        <i class="pi pi-sign-out" />
                        <span class="ml-2">Log Out</span>
                    </button>
                </template>
        </Menu>
    </div>
    <div v-else>
        <Button @click="$router.push({ name: 'auth' })" label="Authorize" severity="plain" text raised />
    </div>
    
</template>
<style scoped></style>