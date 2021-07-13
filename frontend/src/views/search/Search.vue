<template>
  <div id="main">
    <br />

    <!--도서검색결과 있을 시-->
    <h1 style="text-align:center;font-family: 'MaplestoryOTFBold';">'{{ searchWord }}'에 대한 검색 결과</h1>
    <br />

    <mdb-container>
      <mdb-row>
        <mdb-col col="4" v-for="book in searchData" :item="book" :key="book.id">
          <mdb-card style="height:700px">
            <mdb-row>
              <mdb-col col="12" class="pic" v-if="book.img_url">
                <mdb-view hover class="zoom">
                  <mdb-card-image :src="book.img_url" alt="bookImage" class="bookimage" />
                  <mdb-mask flex-center waves overlay="black-slight" text="자세히보기">
                    <i class="fas fa-forward"></i>
                  </mdb-mask>
                </mdb-view>
              </mdb-col>
              <mdb-col col="12" class="pic" v-else>
                <mdb-view hover class="zoom">
                  <!-- <mdb-card-image src="@/assets/img/money.jpg" alt="bookImage" class="bookimage"  /> -->
                  <p>이 책은 사진이 없습니다.</p>
                </mdb-view>
              </mdb-col>
              <mdb-row>
                <mdb-card-body>
                  <h4 style="font-family: 'MaplestoryOTFBold'; margin:0 5% 0 5%">{{ book.title }}</h4>
                  <br />
                  <p style="font-family: 'MaplestoryOTFBold'; margin-left:5%">{{ book.author }}</p>
                  <p
                    style="font-family: 'MaplestoryOTFBold'; margin-left:5%"
                  >출판사 : {{ book.publisher }}</p>
                  <p
                    style="font-family: 'MaplestoryOTFBold'; margin-left:5%"
                  >출판년도 : {{ book.pub_date }}년</p>

                  <div class="button">
                    <mdb-btn
                      color="yellow"
                      style="font-family: 'MaplestoryOTFBold'"
                      @click="gotoDetail(book.id)"
                    >DETAIL</mdb-btn>
                  </div>
                </mdb-card-body>
              </mdb-row>
            </mdb-row>
          </mdb-card>
        </mdb-col>
      </mdb-row>
      <div style="text-align:center;" v-if="isLoading" class="loading">
        <div class="spinner-grow text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-secondary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-success" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-danger" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-warning" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-info" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-light" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-dark" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
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
import axios from "axios";
import {
  mdbContainer,
  mdbRow,
  mdbCol,
  mdbCard,
  mdbCardImage,
  mdbCardBody,
  mdbBtn,
  mdbView,
  mdbMask,
} from "mdbvue";

export default {
  name: "Search",
  data() {
    return {
      fab: false,
      searchData: null,
      isLoading: false,
      flag: true,
      bottomBtn: true,
      isDetect: true,
      page: 0,
    };
  },

  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbCard,
    mdbCardImage,
    mdbCardBody,
    mdbBtn,
    mdbView,
    mdbMask,
  },
  created() {
    this.searchWord = this.$route.params.search_word;
    this.searchType = this.$route.params.search_type;
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/books/book_search/0/`, {
        params: {
          search_word: this.searchWord,
          search_type: this.searchType,
        },
      })
      .then((res) => {
        console.log(res);
        if (res.data.result.length) {
          this.searchData = res.data.result;
        } else {
          this.$router.push("/search2");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
  mounted() {
    this.isLoading = true;
    const el = document.querySelector("#main");
    console.log(el);
    document.addEventListener("scroll", () => {
      const pos = el.scrollHeight - window.scrollY;

      if (pos < 700) {
        if (this.isDetect) {
          this.isDetect = false;
          this.loadMore();
        }
      } else {
        this.isDetect = true;
      }
      try {
        if (0.975 <= window.scrollY / el.scrollHeight) {
          this.bottomBtn = false;
        } else {
          this.bottomBtn = true;
        }
      } catch (err) {
        console.log(err);
      }
      this.isLoading = false;
    });
  },
  methods: {
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    loadMore() {
      const leng = this.searchData.length;
      console.log(leng);
      if (this.flag && leng % 10 == 0 && !this.isLoading) {
        this.isLoading = true;
        const page = parseInt(this.searchData.length / 10);
        console.log(page);
        // axios 요청
        axios
          .get(`${process.env.VUE_APP_SERVER_URL}/books/book_search/${page}/`, {
            params: {
              search_word: this.searchWord,
              search_type: this.searchType,
            },
          })
          .then((res) => {
            console.log("기존의 책들");
            console.log(this.searchData);
            console.log("새로운 책들");
            console.log(res.data.result);
            if (this.flag) {
              this.searchData = this.searchData.concat(res.data.result);
            }
            console.log(this.searchData);
            console.log(this.searchData.length);
            if (res.data.result.length === 0) {
              this.flag = false;
            }
          })
          .catch((err) => {
            console.log(err);
          });

        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.button {
  margin: auto;
  width: 50%;
}
.pic {
  padding: 5%;
}
.bookimage {
  width: 180px;
  height: 270px;
}
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}

.loading {
  text-align: center;
  display: block;
  position: fixed;
  color: black;
  z-index: 2;
  padding: 8px 18px;
  border-radius: 5px;
  left: calc(50% - 105px);
  top: calc(50% - 45px);
}
</style>