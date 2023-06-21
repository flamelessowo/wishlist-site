import { createApp } from 'vue'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config';

import "primevue/resources/themes/mdc-light-indigo/theme.css"
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";

import Toast from 'primevue/toast';
import Menubar from 'primevue/menubar';
import Password from 'primevue/password';
import Menu from 'primevue/menu';
import Textarea from 'primevue/textarea';
import TabMenu from 'primevue/tabmenu';
import InputText from 'primevue/inputtext';
import FileUpload from 'primevue/fileupload';
import Button from 'primevue/button';
import ProgressBar from 'primevue/progressbar';
import Badge from 'primevue/badge';
import Card from 'primevue/card';
import Carousel from 'primevue/carousel';
import Checkbox from 'primevue/checkbox';
import Galleria from 'primevue/galleria';
import Avatar from 'primevue/avatar';
import Calendar from 'primevue/calendar';
import Image from 'primevue/image';
import Toolbar from 'primevue/toolbar';
import DataTable from 'primevue/datatable';
import DataView from 'primevue/dataview';
import Column from 'primevue/column';
import Rating from 'primevue/rating';
import Dialog from 'primevue/dialog';
import ConfirmPopup from 'primevue/confirmpopup';
import ConfirmationService from 'primevue/confirmationservice';
import Listbox from 'primevue/listbox';
import AvatarGroup from 'primevue/avatargroup';

import App from './App.vue'
import router from './router'
import ToastService from 'primevue/toastservice';

const app = createApp(App)

app.use(PrimeVue)

app.component('MenuBar', Menubar);
app.component('Password', Password);
app.component('Menu', Menu);
app.component('TabMenu', TabMenu);
app.component('Textarea', Textarea);
app.component('InputText', InputText);
app.component('FileUpload', FileUpload);
app.component('Button', Button);
app.component('Badge', Badge);
app.component('ProgressBar', ProgressBar);
app.component('Card', Card);
app.component('Carousel', Carousel);
app.component('Checkbox', Checkbox)
app.component('Galleria', Galleria);
app.component('Avatar', Avatar);
app.component('Toast', Toast);
app.component('Calendar', Calendar);
app.component('Image', Image);
app.component('Toolbar', Toolbar);
app.component('DataTable', DataTable);
app.component('DataView', DataView);
app.component('Column', Column);
app.component('Rating', Rating);
app.component('Dialog', Dialog);
app.component('ConfirmPopup', ConfirmPopup);
app.component('Listbox', Listbox);
app.component('AvatarGroup', AvatarGroup);
app.use(ToastService);
app.use(ConfirmationService);
app.use(createPinia())
app.use(router)

app.mount('#app')
