<template>
  <v-app>
    <div>
      <Navbar :isLogin="isLogin" v-show="isLogin" :key="$route.fullPath"/>
    </div>
    <router-view :key="$route.fullPath"></router-view>
  </v-app>
</template>

<script>
// import axios from 'axios'
import VueCookies from "vue-cookies";
import Navbar from "./components/Navbar.vue";
export default {
  name: 'App',

  components: {
    HelloWorld,
  },
  created() {
    this.checkIsLogin();
  },
  data() {
    return {
      isLogin: false,
      imgUrl: "",
    };
  },
  methods: {
    checkIsLogin() {
      if (VueCookies.get("jwt_token")) {
        this.isLogin = true;
      } else {
        this.isLogin = false;
      }
    },
  },
};
</script>

<style>
::-webkit-scrollbar {
  width: 15px;
}

::-webkit-scrollbar-thumb {
  background-color: #4db6ac;
  border-radius: 5px;
  background-clip: padding-box;
  border: 1px solid transparent;
}

::-webkit-scrollbar-track {
  background-color: whitesmoke;
  border-radius: 10px;
  box-shadow: inset 0px 0px 5px white;
}
</style>