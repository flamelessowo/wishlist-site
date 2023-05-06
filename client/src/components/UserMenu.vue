<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/stores/userstore";

const menu = ref();
const items = ref([
    { label: 'Profile', icon: 'pi pi-fw pi-user' },
    { label: 'Settings', icon: 'pi pi-fw pi-cog' },
    { separator: true }
]);

const userstore = useUserStore();

const toggle = (event) => {
    menu.value.toggle(event);
};

</script>
<template>
    <div v-if="userstore.isAuthenticated" class="flex justify-content-center">
            <button @click="toggle" class="w-full p-link flex align-items-center p-2 pl-3 text-color hover:surface-200 border-noround">
                        <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" class="mr-2" shape="circle" />
                        <div class="flex flex-column align">
                            <span class="font-bold">Amy Elsner</span>
                        </div>
        </button>
        <Menu ref="menu" :model="items" popup>
                <template #end>
                    <button class="w-full p-link flex align-items-center p-2 pl-4 text-color hover:surface-200 border-noround">
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