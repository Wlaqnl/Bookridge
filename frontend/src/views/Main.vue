<template>
  <div>
    <mdb-container>
      <h2 class="h1-responsive font-weight-bold text-center my-5" >BOOKRIDGE LIBRARY</h2>
      <h6 class="text-center w-responsive mx-auto mb-5" style="font-family: 'HangeulNuri-Bold'; ">다양한 알고리즘을 기반으로 추천 도서 서비스를 제공합니다.</h6>
      <mdb-row>
        <mdb-col lg="8">
          <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
            <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1" uk-slider>
              <ul
                class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
              >
                <li>
                  <img src="@/assets/img/강아지.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>1</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/구름.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>2</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/궁합.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>3</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/메인.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>4</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>5</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경2.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>6</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/chimmy.jpeg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>7</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/money.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>8</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/PR.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>9</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/kakao_login_btn.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>10</h1>
                  </div>
                </li>
              </ul>

              <a
                class="uk-position-center-left uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-previous
                uk-slider-item="previous"
              ></a>
              <a
                class="uk-position-center-right uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-next
                uk-slider-item="next"
              ></a>
            </div>
            <a>
              <mdb-mask overlay="white-slight" waves />
            </a>
          </div>
        </mdb-col>

        <mdb-col lg="4" style="margin-top:3%;">
          <a class="green-text">
            <h6 class="font-weight-bold mb-3" style="font-family: 'HangeulNuri-Bold'; ">
              <i class="fas fa-child"></i>&nbsp;AGE
            </h6>
          </a>
          <h3 class="font-weight-bold mb-3 p-0" style="font-family: 'HangeulNuri-Bold'; ">
            <strong>90년대생이 많이 읽는 책</strong>
          </h3>
          <p style="font-family: 'HangeulNuri-Bold'; ">00년 00월 ~ 00년 00월 까지</p>
          <div style="font-family: 'HangeulNuri-Bold'; ">
          <p>
            by
            <a>
              <strong>Carine Fox</strong>
            </a>, 19/08/2018
          </p>
          </div>
          <mdb-btn color="success" size="md" class="waves-light">Read more</mdb-btn>
        </mdb-col>
      </mdb-row>
      <hr class="my-5" />

      <mdb-row>
        <mdb-col lg="4" style="margin-top:3%">
          <a class="pink-text">
            <h6 class="font-weight-bold mb-3"  style="font-family: 'HangeulNuri-Bold'; ">
              <i class="fas fa-book-reader"></i>&nbsp;GENRE
            </h6>
          </a>
          <h3 class="font-weight-bold mb-3 p-0"  style="font-family: 'HangeulNuri-Bold'; ">
            <strong>소설 좋아하는 사람을 위한 추천</strong>
          </h3>
          <div style="font-family: 'HangeulNuri-Bold'; ">
            <p>00년 00월 ~ 00년 00월 까지</p>
            <p>
              by
              <a>
                <strong>Carine Fox</strong>
              </a>, 14/08/2018
            </p>
          </div>
          <mdb-btn color="pink" size="md" class="mb-lg-0 mb-4 waves-light">Read more</mdb-btn>
        </mdb-col>
        <mdb-col lg="8">
          <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
            <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1" uk-slider>
              <ul
                class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
              >
                <li>
                  <img src="@/assets/img/강아지.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>1</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/구름.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>2</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/궁합.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>3</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/메인.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>4</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>5</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경2.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>6</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/chimmy.jpeg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>7</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/money.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>8</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/PR.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>9</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/kakao_login_btn.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>10</h1>
                  </div>
                </li>
              </ul>

              <a
                class="uk-position-center-left uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-previous
                uk-slider-item="previous"
              ></a>
              <a
                class="uk-position-center-right uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-next
                uk-slider-item="next"
              ></a>
            </div>

            <a>
              <mdb-mask overlay="white-slight" waves />
            </a>
          </div>
        </mdb-col>
      </mdb-row>
      <hr class="my-5" />

      <mdb-row>
        <mdb-col lg="8">
          <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
            <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1" uk-slider>
              <ul
                class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
              >
                <li>
                  <img src="@/assets/img/강아지.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>1</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/구름.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>2</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/궁합.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>3</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/메인.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>4</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>5</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/풍경2.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>6</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/chimmy.jpeg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>7</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/money.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>8</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/PR.jpg" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>9</h1>
                  </div>
                </li>
                <li>
                  <img src="@/assets/img/kakao_login_btn.png" alt />
                  <div class="uk-position-center uk-panel">
                    <h1>10</h1>
                  </div>
                </li>
              </ul>

              <a
                class="uk-position-center-left uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-previous
                uk-slider-item="previous"
              ></a>
              <a
                class="uk-position-center-right uk-position-small uk-hidden-hover"
                style="color:black"
                href="#"
                uk-slidenav-next
                uk-slider-item="next"
              ></a>
            </div>

            <a>
              <mdb-mask overlay="white-slight" waves />
            </a>
          </div>
        </mdb-col>
        <mdb-col lg="4" style="margin-top:3%">
          <a class="indigo-text">
            <h6 class="font-weight-bold mb-3"  style="font-family:'HangeulNuri-Bold';"> 
              <i class="fas fa-venus-mars"></i>&nbsp;GENDER
            </h6>
          </a>
          <h3 class="font-weight-bold mb-3 p-0" style="font-family: 'HangeulNuri-Bold'; " >
            <strong>남자에게 특히 더 인기 있는 책</strong>
          </h3>
          <div style="font-family:'HangeulNuri-Bold';">
            <p>00년 00월 ~ 00년 00월 까지</p>
            <p>
              by
              <a>
                <strong>Carine Fox</strong>
              </a>, 11/08/2018
            </p>
          </div>
          <mdb-btn color="indigo" size="md" class="waves-light">Read more</mdb-btn>
        </mdb-col>
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
// import swal from "sweetalert";
import VueCookies from "vue-cookies";
import { mdbContainer, mdbRow, mdbCol, mdbMask, mdbBtn } from "mdbvue";
export default {
  name: "Main",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbMask,
    mdbBtn,
  },
  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next('/')
      // swal("잘못된 접근입니다.3")
    } else {
      next();
    }
  },
  created() {
    this.$vuetify.goTo(0);

    if (VueCookies.get("jwt_token") != null) {
      this.isLogin = true;
    }
    // this.isLoading = true;
  },
  data() {
    return {
      isLogin: false,
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
@font-face { 
font-family: 'HangeulNuri-Bold'; 
src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff')
  format('woff'); 
  font-weight: normal; 
  font-style: normal;
  font-size:x-large; 
  }
</style>