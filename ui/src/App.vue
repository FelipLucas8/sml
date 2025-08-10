<script setup>
import Home from './components/Home.vue'
</script>

<template>
  <router-view />
</template>

<style scoped>
@media (min-width: 1024px) {
  /* header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
  
  .logo {
    margin: 0 2rem 0 0;
  } */

}

.nav-bar {
  position: absolute;
  right: 0;
  width: 100%;
  top: 24px;
  display: flex;
  justify-content: center;
}

.main-button-center {
  border-radius: 24px;
  background-color: rgba(128, 128, 128, 0.08);
  padding: 5px;
}

.nav-main-button {
  border-radius: 24px;
  /* background-color: red; */
}

.nav-main-button:hover:nth-child(1) {
  background-color: var(--light-mode-grey);
}

.nav-main-button:hover:nth-child(2) {
  background-color: var(--light-mode-grey);
}

.nav-main-button:hover:nth-child(3) {
  background-color: var(--light-mode-grey);
}

.nav-main-button:hover:nth-child(4) {
  background-color: var(--light-mode-grey);
}

.nav-main-button:hover:nth-child(5) {
  background-color: var(--light-mode-grey);
}

.main-button-right {
  display: flex;
  align-items: center;
  border: 1px solid var(--light-mode-grey);
  border-radius: 24px;
  padding: 2px;
}
</style>
