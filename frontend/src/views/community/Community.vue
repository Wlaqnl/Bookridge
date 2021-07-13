<template>
  <div>
    <br />
    <div style="text-align:center">
      <h1 style="font-family: HangeulNuri-Bold">REVIEWS</h1>
      <mdb-form-inline class="active-cyan active-cyan-4 d-flex justify-content-end" style="margin-right:12%">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" style="font-family: HangeulNuri-Bold; text-align:center;" />
        <mdbIcon icon="search" />
      </mdb-form-inline>
    </div>
    <div class="container">
      <div class="row" >
        <div class="col-lg-6 col-sm-12"  v-for="review in reviewData" :item="review" :key="review.id" style="  width:48%">
          <v-card  >
            <v-row>
              <v-col cols="5" style="margin-left:2%">
                <v-card class="d-inline-block mx-auto" style="width:250px;">
                  <v-container>
                    <v-row justify="space-between">
                      <v-col cols="auto">
                        <v-img
                          height="270"
                          width="200"
                          :src="review.book_img_url"
                          @click="gotoDetail(review.book)"
                        ></v-img>
                      </v-col>
                    </v-row>
                    <v-row
                      class="d-flex justify-content-center"
                      style="margin-left:2%; "
                    >
                     
                      <h4 style="font-family: HangeulNuri-Bold">{{ review.book_title }}</h4>
                    </v-row>
                    <v-row
                      class="d-flex justify-content-center"
                      style="margin-left:2%"
                    >
                      <p><mdb-rating v-bind="star" /></p>
                    </v-row>
                    <v-row class="text-right">
                      <v-col>
                        <v-btn icon>
                          <v-icon>mdi-bookmark</v-icon>
                        </v-btn>
                        <v-btn icon @click="gotoDetail(review.book)" uk-tooltip="책 바로가기">
                          <i class="fas fa-ellipsis-v"></i>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card>
              </v-col>
              <v-col cols="6" class="d-flex flex-column justify-content-between">
                <div>
                  <v-list-item>
                    <v-list-item-avatar>
                      <img src="@/assets/img/chimmy.jpeg" alt />
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title
                        style="font-family: HangeulNuri-Bold;font-size:large"
                        >{{ review.user_name }}</v-list-item-title
                      >
                      
                    </v-list-item-content>
                  </v-list-item>
                  <v-card-text style="margin-left:2%;" >
                    <h4 style="font-family: HangeulNuri-Bold">제목 : {{ review.title }}</h4>
                    <br />
                    <p style="font-family: HangeulNuri-Bold; font-size:large">내용 : {{ review.content }}</p>
                    
                  </v-card-text>
                 
                </div>
                
                <div class="bottomIcon" >
                  <v-list-item-subtitle style="font-family: HangeulNuri-Bold; font-size:medium" class="d-flex justify-content-end"
                      >{{ review.created_at.slice(0, 10) }} {{ review.created_at.slice(11,16) }} </v-list-item-subtitle
                    >

                  <v-row  class="d-flex justify-content-end">
                    <v-btn icon >
                      <v-icon >mdi-heart</v-icon>
                    </v-btn>
                    <v-dialog
                      v-model="dialog"
                      fullscreen
                      hide-overlay
                      transition="dialog-bottom-transition"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-bind="attrs" v-on="on">
                          <i class="fas fa-ellipsis-h"></i>
                        </v-btn>
                      </template>
                      <v-card>
                        <v-toolbar dark color="primary">
                          <v-toolbar-title>CommunityCard</v-toolbar-title>
                          <v-spacer></v-spacer>
                          <v-toolbar-items>
                            <v-btn icon dark @click="dialog = false">
                              <v-icon>mdi-close</v-icon>
                            </v-btn>
                          </v-toolbar-items>
                        </v-toolbar>
                        <v-row class="px-5">
                          <v-col cols="7">
                            <v-list three-line subheader>
                              <v-subheader>글 부분</v-subheader>
                              <v-list-item>
                                <v-list-item-content>
                                  <h3 class="text-center">제목</h3>
                                  <v-row>
                                    <v-col cols="2">
                                      <v-avatar color="indigo">
                                        <v-icon dark>mdi-account-circle</v-icon>
                                      </v-avatar>
                                    </v-col>
                                    <v-col cols="10">
                                      <h5>작성자</h5>
                                      <p>작성날짜 | 좋아요 00개</p>
                                    </v-col>
                                  </v-row>
                                </v-list-item-content>
                              </v-list-item>
                              <v-list-item>
                                <v-list-item-content>
                                  <v-list-item-title>내용</v-list-item-title>
                                  <v-list-item-subtitle
                                    >Contents</v-list-item-subtitle
                                  >
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-col>
                          <v-col cols="5" class="pr-5">
                            <v-subheader inset>댓글부분</v-subheader>
                            <v-row>
                              <v-col cols="2">
                                <v-avatar color="indigo">
                                  <v-icon dark>mdi-account-circle</v-icon>
                                </v-avatar>
                              </v-col>
                              <v-col cols="8">
                                <v-textarea
                                  label="댓글을 입력해주세요."
                                  auto-grow
                                  outlined
                                  rows="1"
                                  row-height="15"
                                ></v-textarea>
                              </v-col>
                              <v-col>
                                <v-btn text>등록</v-btn>
                              </v-col>
                            </v-row>
                            <v-row>
                              <v-col cols="2">
                                <v-avatar color="indigo">
                                  <v-icon dark>mdi-account-circle</v-icon>
                                </v-avatar>
                              </v-col>
                              <v-col cols="2">
                                <p>아이디</p>
                                <p>생성날짜</p>
                              </v-col>
                              <v-col cols="8">
                                <div
                                  class="pa-6 text-center grey lighten-2 rounded-xl"
                                >
                                  댓글
                                </div>
                              </v-col>
                            </v-row>
                            <v-row class="d-flex justify-content-end">
                              <v-btn text>수정</v-btn>
                              <v-btn text>삭제</v-btn>
                            </v-row>
                          </v-col>
                        </v-row>
                      </v-card>
                    </v-dialog>
                  </v-row>
                   <!--Pink-->
                  <mdb-btn color="pink" style="border-radius:5%;font-family: HangeulNuri-Bold" >수정하기</mdb-btn>
                  <!--Purple-->
                  <mdb-btn color="purple" style="border-radius:5%;font-family: HangeulNuri-Bold">삭제하기</mdb-btn>
                   <ReviewForm @sendReview="getReviewList" :book="book" :btnTitle="btnTitle" />
                </div>
              </v-col>
            </v-row>
          </v-card>
          <br>
        </div>
      </div>
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
      <v-icon>mdi-arrow-up-thick</v-icon>
    </v-btn>
  </div>
</template>


<script>
import VueCookies from "vue-cookies";
import swal from "sweetalert";
import { mdbIcon, mdbFormInline,mdbRating,mdbBtn } from "mdbvue";
import axios from "axios";
import ReviewForm from '@/views/form/ReviewForm';

export default {
  components: {
    mdbIcon,
    mdbFormInline,
    mdbRating,
    mdbBtn,
    ReviewForm,
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
      dialog: false,
      star: null,
      reviewData:{},
      
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
    gotoDetail(id){
      this.$router.push(`bookdetail/${id}`)
    },
    
  },
  created() {
      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/reviews/community/`,
        {
          params: { },// Back에서 원하는 데이터
          headers: { Authorization: VueCookies.get("jwt_token") },
        })

        .then((res) => {
          console.log(res);
          this.reviewData=res.data.result;
          
        })
        .catch((err) => {
          console.log(err);
        })

  }
}

</script>

<style scoped>
.active-cyan-2 input[type="text"]:focus:not([readonly]) {
  border: 1px solid #4dd0e1;
  box-shadow: 0 1px 0 0 #4dd0e1;
}
.active-cyan input[type="text"] {
  border: 1px solid #4dd0e1;
  box-shadow: 0 1px 0 0 #4dd0e1;
  text-align: center;
}
.active-cyan .fa,
.active-cyan-2 .fa {
  color: #4dd0e1;
}
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
.bottomIcon {
  align-self: flex-end;
}
</style>
