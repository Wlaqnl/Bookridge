
<template>
  <div id="app">
    <mdb-container>
      <mdb-row>
        <mdb-col lg="4">
          <h2>전국도서이용현황</h2>
        </mdb-col>
        <mdb-col lg="8">
          <img src="https://picsum.photos/400/600" alt />
        </mdb-col>
      </mdb-row>
      <hr />
      <mdb-row>
        <mdb-col lg="4">
          <h2>지역별 장르 선호 현황</h2>
        </mdb-col>
        <mdb-col lg="8">
          <img src="https://picsum.photos/400/600" alt />
        </mdb-col>
      </mdb-row>
      <hr />
      <mdb-row>
        <mdb-col lg="8">
          <img src="https://picsum.photos/600/400" alt />
        </mdb-col>
        <mdb-col lg="4">
          <h2>내 주변의 도서관</h2>
        </mdb-col>
      </mdb-row>
      <mdb-row>
        <mdb-col lg="1"></mdb-col>
        <mdb-col lg="2">
          <mdb-card>
            <mdb-view hover>
              <a href="#!">
                <mdb-card-image src="https://picsum.photos/200/300" alt="Card image cap" />
                <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              </a>
            </mdb-view>
            <mdb-card-body>
              <mdb-card-title>구미인동도서관</mdb-card-title>
              <mdb-card-text>위치 : 경상북도 구미시 진미동 인동14길 14</mdb-card-text>
              <mdb-card-text>휴관일 : 매주 둘째주, 넷째주 월요일</mdb-card-text>
              <mdb-btn class="deep-blue-gradient">HOMEPAGE</mdb-btn>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col lg="2">
          <mdb-card>
            <mdb-view hover>
              <a href="#!">
                <mdb-card-image src="https://picsum.photos/200/300" alt="Card image cap" />
                <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              </a>
            </mdb-view>
            <mdb-card-body>
              <mdb-card-title>구미인동도서관</mdb-card-title>
              <mdb-card-text>위치 : 경상북도 구미시 진미동 인동14길 14</mdb-card-text>
              <mdb-card-text>휴관일 : 매주 둘째주, 넷째주 월요일</mdb-card-text>
              <mdb-btn class="deep-blue-gradient">HOMEPAGE</mdb-btn>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col lg="2">
          <mdb-card>
            <mdb-view hover>
              <a href="#!">
                <mdb-card-image src="https://picsum.photos/200/300" alt="Card image cap" />
                <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              </a>
            </mdb-view>
            <mdb-card-body>
              <mdb-card-title>구미인동도서관</mdb-card-title>
              <mdb-card-text>위치 : 경상북도 구미시 진미동 인동14길 14</mdb-card-text>
              <mdb-card-text>휴관일 : 매주 둘째주, 넷째주 월요일</mdb-card-text>
              <mdb-btn class="deep-blue-gradient">HOMEPAGE</mdb-btn>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col lg="2">
          <mdb-card>
            <mdb-view hover>
              <a href="#!">
                <mdb-card-image src="https://picsum.photos/200/300" alt="Card image cap" />
                <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              </a>
            </mdb-view>
            <mdb-card-body>
              <mdb-card-title>구미인동도서관</mdb-card-title>
              <mdb-card-text>위치 : 경상북도 구미시 진미동 인동14길 14</mdb-card-text>
              <mdb-card-text>휴관일 : 매주 둘째주, 넷째주 월요일</mdb-card-text>
              <mdb-btn class="deep-blue-gradient">HOMEPAGE</mdb-btn>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col lg="2">
          <mdb-card>
            <mdb-view hover>
              <a href="#!">
                <mdb-card-image src="https://picsum.photos/200/300" alt="Card image cap" />
                <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              </a>
            </mdb-view>
            <mdb-card-body>
              <mdb-card-title>구미인동도서관</mdb-card-title>
              <mdb-card-text>위치 : 경상북도 구미시 진미동 인동14길 14</mdb-card-text>
              <mdb-card-text>휴관일 : 매주 둘째주, 넷째주 월요일</mdb-card-text>
              <mdb-btn class="deep-blue-gradient">HOMEPAGE</mdb-btn>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col lg="1"></mdb-col>
      </mdb-row>
    </mdb-container>
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
      <v-icon>mdi-arrow-up-thick</v-icon>
    </v-btn>
  </div>
</template>

<script>
import VueCookies from "vue-cookies";
import swal from "sweetalert";
import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbCard,
  mdbCardImage,
  mdbCardBody,
  mdbCardTitle,
  mdbCardText,
  mdbBtn,
  mdbView,
  mdbMask,
} from "mdbvue";

export default {
  name: "Analyze",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbCard,
    mdbCardImage,
    mdbCardBody,
    mdbCardTitle,
    mdbCardText,
    mdbBtn,
    mdbView,
    mdbMask,
  },
  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      swal("잘못된 접근입니다.")
    } else {
      next();
    }
  },
  data() {
    return {
      // 스크롤
      fab: false,
    };
  },
  methods: {
    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },

    // 최상단으로 이동하기
    toTop() {
      this.$vuetify.goTo(0);
    },
  },
};
</script>

<style scoped>
.col-lg-8 {
  text-align: center;
}
</style>