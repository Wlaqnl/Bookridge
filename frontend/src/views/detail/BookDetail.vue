<template>
  <div>
    <mdb-container>
      <br />
      <mdb-row>
        <mdb-col col="3">
          <img :src="image" style="width:200px; height:270px" />
          <br /><br />
          <img
            src="@/assets/img/교보문고.jpg"
            @click="kyobo"
            style="border-radius:50%; width:50px; height:50px; margin:0 5% 0 5%"
            alt
          />
          <img
            src="@/assets/img/yes24.jpg"
            @click="yes24"
            style="border-radius:50%; width:50px; height:50px; margin:0 5% 0 0"
            alt
          />
          <img
            src="@/assets/img/알라딘.jpg"
            @click="aladin"
            style="border-radius:50%; width:50px; height:50px;  margin:0 5% 0 0"
            alt
          />
        </mdb-col>
        <mdb-col col="8" style="margin-left:5px;">
          <h1 class="do">{{ title }}</h1>
          <h5 class="do">{{ author }}</h5>
          <!-- <h4 v-if="tempData.">{{ tempData.Translator }}</h4> -->
          <h5 class="do" style="font-weight:500">{{ publisher }}</h5>
          <h6 style="font-family:InfinitySans-RegularA1">{{ description }}</h6>
          <mdb-btn
            v-for="(pick, ind) in idList"
            :key="ind"
            color="primary"
            @click="goToSomewhere(pick)"
          >
            {{ pick }}
          </mdb-btn>

          <!-- <p v-if="error === null" style="font-family:BMEULJIRO">{{ popular }}</p> -->
          <!-- <p v-else class="do">인기 도서 : {{ error }}</p> -->
        </mdb-col>
        <mdb-row>
          <mdb-col lg="5" style="margin-left:2%">
            <span class="do">내용 평점 : </span>
            <vue-feedback-reaction
              v-model="feedback"
              :labels="['Worse', 'Bad', 'SoSo', 'Good', 'Best']"
              class="jua"
            />
          </mdb-col>
          <mdb-col lg="5">
            <span class="do">디자인 평점 : </span>
            <vue-feedback-reaction
              v-model="feedback"
              :labels="['Worse', 'Bad', 'SoSo', 'Good', 'Best']"
              class="jua"
            />
          </mdb-col>
        </mdb-row>
      </mdb-row>
      <br />
      <br />
      <mdb-row>
        <h3 class="do">📚이 책을 읽은 사람들이 본 책</h3>
        <br />
        <br />
        <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
          <div
            class="uk-position-relative uk-visible-toggle uk-light"
            tabindex="-1"
            uk-slider
          >
            <ul
              class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-6@m"
            >
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">1</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">2</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">3</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">4</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">5</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">6</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">7</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">8</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">9</h1>
                </div>
              </li>
              <li>
                <img src="https://picsum.photos/180/270" alt />
                <div class="uk-position-center uk-panel">
                  <h1 class="do">10</h1>
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
        </div>
      </mdb-row>
      <br />
      <br />
      <div id="seeChart">
        <BookChart :popular="popular" v-if="temp" />
      </div>
      <div id="seeLibrary">
        <mdb-row>
          <mdb-col lg="4">
            <h6 class="font-weight-bold mb-3 do">📖대출 가능한 도서관📗</h6>
            <h3 class="font-weight-bold mb-3 p-0 do">
              <strong>가까운 순 TOP 5</strong>
            </h3>
            <p class="do">00년 00월 ~ 00년 00월 까지</p>
            <p class="do">
             19/08/2018 기준
            </p>
          </mdb-col>
          <mdb-col lg="8">
            <img src="@/assets/img/gps.jpg" alt />
          </mdb-col>
        </mdb-row>
      </div>
      <hr class="my-3" />

      <div id="seePhrase">
        <mdb-row>
          <mdb-col>
            <span style="font-size:xx-large" class="do">📌Phrase</span>
            <PhraseForm @sendPhrase="getPhraseList" :booktitle2="title" />
          </mdb-col>
        </mdb-row>
        <mdb-row>
          <mdb-col lg="6">
            <img
              src="https://picsum.photos/400/300"
              style="text-align:center;"
              alt
            />
          </mdb-col>
          <mdb-col lg="6">
            <img
              src="https://picsum.photos/400/300"
              style="text-align:center;"
              alt
            />
          </mdb-col>
        </mdb-row>
      </div>

      <hr class="my-3" />

      <mdb-row id="seeReview">
        <mdb-col>
          <span style="font-size:xx-large" class="do">📝REVIEW</span>
          <ReviewForm @sendReview="getReviewList" :book="book" :btnTitle="btnTitle" />
          <mdb-container>
            <mdb-row>
              <br />
              <div class="mdb-feed" v-for="review in reviewList" :item="review" :key="review.id">
                <div class="news">
                  <div class="label">
                    <img
                      src="@/assets/img/chimmy.jpeg"
                      class="rounded-circle z-depth-1-half"
                      style="width:60px;height:60px"
                    />
                    <span class="do">&nbsp;작성자 : {{ review.user.name }} </span>
                  </div>
                  <br>
                  <div class="excerpt">
                    <div class="brief">
                      <p class="name do" style="color:blue" >제목 : {{ review.review.title }}</p>
                      <p class="do">내용 : {{ review.review.content }}</p>
                      <p class="date do" style="color:hotpink">작성 시간 : {{ review.review.created_at.slice(0,10)}}</p>
                       <p class="do">조회수 : {{ review.review.hitcount }}</p>
                      
                      <div style="color:yellow">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </mdb-row>
          </mdb-container>
          <!--Pagination teal-->
          <mdb-pagination color="teal">
            <mdb-page-nav prev></mdb-page-nav>
            <mdb-page-item active>1</mdb-page-item>
            <mdb-page-item>2</mdb-page-item>
            <mdb-page-item>3</mdb-page-item>
            <mdb-page-item>4</mdb-page-item>
            <mdb-page-item>5</mdb-page-item>
            <mdb-page-nav next></mdb-page-nav>
          </mdb-pagination>
          <!--/Pagination teal-->
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
import VueCookies from "vue-cookies";
import swal from "sweetalert";
import ReviewForm from "@/views/form/ReviewForm";
import PhraseForm from "@/views/form/PhraseForm";
import BookChart from "@/views/detail/BookChart";

import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbBtn,
  mdbPagination,
  mdbPageItem,
  mdbPageNav,
} from "mdbvue";

import { VueFeedbackReaction } from "vue-feedback-reaction";
import axios from "axios";

export default {
  name: "BookDetail",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    VueFeedbackReaction,
    mdbBtn,
    mdbPagination,
    mdbPageItem,
    mdbPageNav,
    ReviewForm,
    PhraseForm,
    BookChart,
  },

  created() {
    this.$vuetify.goTo(0);

    axios
      .get(
        `${process.env.VUE_APP_SERVER_URL}/books/book_detail/${this.$route.params.pk}/`
      )
      .then((res) => {
        console.log(res);
        this.tempData = res.data;
        this.author = res.data.author;
        this.description = res.data.description;
        this.book_pk = res.data.id;
        this.image = res.data.img_url;
        this.isbn = res.data.isbn;
        this.like_users = res.data.like_users;
        this.price = res.data.price;
        this.pub_date = res.data.pub_date;
        this.publisher = res.data.publisher;
        this.title = res.data.title;
        this.book = { book_pk: this.book_pk, book_title: this.title };
        if (res.data.popular !== undefined) {
          this.popular = res.data.popular;
        }
        if (res.data.error !== undefined) {
          this.error = res.data.error;
        }
        setTimeout(() => {
          this.temp = true;
        }, 1000);
        // this.error = res.data.error
        // this.popular = res.data.popular
      })
      .catch((err) => {
        console.log(err);
      })


      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/reviews/review/`,
            {
              params:{ book_pk: String(this.$route.params.pk) },
              headers: { Authorization: VueCookies.get("jwt_token") },  
            }
        )
        .then((res) => {
          console.log("리뷰리스트~~~");
          console.log(res.data);
          this.reviewList=res.data.result
          console.log(this.reviewList)
        })
        .catch((err) => {
          console.log(err);
        });
      
  },
  mounted(){
    console.log(this.$route.params.pk)

  },
  
  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      swal("잘못된 접근입니다.");
    } else {
      next();
    }
  },
  data() {
    return {
      // 스크롤
      fab: false,
      temp: false,
      feedback: null,
      tempData: {},
      author: null,
      description: null,
      image: null,
      isbn: null,
      like_users: null,
      price: null,
      pub_date: null,
      publisher: null,
      title: null,
      error: null,
      popular: null,
      basicRating: "",
      book_pk: null,
      book: {},
      reviewList: [],
      comment1: false,
      comment2: false,
      comment3: false,
      comment4: false,
      comment5: false,
      idList: [
        ("차트보기", "seeChart"),
        ("대출가능도서관", "seeLibrary"),
        ("글귀보기", "seePhrase"),
        ("리뷰보기", "seeReview"),
      ],
      btnTitle:"리뷰작성"
    };
  },
  methods: {
    beforeEnter(el) {
      this.elHeight = el.scrollHeight;
    },
    enter(el) {
      el.style.height = this.elHeight + "px";
    },
    beforeLeave(el) {
      el.style.height = 0;
    },
    getReviewList(data) {
      this.reviewList = data.review_list;
    },
    getPhraseList(data) {
      this.phraseList = data.phrase_list;
    },
    kyobo() {
      window.open(
        `https://search.kyobobook.co.kr/web/search?vPstrKeyWord=${this.isbn}`
      );
    },
    yes24() {
      window.open(
        `http://www.yes24.com/SearchCorner/Search?domain=BOOK&query=${this.isbn}`
      );
    },
    aladin() {
      //window.open(`https://www.aladin.co.kr/weeklyeditorialmeeting/detail.aspx?&isbn=${this.isbn}`);
      window.open(
        `https://www.aladin.co.kr/shop/wproduct.aspx?isbn=${this.isbn}`
      );
      //window.open(`https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord=${this.title}`);
    },
    goToSomewhere(item) {
      window.scrollTo(0, document.getElementById(item).offsetTop);
    },
    toTop() {
      this.$vuetify.goTo(0);
    },

    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
  },
};
</script>

<style scoped>
.yellow-text-dark-2 {
  color: #d7c952 !important;
}
.yellow-text-dark-3 {
  color: #9b9247 !important;
}
.yellow-text-dark-4 {
  color: #827c47 !important;
}
.yellow-text-dark-1 {
  color: #e9d947 !important;
}
.collapse-item {
  overflow: hidden;
  height: 0;
  padding: 0;
  transition: height 0.5s;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
.jua {
  font-family: "Jua", sans-serif;
}
.poor {
  font-family: "Poor Story", cursive;
}
.nanum {
  font-family: "Nanum Pen Script", cursive;
}
.lucky {
  font-family: "Luckiest Guy", cursive;
}
.godic {
  font-family: "Nanum Gothic", sans-serif;
}
@font-face {
  font-family: "InfinitySans-RegularA1";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/InfinitySans-RegularA1.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}
@font-face {
  font-family: "BMEULJIRO";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.0/BMEULJIRO.woff")
    format("woff");
  font-weight: lighterl;
  font-style: normal;
}
@font-face {
  font-family: "TmonMonsori";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/TmonMonsori.woff")
    format("woff");
  font-weight: lighter;
  font-style: normal;
}
</style>
