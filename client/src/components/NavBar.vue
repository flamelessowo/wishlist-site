<script setup lang="ts">
import { ref } from "vue";
import UserMenu from "@/components/UserMenu.vue"

const items = ref([
    {
        label: 'Home',
        icon: 'pi pi-fw pi-home',
        to: '/'
    },
    {
        label: 'Wish lists',
        icon: 'pi pi-fw pi-list',
    },
]);
</script>
<template>
    <div class="card">
        <MenuBar :model="items" >
            <template #start>
        <img
          alt="logo"
          src="wishlist.png"
          height="30"
          class="mr-2"
        />
      </template>
      <template #end>
        <!-- <InputText placeholder="Search" type="text" /> -->
        <UserMenu style="position: relative;"/>
      </template>
        </MenuBar>
    </div>
</template>
<style scoped></style>