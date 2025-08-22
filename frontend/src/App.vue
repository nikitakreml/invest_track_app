<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/dashboard">Dashboard</router-link> |
      <router-link to="/transactions">Transactions</router-link> |
      <router-link to="/settings">Settings</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Montserrat', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #174D38;
  margin-top: 60px;
  background-color: #F2F2F2;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #174D38;
}

nav a.router-link-exact-active {
  color: #4D1717;
}
</style>
