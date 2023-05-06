<script setup lang="ts"></script>

<template>
  <footer class="p-d-flex p-jc-center p-ai-center">
    <div class="p-d-flex p-jc-between p-ai-center container">
      <div class="p-d-flex p-flex-column">
        <h3>Contact Us</h3>
        <ul class="p-m-0">
          <li><i class="pi pi-map-marker"></i> 1234 Main St, Anytown USA</li>
          <li><i class="pi pi-phone"></i> (555) 555-5555</li>
          <li><i class="pi pi-envelope"></i> info@mycompany.com</li>
        </ul>
      </div>
      <div class="p-d-flex p-flex-column">
        <h3>Follow Us</h3>
        <ul class="p-m-0">
          <li><a href="#"><i class="pi pi-facebook"></i> Facebook</a></li>
          <li><a href="#"><i class="pi pi-twitter"></i> Twitter</a></li>
          <li><a href="#"><i class="pi pi-instagram"></i> Instagram</a></li>
        </ul>
      </div>
      <div>
        <p class="p-m-0">&copy; 2023 My Company. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  background-color: #f8f9fa;
  color: #343a40;
  padding: 40px 0;
}

h3 {
  color: #007bff;
}

ul {
  list-style: none;
}

ul li {
  margin-bottom: 10px;
}

ul li a {
  color: #343a40;
}

ul li a:hover {
  color: #007bff;
}

.p-flex-column {
  flex-direction: column;
}

@media (min-width: 768px) {
  .p-d-flex {
    flex-direction: row;
  }

  .p-d-flex > *:not(:last-child) {
    margin-right: 50px;
  }

  .p-flex-column {
    flex-direction: row;
  }

  .p-flex-column > *:not(:last-child) {
    margin-right: 30px;
  }
}
</style>
