<template>
  <v-app>
    <div class="home">
      <div class="container">
        <mdb-container>
          <section class="my-5">
            <h2 class="h1-responsive font-weight-bold text-center my-5">Why the GAMA?</h2>
            <p
              class="lead grey-text w-responsive text-center mx-auto mb-5"
            >지금 당장 GAMA 모바일 앱을 다운로드 받으세요~</p>
            <mdb-row>
              <mdb-col lg="5" class="text-center text-lg-left">
                <img
                  class="img-fluid"
                  src="https://mdbootstrap.com/img/Photos/Others/screens-section.jpg"
                  alt="Sample image"
                />
              </mdb-col>
              <mdb-col lg="7">
                <mdb-row class="mb-3">
                  <mdb-col size="1">
                    <mdb-icon icon="share" size="lg" class="indigo-text" />
                  </mdb-col>
                  <mdb-col xl="10" md="11" size="10">
                    <h5 class="font-weight-bold mb-3">01. 읽은 책을 기록하고</h5>
                    <p
                      class="grey-text"
                    >지금 어떤 책을 읽고 있는지 기록하고, 다 읽고 난 후에 평점과 리뷰를 남기세요. 한 눈에 볼 수 있도록 'GAMA'가 잘 정리해드립니다.</p>
                  </mdb-col>
                </mdb-row>
                <mdb-row class="mb-3">
                  <mdb-col size="1">
                    <mdb-icon icon="share" size="lg" class="indigo-text" />
                  </mdb-col>
                  <mdb-col xl="10" md="11" size="10">
                    <h5 class="font-weight-bold mb-3">02. 독서노트로 기억해주고</h5>
                    <p
                      class="grey-text"
                    >책을 읽다가 기억하고 싶은 글귀를 만났다면, 글/사진으로 기록하세요. ‘GAMA’가 책 별/페이지 별로 기억해줍니다.</p>
                  </mdb-col>
                </mdb-row>
                <mdb-row class="mb-3">
                  <mdb-col size="1">
                    <mdb-icon icon="share" size="lg" class="indigo-text" />
                  </mdb-col>
                  <mdb-col xl="10" md="11" size="10">
                    <h5 class="font-weight-bold mb-3">03. 읽은 책을 정리해주고</h5>
                    <p class="grey-text">내가 정한 독서 목표에 얼마나 도달했는지 확인시켜 주고, 읽은 책을 독서 달력으로 보기 좋게 정리해줍니다.</p>
                  </mdb-col>
                </mdb-row>
              </mdb-col>
            </mdb-row>
          </section>
        </mdb-container>

        <v-container class="text-center">
          <v-row no-gutters>
            <v-col md="6" offset-md="3">
              <v-btn v-show="!isLogin" x-large color="success" dark @click="loginDialog = true">로그인</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </div>
      <v-btn
        v-scroll="onScroll"
        v-show="fab"
        fab
        dark
        fixed
        bottom
        right
        color="#34495e"
        @click="toTop"
      >
        <i class="fas fa-arrow-up" style="color:white"></i>
      </v-btn>
      <!-- login dialog -->
      <LoginDialog :loginDialog="loginDialog" @closeLoginModal="closeLoginModal" />
    </div>
  </v-app>
</template>

<script>
import VueCookies from "vue-cookies";
// import swal from "sweetalert";
import LoginDialog from "../components/LoginDialog";
import { mdbContainer, mdbRow, mdbCol, mdbIcon } from "mdbvue";

export default {
  name: 'Home',
  components: {
    LoginDialog,
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbIcon,
  },
  beforeRouteEnter(to, from, next) {
    // console.log(VueCookies.get('jwt_token'))
    if (VueCookies.get("jwt_token")) {
      next({ path: "/main" });
      // swal("잘못된 접근입니다.2");
    } else {
      next();
    }
  },
  created() {
    this.isLogin = VueCookies.get("jwt_token") ? true : false;
    console.log("###");
    console.log(this.isLogin);
    console.log("###");
  },
  methods: {
    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    closeLoginModal() {
      this.loginDialog = false;
    },
  },
  data() {
    return {
      loginDialog: false,
      // 스크롤(Top)
      fab: false,

      model: 0,
      isLogin: false,
    };
  },
  mounted() {},
};
</script>
