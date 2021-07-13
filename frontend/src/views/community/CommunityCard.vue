<template>
  <div>
    <v-app>
      <v-card  max-width="700px">
        <v-row>
          <v-col cols="5" style="margin-left:2%">
            <v-card class="d-inline-block mx-auto">
              <v-container>
                <v-row justify="space-between">
                  <v-col cols="auto">
                    <v-img
                      height="270"
                      width="200"
                      src="https://cdn.vuetifyjs.com/images/cards/store.jpg"
                    ></v-img>
                  </v-col>
                </v-row>
                <v-row
                  class="d-flex justify-content-center"
                  style="margin-left:2%; "
                >
                  <h3 style="font-family: HangeulNuri-Bold">Book Title</h3>
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
                      <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <v-btn icon>
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
                    class="headline"
                    style="font-family: HangeulNuri-Bold"
                    >USER ID</v-list-item-title
                  >
                  <v-list-item-subtitle style="font-family: HangeulNuri-Bold"
                    >20.09.23</v-list-item-subtitle
                  >
                </v-list-item-content>
              </v-list-item>
              <v-card-text style="margin-left:2%">
                <h4 style="font-family: HangeulNuri-Bold">Review Title</h4>
                <br />
                <p style="font-family: HangeulNuri-Bold">Review Content</p>
              </v-card-text>
            </div>
            <div class="bottomIcon">
              <v-row>
                <v-btn icon>
                  <v-icon>mdi-bookmark</v-icon>
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
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-app>
  </div>
</template>

<script>
import { mdbRating } from "mdbvue";
export default {
  components: {
    mdbRating,
  },
  data() {
    return {
      dialog: false,
      star: null,
    };
  },
};
</script>

<style scoped>
.bottomIcon {
  align-self: flex-end;
}
@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
</style>
