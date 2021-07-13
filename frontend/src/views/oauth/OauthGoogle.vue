<template>
  <div></div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "OauthGoogle",
  created() {
    const code = this.$route.query.code;
    if (code) {
      console.log(code);
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/oauth2?code=` + code)
        .then((response) => {
          // console.log(response)
          VueCookies.set("jwt_token", response["data"]["token"], "1h");
          VueCookies.set("user_pk", response["data"]["user_pk"], "1h");
          VueCookies.set("social_id", response["data"]["social_id"], "1h");
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
            this.$router.replace("/");
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