import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Error from '@/views/Error.vue'
import Profile from '@/views/Profile.vue'
import ProfileEdit from '@/views/ProfileEdit.vue'
import { useUserStore } from '@/stores/userstore'

import { LOCALSTORAGE_AUTH_KEY } from '@/core/constants'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/auth',
      name: 'auth',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/profile/:user',
      name: 'profile',
      component: Profile
    },
    {
      path: '/profile/:user/edit',
      name: 'profile-edit',
      component: ProfileEdit
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'pagenotfound',
      component: Error
    },
  ]
})

router.beforeEach(async (to, from, next) => {
  const userstore = useUserStore(); 
  const publicPages = ['/auth', '/register', '/'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem(LOCALSTORAGE_AUTH_KEY);

  if (loggedIn) {
    const localuser = JSON.parse(loggedIn);
    await userstore.getUserAndProfile(localuser.username);
    userstore.setTokens(localuser.refreshToken, localuser.accessToken);
  }

  if (authRequired && !loggedIn) {
    next('/auth');
  } else {
    next();
  }
});

export default router
