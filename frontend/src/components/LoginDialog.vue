<template>
  <v-row justify="center">
    <!-- Dialgo2 -->
    <v-dialog v-model="loginDialog" @click:outside="closeLoginModal" max-width="900px" class="m-0">
      <v-card max-width="900px">
        <v-row>
          <v-col cols="6">
            <v-card class="ml-3" min-height="400px">
              <v-card-text>
                <v-card-title class="headline justify-content-center">로그인</v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row justify="center">
                      <v-col cols="12" class="py-0">
                        <v-text-field ref="emailInput" v-model="email" label="아이디" required></v-text-field>
                        <!-- <p class="hint-size caption">'아이디@bookridge.com' 형식으로 입력해주세요.</p> -->
                      </v-col>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          ref="passwordInput"
                          v-model="password"
                          label="비밀번호"
                          type="password"
                          hint
                          required
                        ></v-text-field>
                      </v-col>
                      <v-spacer></v-spacer>
                      <div class="d-flex justify-center">
                        <v-btn
                          color="success"
                          @click="login"
                          min-width="240"
                          max-width="300"
                          outlined
                        >로그인</v-btn>
                      </div>
                    </v-row>
                  </v-container>
                </v-card-text>

                <h6 class="text-center">
                  아직 회원이 아니신가요?
                  <v-btn color="green darken-1" text @click="closeLoginModal" to="/signup">회원가입</v-btn>
                </h6>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="mr-3" min-height="400px">
              <v-card-text>
                <v-card-title class="headline justify-content-center">SNS 로그인</v-card-title>
                <v-card-text class="pt-5">
                  <a class="d-flex justify-center my-2" :href="kakaoRedirect">
                    <img
                      class="tempLogin"
                      src="@/assets/img/kakao_login_btn.png"
                      height="20px"
                      width="300px"
                    />
                  </a>

                  <a class="d-flex justify-center" :href="googleRedirect">
                    <img
                      class="tempLogin"
                      src="@/assets/img/google_login_btn.png"
                      height="20px"
                      width="300px"
                    />
                  </a>
                </v-card-text>
                <v-spacer></v-spacer>
                <v-card-actions class="justify-content-end mt-5">
                  <v-btn class="mt-5" color="green darken-1" text @click="closeLoginModal">닫기</v-btn>
                </v-card-actions>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialog3" max-width="500px">
      <v-card>
        <v-card-title>
          <v-card-title class="px-0">이메일 인증이 확인되지 않았습니다.</v-card-title>
          <v-spacer></v-spacer>
        </v-card-title>

        <v-card-text>이메일을 확인해주세요.</v-card-text>
        <v-card-text>
          메일이 도착하지 않았을 경우
          <v-btn class="pb-1 px-0" color="success" text @click="final">인증메일 다시보내기</v-btn>를 클릭해주세요.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="dialog3 = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import swal from "sweetalert";
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "LoginDialog",
  props: {
    loginDialog: Boolean,
  },
  data() {
    return {
      kakaoRedirect: `${process.env.VUE_APP_SERVER_URL}/accounts/kakao_login/`,
      googleRedirect: `${process.env.VUE_APP_SERVER_URL}/accounts/google_login/`,
      dialog2: false,
      dialog3: false,
      notifications: false,
      sound: true,
      widgets: false,
      ///////////
      email: "",
      password: "",
    };
  },
  methods: {
    final() {
      console.log(this.email);
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/user/verifymailsend?email=${this.email}`
        )
        .then((res) => {
          console.log(res.data.object);
          this.dialog3 = false;
          // alert("인증메일을 재전송하였습니다.");
          this.email = "";
          this.password = "";
        })
        .catch((err) => {
          console.log(err);
        });
    },
    login() {
      axios
        .post(`${process.env.VUE_APP_SERVER_URL}/accounts/login/`, {
          email: this.email + '@bookridge.com',
          password: this.password,
        })
        .then((res) => {
          if (res.data.error) {
            swal("아이디 비밀번호를 확인해주세요!");
          } else {
            VueCookies.set("jwt_token", res["data"]["token"], "6h");
            VueCookies.set("user_pk", res["data"]["user_pk"], "6h");
            VueCookies.set("social_id", 0, "6h");

            this.closeLoginModal();
            this.$router.push("/main");
            this.$router.go();
            this.dialog3 = true;
          }
        })
        .catch((err) => {
          this.err = err;
          alert("아이디 또는 비밀번호를 확인해주세요.");
        });
    },
    closeLoginModal() {
      this.email = "";
      this.password = "";
      this.$emit("closeLoginModal");
    },
    loginInputEnter() {
      if (this.email !== "" && this.password === "") {
        this.$refs.passwordInput.focus();
      } else if (this.password !== "" && this.email === "") {
        this.$refs.emailInput.focus();
      } else {
        this.login();
      }
    },
  },
};
</script>

<style scoped>
.tempLogin {
  height: 40px;
}
a {
  border-radius: 5px;
}
a:hover {
  opacity: 0.7;
}
.hint-size {
  font-size: 12px;
}
</style>