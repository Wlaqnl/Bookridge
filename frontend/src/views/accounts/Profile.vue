<template>
  <div id="main d-flex flex-row" class="my-5 bg">
    <transition name="fade">
      <div id="element" class="loading" v-show="isLoading">
        <div class="fa-3x">
          <i class="fas fa-spinner fa-spin"></i> Loading
        </div>
      </div>
    </transition>
    <v-container class="mx-auto" style="min-width: 1000px;">
      <v-tabs vertical>
        <v-container class="pt-0">
          <v-card class="mx-auto text-center pt-5" width="250">
            <v-img
              src="@/assets/img/profile/profile.png"
              aspect-ratio="1"
              width="200"
              height="200"
              contain
              class="mx-auto"
              style="position: relative;"
            ></v-img>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-subtitle width="250" v-show="name">{{ this.name }}님의 프로필</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-tab @click="toTop">
              <v-icon left>mdi-account</v-icon>상세 프로필
            </v-tab>
            <v-tab @click="toTop">
              <v-icon left>mdi-lead-pencil</v-icon>독서기록
            </v-tab>
            <v-tab @click="toTop">
              <v-icon left>mdi-bookshelf</v-icon>나의서재
            </v-tab>
            <v-tab @click="toTop">
              <v-icon left>mdi-book-open-page-variant</v-icon>독서성향
            </v-tab>
            <v-tab @click="toTop" v-if="!social" v-cloak>
              <!-- v-if="isYou && social == 0"  -->
              <v-icon left>mdi-account-lock</v-icon>비밀번호 수정
            </v-tab>
            <v-tab @click="toTop">
              <!-- v-if="isYou && social == 0"  -->
              <v-icon left>mdi-account-remove</v-icon>회원 탈퇴
            </v-tab>
          </v-card>
        </v-container>
        <!-- 상세 프로필 -->
        <v-tab-item>
          <v-card height="100%" color>
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row>
                  <v-col cols="9">
                    <h2>프로필 정보</h2>
                  </v-col>
                  <v-col cols="3" class="text-right">
                    <v-btn
                      @click="updateNow = true"
                      class="ma-2"
                      outlined
                      color="#34495e"
                      v-show="isYou && !updateNow && !!social"
                    >프로필 수정</v-btn>
                    <v-dialog
                      v-model="dialogPw"
                      @keydown.esc="closeDialog"
                      persistent
                      width="400"
                      height="270"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          class="ma-2"
                          outlined
                          color="#34495e"
                          v-show="isYou && !updateNow && !social"
                          v-bind="attrs"
                          v-on="on"
                        >프로필 수정</v-btn>
                      </template>
                      <v-card width="400" height="270">
                        <v-card-title class="headline green lighten-4 justify-content-center">프로필 수정</v-card-title>
                        <v-card-text class="p-3 mt-5">
                          <h6>프로필 수정을 위해 비밀번호를 입력해주세요.</h6>
                          <v-text-field
                            v-model="password"
                            color="deep-purple"
                            label="비밀번호를 입력해주세요."
                            type="password"
                            clearable
                          ></v-text-field>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="success" text @click="checkPassword(0), dialogPw = false">확인</v-btn>
                          <v-btn color="error" text @click="closeDialog">취소</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-col>
                </v-row>
                <v-list two-line subheader>
                  <!-- <v-subheader inset>상세 프로필</v-subheader> -->
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-tag-text-outline</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title>이름</v-list-item-title>
                          <v-list-item-subtitle v-show="updateNow">필수정보입니다.</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6 v-show="!updateNow">{{ name }}</h6>
                          <v-form ref="form1" v-model="validName" class="form-width">
                            <v-text-field
                              :rules="nameRules"
                              v-show="updateNow"
                              v-model="newName"
                              clearable
                              label="이름을 입력해주세요."
                              outlined
                            ></v-text-field>
                          </v-form>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1" class="px-0">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-face</v-icon>
                          <v-icon class="pr-5">mdi-face-woman</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title>성별</v-list-item-title>
                          <v-list-item-subtitle v-show="updateNow">필수정보입니다.</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6 v-show="!updateNow && isYou">{{ newGender }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkGender=='공개'">{{ newGender }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkGender=='비공개'">비공개 입니다.</h6>
                          <v-select
                            v-show="updateNow"
                            v-model="newGender"
                            :items="genders"
                            :rules="[v => !!v || '성별을 입력해주세요.']"
                            label="성별"
                            required
                          ></v-select>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="3" class="text-right">
                        <v-list-item-action>
                          <v-btn-toggle
                            v-show="updateNow"
                            v-model="checkGender"
                            tile
                            color="deep-purple accent-3"
                            group
                          >
                            <v-btn value="공개">공개</v-btn>
                            <v-btn value="비공개">비공개</v-btn>
                          </v-btn-toggle>
                        </v-list-item-action>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-cake-variant</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title>생년월일</v-list-item-title>
                          <v-list-item-subtitle v-show="updateNow">필수정보입니다.</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6 v-show="!updateNow && isYou">{{ newBirth }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkBirth=='공개'">{{ newBirth }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkBirth=='비공개'">비공개 입니다.</h6>
                          <v-menu
                            ref="menu"
                            v-model="menu"
                            :close-on-content-click="false"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-show="updateNow"
                                v-model="newBirth"
                                label="생년월일을 입력해주세요."
                                readonly
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              v-show="updateNow"
                              ref="picker"
                              v-model="newBirth"
                              :max="new Date().toISOString().substr(0, 10)"
                              min="1950-01-01"
                              @change="save"
                            ></v-date-picker>
                          </v-menu>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="3" class="text-right">
                        <v-list-item-action>
                          <v-btn-toggle
                            v-show="updateNow"
                            v-model="checkBirth"
                            tile
                            color="deep-purple accent-3"
                            group
                          >
                            <v-btn value="공개">공개</v-btn>
                            <v-btn value="비공개">비공개</v-btn>
                          </v-btn-toggle>
                        </v-list-item-action>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-map-marker</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title>주소</v-list-item-title>
                          <v-list-item-subtitle v-show="updateNow">필수정보입니다.</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6 v-show="!updateNow && isYou">{{ address }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkAddress=='공개'">{{ address }}</h6>
                          <h6 v-show="!updateNow && !isYou && checkAddress=='비공개'">비공개 입니다.</h6>

                          <v-text-field
                            v-show="updateNow"
                            type="text"
                            id="sample5_address"
                            placeholder="주소를 검색해주세요."
                            disabled
                          ></v-text-field>
                          <input
                            width="100"
                            v-show="updateNow"
                            type="button"
                            onclick="sample5_execDaumPostcode()"
                            value="주소 검색"
                            class="mr-3 address-btn"
                          />
                          <!-- longitude -->
                          <v-text-field type="text" v-show="hide" id="x" placeholder="주소" disabled></v-text-field>
                          <!-- latitude -->
                          <v-text-field type="text" v-show="hide" id="y" placeholder="주소" disabled></v-text-field>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="3" class="text-right">
                        <v-list-item-action>
                          <v-btn-toggle
                            v-show="updateNow"
                            v-model="checkAddress"
                            tile
                            color="deep-purple accent-3"
                            group
                          >
                            <v-btn value="공개">공개</v-btn>
                            <v-btn value="비공개">비공개</v-btn>
                          </v-btn-toggle>
                        </v-list-item-action>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
                <div class="text-center w-100" v-show="updateNow">
                  <v-btn
                    text
                    outlined
                    :disabled="!validName"
                    color="success"
                    @click="saveProfile"
                  >프로필 저장</v-btn>
                  <v-btn text outlined color="error" dark @click="cancelProfile()" class="mx-1">취소</v-btn>
                </div>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <!-- 독서 기록 -->
        <v-tab-item>
          <v-card>
            <v-card-text class="text-center">
              <v-row>
                <v-col>
                  <h2 class="my-5">독서 기록</h2>
                </v-col>
                <v-col class="mt-5">
                  <v-btn text outlined @click="testdelete">삭제</v-btn>
                  <v-dialog v-model="dialogCalendar" persistent max-width="600px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn text outlined v-bind="attrs" v-on="on">도서 추가하기</v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">도서 추가하기</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-text-field required></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                        <v-form ref="form" v-model="valid" lazy-validation>
                          <v-container>
                            <v-row>
                              <v-col cols="12" md="3" sm="6">
                                <v-menu
                                  ref="menuStart"
                                  v-model="menuStart"
                                  :close-on-content-click="false"
                                  :return-value.sync="Sdate"
                                  transition="scale-transition"
                                  offset-y
                                  min-width="290px"
                                >
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-text-field
                                      v-model="Sdate"
                                      label="독서 시작 날짜"
                                      required
                                      readonly
                                      :rules="[rules.startDate]"
                                      v-bind="attrs"
                                      v-on="on"
                                    ></v-text-field>
                                  </template>
                                  <v-date-picker
                                    v-model="Sdate"
                                    no-title
                                    scrollable
                                    :max="SDateMax"
                                  >
                                    <v-spacer></v-spacer>
                                    <v-btn text color="primary" @click="menuStart = false">Cancel</v-btn>
                                    <v-btn
                                      text
                                      color="primary"
                                      @click="$refs.menuStart.save(Sdate)"
                                    >OK</v-btn>
                                  </v-date-picker>
                                </v-menu>
                              </v-col>
                              <v-col cols="12" md="3" sm="6">
                                <v-menu
                                  ref="menuEnd"
                                  v-model="menuEnd"
                                  :close-on-content-click="false"
                                  :return-value.sync="Edate"
                                  transition="scale-transition"
                                  offset-y
                                  min-width="290px"
                                >
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-text-field
                                      v-model="Edate"
                                      label="독서 마감 날짜"
                                      required
                                      readonly
                                      :rules="[rules.endDate]"
                                      v-bind="attrs"
                                      v-on="on"
                                    ></v-text-field>
                                  </template>
                                  <v-date-picker
                                    v-model="Edate"
                                    :min="EDateMin"
                                    :max="EDateMax"
                                    no-title
                                    scrollable
                                  >
                                    <v-spacer></v-spacer>
                                    <v-btn text color="primary" @click="menuEnd = false">Cancel</v-btn>
                                    <v-btn
                                      text
                                      color="primary"
                                      @click="$refs.menuEnd.save(Edate)"
                                    >OK</v-btn>
                                  </v-date-picker>
                                </v-menu>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-form>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="dialogCalendar = false, test()">저장</v-btn>
                        <v-btn color="blue darken-1" text @click="dialogCalendar = false">취소</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-col>
              </v-row>
            </v-card-text>
            <v-row>
              <v-col>
                <v-date-picker
                  v-model="date"
                  :landscape="$vuetify.breakpoint.smAndUp"
                  :event-color="date => date ? 'red' : 'yellow'"
                  :events="calendarEvents"
                  class="mt-4"
                ></v-date-picker>
              </v-col>
              <v-col></v-col>
            </v-row>
          </v-card>
        </v-tab-item>
        <!-- 나의서재 -->
        <v-tab-item>
          <v-card>
            <v-card-text class="text-center">
              <v-row>
                <v-col>
                  <h2 class="my-5">나의 서재</h2>
                </v-col>
              </v-row>
            </v-card-text>
            <v-tabs background-color="white" color="deep-purple accent-4" centered>
              <v-tab>좋아요</v-tab>
              <v-tab>독후감</v-tab>
              <v-tab>문장</v-tab>

              <v-tab-item>
                <v-container fluid>
                  <v-row>
                    <v-col v-for="i in 6" :key="i" cols="12" md="4">
                      <v-img
                        :src="`https://picsum.photos/500/300?image=${i * 5 + 10}`"
                        :lazy-src="`https://picsum.photos/10/6?image=${i * 5 + 10}`"
                        aspect-ratio="1"
                      ></v-img>
                    </v-col>
                  </v-row>
                </v-container>
              </v-tab-item>
              <v-tab-item>
                <v-container fluid>
                  <v-row>
                    <v-col v-for="i in 6" :key="i" cols="12" md="4">
                      <v-img
                        :src="`https://picsum.photos/500/300?image=${i * 6 + 10}`"
                        :lazy-src="`https://picsum.photos/10/6?image=${i * 6 + 10}`"
                        aspect-ratio="1"
                      ></v-img>
                    </v-col>
                  </v-row>
                </v-container>
              </v-tab-item>
              <v-tab-item>
                <v-container fluid>
                  <v-row>
                    <v-col v-for="i in 6" :key="i" cols="12" md="4">
                      <v-img
                        :src="`https://picsum.photos/500/300?image=${i * 7 + 10}`"
                        :lazy-src="`https://picsum.photos/10/6?image=${i * 7 + 10}`"
                        aspect-ratio="1"
                      ></v-img>
                    </v-col>
                  </v-row>
                </v-container>
              </v-tab-item>
            </v-tabs>
          </v-card>
        </v-tab-item>
        <!-- 독서 성향 -->
        <v-tab-item>
          <v-card height="100%" color>
            <v-card-text>
              <v-container>
                <v-row class="d-flex justify-content-center">
                  <h2 class="my-5">독서 성향</h2>
                </v-row>
                <v-row>
                  <v-col cols="8">
                    <mdb-radar-chart
                      :data="radarChartData"
                      :options="radarChartOptions"
                      :width="600"
                      :height="300"
                    ></mdb-radar-chart>
                  </v-col>
                  <v-col cols="4">
                    <h4>{{ name }}님의 선호 장르</h4>
                    <v-list nav dense>
                      <v-list-item-group color="primary">
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>1위</v-list-item-title>
                          </v-list-item-content>
                          <v-list-item-content>
                            <v-list-item-title>소설</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>2위</v-list-item-title>
                          </v-list-item-content>
                          <v-list-item-content>
                            <v-list-item-title>시</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>3위</v-list-item-title>
                          </v-list-item-content>
                          <v-list-item-content>
                            <v-list-item-title>컴퓨터/IT</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>4위</v-list-item-title>
                          </v-list-item-content>
                          <v-list-item-content>
                            <v-list-item-title>과학</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>5위</v-list-item-title>
                          </v-list-item-content>
                          <v-list-item-content>
                            <v-list-item-title>사회</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list-item-group>
                    </v-list>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="8">
                    <mdb-line-chart
                      :data="lineChartData"
                      :options="lineChartOptions"
                      :width="600"
                      :height="300"
                    ></mdb-line-chart>
                  </v-col>
                  <v-col cols="4">
                    <h4>{{ name }}님의 독서 그래프</h4>
                  </v-col>
                </v-row>
                <v-img src="@/assets/img/profile/booktype.png" width="700" height="300" contain></v-img>
                <v-row class="d-flext justify-content-center">
                  <h5 class="my-5">당신의 독서 취향은 OOO입니다.</h5>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- 비밀번호 수정 -->
        <v-tab-item v-if="!social">
          <v-card height="100%" color>
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row>
                  <v-col cols="9">
                    <h2>비밀번호 수정</h2>
                  </v-col>
                  <v-col cols="3" class="text-right">
                    <v-dialog
                      v-model="dialogChangePw"
                      @keydown.esc="dialogChangePw = false"
                      persistent
                      width="450"
                      height="280"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          class="ma-2"
                          outlined
                          color="indigo"
                          v-bind="attrs"
                          v-on="on"
                          v-show="isYou && !updatePwNow && !social"
                        >비밀번호 수정</v-btn>
                      </template>
                      <v-card width="450" height="280">
                        <v-card-title
                          class="headline green lighten-4 justify-content-center"
                        >비밀번호 수정</v-card-title>
                        <v-card-text class="p-3 mt-5">
                          <h6>비밀번호 수정을 위해 현재 비밀번호를 입력해주세요.</h6>
                          <v-text-field
                            v-model="password"
                            color="deep-purple"
                            label="비밀번호를 입력해주세요."
                            type="password"
                            clearable
                          ></v-text-field>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            color="success"
                            text
                            @click="checkPassword(1), dialogChangePw = false"
                          >확인</v-btn>
                          <v-btn color="error" text @click="dialogChangePw = false, password=''">취소</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-col>
                </v-row>
                <div class="my-5">
                  <v-sheet color :outlined="true" class="py-5">
                    <h5 class="px-5 mb-5 text-blue">비밀번호 수정 안내</h5>
                    <h6
                      class="px-5"
                      v-show="!updatePwNow"
                    >비밀번호 수정을 원하시면 "비밀번호 수정" 버튼을 클릭하여 비밀번호를 인증해주세요.</h6>
                  </v-sheet>
                </div>
                <v-list two-line subheader v-show="updatePwNow">
                  <v-card>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="3" class="mt-5">새 비밀번호1</v-col>
                          <v-col cols="9">
                            <v-text-field
                              v-model="newPassword1"
                              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                              :rules="rulesPw"
                              :type="show1 ? 'text' : 'password'"
                              label="변경할 비밀번호를 입력해주세요."
                              hint="최소 8자 이상으로 비밀번호를 설정해주세요."
                              counter
                              @click:append="show1 = !show1"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="3" class="mt-5">새 비밀번호2</v-col>
                          <v-col cols="9">
                            <v-text-field
                              v-model="newPassword2"
                              :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                              :rules="rulesPw"
                              :type="show2 ? 'text' : 'password'"
                              label="한 번 더 입력해주세요."
                              hint="최소 8자 이상으로 비밀번호를 설정해주세요."
                              counter
                              @click:append="show2 = !show2"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                  </v-card>
                  <div class="d-flex justify-content-center my-5">
                    <v-btn
                      class="ma-2"
                      outlined
                      color="success"
                      text
                      @click="updatePassword"
                      v-if="newPassword1.length > 7 && newPassword2.length > 7 && newPassword1 === newPassword2"
                    >저장</v-btn>
                    <v-btn color="success" class="ma-2" outlined disabled v-else>저장</v-btn>
                    <v-btn @click="updatePwNow = false" class="ma-2" outlined color="error">취소</v-btn>
                  </div>
                </v-list>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card height="100%">
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row>
                  <v-col cols="9">
                    <h2>회원 탈퇴</h2>
                  </v-col>
                  <v-col cols="3" class="text-right"></v-col>
                </v-row>
                <div class="text-center my-5 table-cell">
                  <v-sheet color="grey lighten-2" class="px-3 py-5 vertical" min-height="200px">
                    <h4 class="mt-5 pt-5">{{ name }}님의 {{ email }} 계정을 탈퇴합니다.</h4>
                    <h4 class="mt-5">회원 탈퇴가 완료되면 회원님의 개인정보는 즉시 삭제됩니다.</h4>
                  </v-sheet>
                </div>
                <div class="my-5">
                  <v-sheet color :outlined="true" class="py-5">
                    <h5 class="pl-5 mb-5 text-blue">탈퇴 전 주의사항</h5>
                    <p class="pl-5">1. 삭제된 데이터는 복구할 수 없습니다.</p>
                    <p class="pl-5">2. 해당 아이디로 작성된 게시물은 삭제되지 않습니다.</p>
                  </v-sheet>
                </div>
                <div class="text-center">
                  <v-dialog
                    width="500"
                    v-model="dialogDeleteAccount"
                    @keydown.esc="dialogSecurityAccount = false"
                    persistent
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        class="ma-2"
                        outlined
                        color="rgba-teal-strong"
                        v-bind="attrs"
                        v-on="on"
                        v-show="isYou"
                      >회원 탈퇴</v-btn>
                    </template>
                    <v-card width="500" min-height="300">
                      <v-card-title class="headline green lighten-4 justify-content-center">회원 탈퇴</v-card-title>
                      <v-card-text class="p-3 mt-5">
                        <h5>정말 탈퇴를 진행하시겠습니까?</h5>
                        <span v-show="!social">회원 탈퇴 희망시 비밀번호를 입력해주세요.</span>
                        <span v-show="!!social">회원 탈퇴 희망시 '확인' 버튼을 클릭해주세요.</span>
                        <br />
                        <br />
                        <span class="mb-5">주의) 한 번 진행하면 되돌릴 수 없습니다.</span>
                        <v-text-field
                          v-show="!social"
                          v-model="password"
                          color="deep-purple"
                          label="비밀번호를 입력해주세요."
                          type="password"
                          clearable
                        ></v-text-field>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <!-- !!!!!!!!!!!!! -->
                        <v-btn
                          v-show="!social"
                          color="success"
                          text
                          @click="checkPassword(2), dialogDeleteAccount = false"
                        >확인</v-btn>
                        <v-btn
                          v-show="!!social"
                          color="success"
                          text
                          @click="deleteAccount(), dialogDeleteAccount = false"
                        >확인</v-btn>
                        <v-btn
                          color="error"
                          text
                          @click="dialogDeleteAccount = false, password=''"
                        >취소</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </div>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-container>
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
import { mdbRadarChart, mdbLineChart } from "mdbvue";
import swal from "sweetalert";
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "Profile",
  components: { mdbRadarChart, mdbLineChart },

  // watch: {
  // dialog(val) {
  //   val || this.close();
  // },

  // },
  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      // swal("잘못된 접근입니다.1");
    } else {
      next();
    }
  },
  computed: {
    SDateMax() {
      return new Date().toISOString().split("T")[0];
    },
    EDateMin() {
      // 컨퍼런스를 생성하는 경우 시작일 제한
      if (this.Sdate == "") {
        return new Date().toISOString().split("T")[0];
      } else {
        return this.Sdate;
      }
    },
    EDateMax() {
      console.log(new Date().toISOString().split("T")[0]);
      return new Date().toISOString().split("T")[0];
    },
  },
  mounted() {
    this.arrayEvents = [...Array(6)].map(() => {
      const day = Math.floor(Math.random() * 30);
      const d = new Date();
      d.setDate(day);
      return d.toISOString().substr(0, 10);
    });
  },

  data() {
    return {
      rules: {
        startDate(val) {
          if (val) return true;
          else return "시작날짜를 선택해주세요.";
        },
        endDate(val) {
          if (val) return true;
          else return "종료날짜를 선택해주세요.";
        },
      },
      valid: false,
      startDates: ["2020-09-21", "2020-09-22"],
      endDates: ["2020-09-24", "2020-09-01"],
      arrayEvents: null,
      date: new Date().toISOString().substr(0, 10),
      Sdate: "",
      Edate: "",
      lineChartData: {
        labels: [
          "1월",
          "2월",
          "3월",
          "4월",
          "5월",
          "6월",
          "7월",
          "8월",
          "9월",
          "10월",
          "11월",
          "12월",
        ],
        datasets: [
          {
            label: "2020",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [65, 59, 80, 81, 56, 55, 40, 10, 20, 30, 20, 25],
          },
        ],
      },
      lineChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
      radarChartData: {
        labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        datasets: [
          {
            label: "My First dataset",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [65, 59, 90, 81, 56, 55, 40, 35, 52],
          },
        ],
      },
      radarChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
      },
      validName: true,
      nameRules: [
        (v) => !!v || "이름은 필수값입니다.",
        (v) => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요.",
      ],
      dialgotest: false,
      isLogin: true,
      checkGender: "공개",
      checkGender2: "공개",
      checkBirth: "공개",
      checkBirth2: "공개",
      checkAddress: "공개",
      checkAddress2: "공개",

      visible: false,
      index: 0,

      show1: false,
      show2: false,

      rulesPw: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],

      genders: ["남자", "여자"],
      afterProfileImg: null,
      profileImgUrl: null,

      // 개인정보
      userPk: "", // 로그인한 회원
      name: "", // 닉네임
      newName: "", // 새로운 닉네임

      email: null,

      birth: null,
      newBirth: null,
      menu: false,
      menuStart: false,
      menuEnd: false,

      nowPassword: null,
      password: null, // 기존비밀번호
      newPassword1: "", // 새로운 비밀번호1
      newPassword2: "", // 새로운 비밀번호2

      gender: null,
      newGender: null,

      hide: false,
      longitude: null,
      latitude: null,

      address: null,
      newAddress: null,

      social: null,

      profileImg: null,

      // dialog 모음
      dialogCalendar: false,
      dialogPI: false,
      dialogBirth: false,
      // 프로필 수정시 비밀번호 물어보는 dialog
      dialogPw: false,
      // 개인보안 dialog
      dialogSecurityAccount: false,
      // 비밀번호 수정 dialog
      dialogChangePw: false,
      // 회원탈퇴 dialog
      dialogDeleteAccount: false,
      // 본인일치여부
      isYou: false,

      // 수정 여부
      updateNow: false,
      updatePwNow: false,

      // 스크롤
      fab: false,

      // 탭
      tab: null,

      // 기본정보 값
      isLoading: false,
      nextItem: 1,
      // pagination
      perPage: 5,
      currentPage: 1,
      start: 0,
      end: 5,
    };
  },
  created() {
    // this.isLoading = true;
    this.isLogin = VueCookies.get("jwt_token") ? true : false;
    this.userPk = this.$route.params.pk; // userPk
    // 본인 일치치여부 확인
    if (VueCookies.get("user_pk") == this.userPk) {
      this.isYou = true;
    }

    // 프로필 정보 가져오기
    axios
      .get(
        `${process.env.VUE_APP_SERVER_URL}/accounts/profile/${this.$route.params.pk}/`,
        {
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        }
      )
      .then((res) => {
        // console.log("회원정보 가져오기");
        // console.log(res);
        this.name = res.data.name;
        this.newName = res.data.name;

        this.email = res.data.email;

        this.gender = res.data.gender == 0 ? "남자" : "여자";
        this.newGender = this.gender;

        this.birth = res.data.birth;
        this.newBirth = this.birth;

        document.getElementById("sample5_address").value = res.data.address;
        this.address = res.data.address;

        document.getElementById("x").value = res.data.latitude;
        this.latitude = res.data.latitude;
        document.getElementById("y").value = res.data.longitude;
        this.longitude = res.data.longitude;

        this.social = res.data.social;

        this.checkGender = res.data.privacy.gender == 0 ? "공개" : "비공개";
        this.checkBirth = res.data.privacy.birth == 0 ? "공개" : "비공개";
        this.checkAddress = res.data.privacy.address == 0 ? "공개" : "비공개";
      })
      .catch((err) => {
        console.log(err);
        console.log("너니?");
      });
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
    date() {
      console.log("#########");
    },
    checkGender() {
      if (this.checkGender) {
        this.checkGender2 = this.checkGender;
      } else {
        this.checkGender = this.checkGender2;
      }
      console.log(this.checkGender);
      console.log(this.checkGender2);
    },
    checkBirth() {
      console.log(this.checkGender);
    },
    checkAddress() {
      console.log(this.checkGender);
    },
  },

  methods: {
    testdelete() {
      axios.delete(`${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`,
      { 
        params: {calendar_pk:1},
        headers: { Authorization: VueCookies.get("jwt_token") }
      }
      )
      .then(res => {
        console.log(res)
      })
      .catch(err => {
        console.log(err)
      })
    },
    test() {
      console.log(this.Sdate);
      console.log(this.Edate);
      axios
        .put(
          `${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`,
          {
            start_date: this.Sdate,
            end_date: this.Edate,
            book_pk: 1,
          },
          {
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    calendarEvents(date) {
      // console.log(date)
      // for (const day of this.test) {
      // console.log(day);
      // }
      // console.log(date)
      console.log(this.date);

      for (var i = 0; i < this.startDates.length; i++) {
        if (this.startDates[i] == date) {
          return true;
        }
      }
      for (var j = 0; j < this.endDates.length; j++) {
        if (this.endDates[j] == date) {
          return ["yellow"];
        }
      }
      // for (const day in date) {
      // console.log(day)
      // }
      // const [, , day] = date.split("-");
      // console.log([, , day]);
      // const [, month] = date.split("-");
      // const [year, ,] = date.split("-");
      // console.log(date)
      // if (date) return true;
      // console.log([12, 17, 28].includes(parseInt(day, 10)))
      // if (date) return ["red", "green"];
      return false;
    },
    save(date) {
      this.$refs.menu.save(date);
    },
    showLightbox(index) {
      this.index = index;
      this.visible = true;
    },
    handleHide() {
      this.visible = false;
    },

    deleteAccount() {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/accounts/unlink/`, {
          // social_id: VueCookies.get("social_id"),
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then((res) => {
          VueCookies.keys().forEach((cookie) => VueCookies.remove(cookie));
          console.log(res);
          swal("정상적으로 회원탈퇴 되었습니다.");
          this.$router.push("/");
          this.$router.go();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    // 프로필 페이지로 이동
    goToProfile(userId) {
      this.$router.push({
        name: "Profile",
        params: { id: userId },
      });
    },
    // 프로필 이미지 저장
    saveProfileImage() {
      // var frm = new FormData();
      // var photoFile = this.afterProfileImg[0];
      // frm.append("file", photoFile);
      // frm.append("userNo", this.userNumber);
      // axios
      //   .post(`${process.env.VUE_APP_SERVER_URL}/user/setprofile`, frm, {
      //     headers: {
      //       "Content-Type": "multipart/form-data",
      //     },
      //   })
      //   .then((res) => {
      //     this.dialogPI = false;
      //   });
      // alert("저장이 완료되었습니다.");
      // this.$router.go();
    },

    // 프로필사진 취소
    cancelProfileImage() {
      this.profileImgUrl = this.profileImg;
      this.dialogPI = false;
    },
    // 이미지 업로드
    onClickImageUpload() {
      this.$refs.imageInput.click();
    },

    // 프로필 이미지 변경
    onChangeProfileImages(e) {
      const file = e.target.files[0]; // Get first index in files
      this.profileImgUrl = URL.createObjectURL(file); // Create File URL
      this.afterProfileImg = e.target.files;
    },

    // 모달 닫는 부분
    closeDialog() {
      this.dialogPw = false;
      this.dialogChangePw = false;
      this.password = "";
      this.newPassword1 = "";
      this.newPassword2 = "";
    },

    // 비밀번호 일치여부 확인 후 상태변화
    // flag 0 = 프로필 수정 | flag 1 = 비밀번호 수정 | flag 2 = 회원 탈퇴
    checkPassword(flag) {
      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/accounts/password/${this.userPk}/`,
          {
            params: {
              password: this.password,
            },
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then((res) => {
          if (res.data.result) {
            if (flag == 0) {
              this.updateNow = true;
              this.password = "";
            } else if (flag == 1) {
              this.updatePwNow = true;
              this.nowPassword = this.password;
              this.password = "";
            } else if (flag == 2) {
              this.password = "";
              this.deleteAccount();
            }
          } else {
            this.password = "";
            swal("비밀번호가 일치하지 않습니다. 다시 시도해주세요.");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 비밀번호 수정
    updatePassword() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/password/${this.userPk}/`,
          {
            password: this.nowPassword,
            password1: this.newPassword1,
            password2: this.newPassword2,
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then(() => {
          swal("비밀번호가 변경되었습니다.");
          this.updatePwNow = false;
          this.password = "";
          this.newPassword1 = "";
          this.newPassword2 = "";
        })
        .catch((err) => {
          console.log(err);
        });
    },

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

    // 프로필 저장
    saveProfile() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/profile/${this.userPk}/`,
          {
            email: this.email,
            birth: this.newBirth,
            name: this.newName,
            address: document.getElementById("sample5_address").value,
            latitude: document.getElementById("x").value,
            longitude: document.getElementById("y").value,
            gender: this.newGender == "남자" ? 0 : 1,
            social: this.social,
            social_id: VueCookies.get("social_id"),
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then((res) => {
          (this.birth = this.newBirth),
            (this.name = this.newName),
            (this.address = document.getElementById("sample5_address").value),
            (this.latitude = document.getElementById("x").value),
            (this.longitude = document.getElementById("y").value),
            (this.gender = this.newGender == "남자" ? 0 : 1);
          console.log("수정 후 데이터");
          console.log(res);

          swal("성공적으로 저장되었습니다.");
          this.updateNow = false;
          this.$router.go();
        });
      // 공개 비공개 여부 axios요청
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/privacy/${this.userPk}/`,

          {
            birth: this.checkBirth == "공개" ? 0 : 1,
            name: 1,
            address: this.checkAddress == "공개" ? 0 : 1,
            gender: this.checkGender == "공개" ? 0 : 1,
            calendar: 1,
            favorite: 1,
            review: 1,
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 프로필 수정 취소
    cancelProfile() {
      this.updateNow = !this.updateNow;
      //   this.profileImgUrl = this.profileImg;
      this.newName = this.name;
      this.newGender = this.gender;
      this.newBirth = this.birth;
      document.getElementById("sample5_address").value = this.address;
      document.getElementById("x").value = this.latitude;
      document.getElementById("y").value = this.longitude;
      swal("프로필 수정이 취소되었습니다.");
      this.$router.go();
    },

    // 개인보안 수정 취소
    cancelSecurity() {
      this.updatePwNow = false;
      swal("취소되었습니다.");
    },

    onClickPage() {
      //   const n = event.target.dataset.page;
      //   this.start = (n - 1) * 5;
      //   this.end = n * 5;
    },
  },
};
</script>

<style scoped>
body,
html {
  height: 100%;
}

.bg {
  /* background-image: url("../src/assets/img/signup.png"); */
  /* background: url("../../assets/img/books.png"); */
  /* height: 100%; */
  /* background-position: center; */
  /* background-repeat: no-repeat; */
  /* background-size: cover; */
}
.vertical {
  vertical-align: middle;
}
[v-clock] {
  display: none;
}
.v-tabs-slider {
  background-color: white;
}
.address-btn {
  font-size: 15px;
  width: 50;
  background-color: white;

  color: green;
  padding: 6px 14px;

  margin: 4px 2px;
  cursor: pointer;
}
.address-btn:hover {
  opacity: 0.9;
  border: none;
  border-radius: 5px;
  box-shadow: 0.5px 0.5px 0.5px 0.5px #bdbdbd;
}

.text-blue {
  color: #42a5f5;
}
</style>