<template>
  <div>
    <div class="nobook">
      <br />
      <h1 style="text-align:center">검색하신 도서는 없습니다.</h1>
      <!-- <mdb-btn gradient="blue">
        관리자에게 문의하기
        <i class="fas fa-exclamation"></i>
      </mdb-btn> -->
    </div>
  </div>
</template>

<script>
// import { mdbBtn } from "mdbvue";

export default {
  components: {
    // mdbBtn,
  },
};
</script>

<style scoped>
.nobook {
  background-image: url("/src/assets/img/물음표.png");
  text-align: center;
}
</style>