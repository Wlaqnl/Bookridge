<template>
  <mdb-container>
    <!-- <mdb-btn color="default" @click.native="header = true"
      >Review 쓰기 <i class="fas fa-edit"></i
    ></mdb-btn> -->
    <mdb-btn
      class="deep-blue-gradient"
      style="color:white;float:right"
      @click.native="header = true"
      >{{ btnTitle }}</mdb-btn
    >

    <mdb-modal :show="header" @close="header = false" warning>
      <mdb-modal-header class="text-center">
        <mdb-modal-title tag="h4" bold class="w-100"
          >Review Form</mdb-modal-title
        >
      </mdb-modal-header>
      <mdb-modal-body class="mx-3">
        <div v-if="bookTitle == null">
          <mdb-input
            label="Book Title"
            v-model="book.book_title"
            icon="clipboard"
            class="mb-5"
            iconClass="text"
            style="font-family: 'MaplestoryOTFBold';"
          />
        </div>
        <div v-else>
          <h2 style="font-family: 'MaplestoryOTFBold';">{{ bookTitle }}</h2>
        </div>
        <mdb-input
          label="Review Title"
          v-model="reviewdata.title"
          icon="clipboard"
          class="mb-5"
          iconClass="text"
          style="font-family: 'MaplestoryOTFBold';"
        />
        <mdb-input
          type="textarea"
          outline
          v-model="reviewdata.content"
          :rows="4"
          label="content"
          icon="comment"
          style="font-family: 'MaplestoryOTFBold';"
        />
        <mdb-row>
          <mdb-col>
            <span style="font-family: 'MaplestoryOTFBold';"
          >내용 평점 :<vue-feedback-reaction
            v-model="reviewdata.content_score"
            :labels="['1', '2', '3', '4', '5']"
        /></span>
          </mdb-col>
        </mdb-row>

        <mdb-row>
          <mdb-col>
            <span style="font-family: 'MaplestoryOTFBold';"
              >디자인 평점 :<vue-feedback-reaction
                v-model="reviewdata.design_score"
                :labels="['1', '2', '3', '4', '5']"
            /></span>
          </mdb-col>
        </mdb-row>
        <br />
        {{ reviewdata }}
      </mdb-modal-body>
      <mdb-modal-footer center>
        <mdb-btn @click="sendReview" outline="warning"
          >Send <mdb-icon icon="paper-plane" class="ml-1"
        /></mdb-btn>
        <mdb-btn @click.native="header = false" outline="primary"
          >Close <mdb-icon icon="times" class="ml-1" style="color:blue"
        /></mdb-btn>
      </mdb-modal-footer>
    </mdb-modal>
  </mdb-container>
</template>

<script>
import swal from "sweetalert";
import {
  mdbContainer,
  mdbBtn,
  mdbModal,
  mdbModalHeader,
  mdbModalBody,
  mdbInput,
  mdbModalFooter,
  mdbModalTitle,
  mdbIcon,
  mdbRow,
  mdbCol,
} from "mdbvue";
import { VueFeedbackReaction } from "vue-feedback-reaction";
import axios from "axios";
import VueCookies from 'vue-cookies';


export default {
  components: {
    mdbContainer,
    mdbBtn,
    mdbModal,
    mdbModalHeader,
    mdbModalBody,
    mdbInput,
    mdbModalFooter,
    mdbModalTitle,
    mdbIcon,
    VueFeedbackReaction,
    mdbRow,
    mdbCol,
  },
  data() {
    return {
      header: false,
      bookTitle: null,
      reviewdata: {
        title: null,
        content: null,
        content_score: null,
        design_score: null,
        book_pk:null
      },
    };
  },
  methods: {
    sendReview() {
      this.reviewdata.book_pk=this.book.book_pk
      console.log(this.reviewdata)
      axios
        .put(
          `${process.env.VUE_APP_SERVER_URL}/reviews/review/`,
            this.reviewdata,
            {
              headers: { Authorization: VueCookies.get("jwt_token") }, // 마찬가지로 Back에 @permission 있으면 작성해 줘야되유
            }
        )
        .then((res) => {
          console.log(res);
          this.$emit("sendReview", res.data);
          this.header = false
          swal("리뷰작성이 완료되었습니다.")
        })
        .catch((err) => {
          console.log(err);
        });
    },
    sendModify(){
      // axios
      //   .post(`${process.env.VUE_APP_SERVER_URL}/reviews/review`,
      //   {
      //     review_pk: id,
      //   },
      //   {
      //     headers:{Authorization: VueCookies.get("jwt_token")}
      //   }
      // )
    }
  },
  props:{
    book:Object,
    btnTitle:String,
  }
};
</script>

<style scoped>
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
}
</style>
