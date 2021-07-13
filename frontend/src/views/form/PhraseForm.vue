<template>
  <mdb-container>
    <!-- <mdb-btn color="default" @click.native="header = true">Phrase 쓰기 <i class="fas fa-edit"></i></mdb-btn> -->
    <mdb-btn class="deep-blue-gradient" style="color:white;float:right" @click.native="header=true">글귀 작성</mdb-btn>
    <mdb-modal :show="header" @close="header = false" warning> 
      <mdb-modal-header class="text-center">
        <mdb-modal-title tag="h4" bold class="w-100">Phrase Form</mdb-modal-title>
      </mdb-modal-header>
      <mdb-modal-body class="mx-3">
        <div v-if="bookTitle == null">
          <mdb-input
            label="Book Title"
            v-model="booktitle2"
            icon="clipboard"
            class="mb-5"
            iconClass="text"
            style="font-family: 'MaplestoryOTFBold';"
          />
        </div>
        <div v-else>
          <h2 style="font-family: 'MaplestoryOTFBold';">{{ bookTitle }}</h2>
        </div>
        <mdb-input label="Page Number" v-model="phrasedata.page" icon="sticky-note" class="mb-5" style="font-family: 'MaplestoryOTFBold';"/>
        <mdb-input type="textarea" outline :rows="2" label="Phrase" icon="comment"  v-model="phrasedata.content" style="font-family: 'MaplestoryOTFBold';" />
      </mdb-modal-body>
      <mdb-modal-footer center>
        <mdb-btn @click="sendPhrase" outline="warning">Send <mdb-icon icon="paper-plane" class="ml-1"/></mdb-btn>
        <mdb-btn @click.native="header = false" outline="primary">Close <mdb-icon icon="times" class="ml-1" style="color:blue"/></mdb-btn>
      </mdb-modal-footer>
    </mdb-modal>
    </mdb-container>
  
</template>

<script>
import { mdbContainer, mdbBtn, mdbModal, mdbModalHeader, mdbModalBody, mdbInput, mdbModalFooter, mdbModalTitle, mdbIcon } from 'mdbvue';
import axios from "axios";

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
    },
    data() {
      return {
        header: false,
        bookTitle: null,
        feedback:'',
        phrasedata:{
          content:null,
          page:null,
        },
      };
    },
    methods:{
      sendPhrase(){
        axios.post(`${process.env.VUE_APP_SERVER_URL}/phrase/create`, this.phrasedata)
        .then((res)=>{
          console.log(res);
          this.header=false;
          this.$emit('sendPhrase',res.data);
        })
        .catch((err)=>{
          console.log(err);
        });
      },
    },
    props:{
      booktitle2:String,
    }
};
</script>

<style scoped>

</style>