<template>
  <div></div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "OauthKakao",
  created() {
    const code = this.$route.query.code;
    if (code) {
      console.log(code);
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/oauth?code=` + code)
        .then((response) => {
          VueCookies.set("jwt_token", response["data"]["token"], "1h");
          VueCookies.set("user_pk", response["data"]["user_pk"], "1h");
          VueCookies.set("social_id", response["data"]["social_id"], "1h");
          // VueCookies.set("user_gender", response["data"]["user_gender"], "1h");
          console.log(response);
          if (response.data.user_gender == 2) {
            this.$router.push({
              name: "Signup",
              params: {
                name: response.data.name,
                email: response.data.email,
                social: response.data.social,
              },
            });
          } else {
            this.$router.replace("/main");
            this.$router.go();
          }
        })
        .catch((err) => {
          this.err = err;
        });
    } else {
      // this.$router.replace("/")
    }
  },
};
</script>

<style>
</style>