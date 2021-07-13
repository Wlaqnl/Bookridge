<template>
  <div id="dmap" class="mt-5 mx-auto">
    <h1 class="my-5 text-center nohover">✏Signup</h1>
    <v-stepper v-model="e1" :alt-labels="true">
      <v-stepper-header>
        <v-stepper-step :complete="e1 > 1" step="1">기본정보</v-stepper-step>
        <v-divider></v-divider>

        <v-stepper-step :complete="e1 > 2" step="2">상세정보</v-stepper-step>
        <v-divider></v-divider>

        <v-stepper-step :complete="e1 > 3" step="3">좋아하는 장르</v-stepper-step>
        <v-divider></v-divider>

        <v-stepper-step step="4">좋아하는 책</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card class="mb-12" color height="100%" min-width="900px" min-height="700px">
            <v-container>
              <v-row class>
                <v-col>
                  <img src="https://picsum.photos/500/600" alt />
                </v-col>
                <v-col>
                  <v-form ref="form1" v-model="valid1" :lazy-validation="lazy1" class="form-width">
                    <v-row>
                      <!-- 이메일 -->
                      <v-col cols="5">
                        <v-text-field v-model="email" label="아이디" :rules="emailRules" required></v-text-field>
                      </v-col>
                      <v-col cols="4">
                        <v-text-field :disabled="true" placeholder="@bookridge.com"></v-text-field>
                      </v-col>
                      <v-col cols="3">
                        <v-btn
                          v-if="email == ''"
                          text
                          outlined
                          color="success"
                          :disabled="true"
                        >중복확인</v-btn>
                        <v-btn v-else text outlined color="success" @click="checkEmail">중복확인</v-btn>
                      </v-col>
                    </v-row>
                    <v-row class="ml-1">
                      <p
                        class="text-green text-caption"
                        v-if="checkedEmail == email && isCheckedEmail"
                      >사용가능한 아이디입니다.</p>
                      <p v-else class="text-red text-caption">아이디 중복확인이 필요합니다.</p>
                    </v-row>
                    <!-- 이름 -->
                    <v-text-field
                      v-model="name"
                      :counter="10"
                      :rules="nameRules"
                      label="이름"
                      required
                    ></v-text-field>
                    <!-- 비밀번호 -->
                    <v-text-field
                      v-model="password1"
                      :rules="password1Rules"
                      label="비밀번호"
                      required
                      counter
                      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show1 ? 'text' : 'password'"
                      @click:append="show1 = !show1"
                    ></v-text-field>
                    <v-text-field
                      v-model="password2"
                      :rules="password2Rules"
                      label="비밀번호 확인"
                      required
                      counter
                      :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show2 ? 'text' : 'password'"
                      @click:append="show2 = !show2"
                    ></v-text-field>
                    <v-divider></v-divider>
                    <div class="d-flex justify-end mt-5">
                      <v-btn
                        text
                        outlined
                        color="success"
                        :disabled="(!valid1) || (!isCheckedEmail)"
                        @click="e1 = 2"
                      >다음 단계</v-btn>
                    </div>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-card class="mb-12" color height="100%" min-width="900px" min-height="700px">
            <v-container>
              <v-row class>
                <v-col>
                  <img src="https://picsum.photos/500/600" alt />
                </v-col>
                <v-col>
                  <v-form ref="form2" v-model="valid2" :lazy-validation="lazy2" class="form-width">
                    <!-- 성별 -->
                    <v-select
                      v-model="gender"
                      :items="genders"
                      :rules="genderRules"
                      label="성별"
                      required
                      class="mb-3"
                    ></v-select>

                    <!-- 생년월일 -->
                    <v-menu
                      ref="menu"
                      v-model="menu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          :rules="birthdayRules"
                          v-model="birth"
                          label="생년월일"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        ref="picker"
                        v-model="birth"
                        :max="new Date().toISOString().substr(0, 10)"
                        min="1950-01-01"
                        @change="save"
                      ></v-date-picker>
                    </v-menu>
                    <!-- 주소 -->
                    <v-text-field
                      type="text"
                      v-model="address"
                      disabled
                      id="sample5_address"
                      :rules="addressRules"
                    ></v-text-field>
                    <v-text-field type="text" v-show="hide" id="x" placeholder="주소" disabled></v-text-field>
                    <v-text-field type="text" v-show="hide" id="y" placeholder="주소" disabled></v-text-field>
                    <input
                      ref="test"
                      type="button"
                      onclick="sample5_execDaumPostcode()"
                      value="주소 검색"
                      class="mr-3 address-btn"
                      uk-tooltip="버튼을 클릭해주세요."
                    />
                    <v-checkbox
                      v-model="checkbox"
                      :rules="agreeRules"
                      label="약관 동의"
                      required
                      @click="test"
                    ></v-checkbox>
                    <v-dialog v-model="dialogPolicy" width="700">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn text small color="primary" dark v-bind="attrs" v-on="on">서비스 이용 약관</v-btn>
                      </template>

                      <v-card width="700">
                        <v-card-title
                          class="headline grey lighten-2 d-flex justify-content-center"
                        >서비스 이용약관</v-card-title>
                        <v-card-text class="mt-5">저희 '북릿지' 서비스는 도서 추천 웹 서비스입니다.</v-card-text>
                        <v-card-text
                          class="mt-5"
                        >북릿지는 「개인정보보호법」 제30조(개인정보 처리방침의 수립 및 공개)에 따라 정보주체의 개인정보와 권익을 보호하고, 개인정보와 관련한 정보주체의 고충을 신속하고 원활하게 처리할 수 있도록 다음과 같이 개인정보 처리방침을 수립·공개합니다.</v-card-text>
                        <v-card-text
                          class="mt-5"
                        >이 방침은 별도의 설명이 없는 한 북릿지에서 처리하는 모든 개인정보 파일에 적용됩니다. 다만, 소관 업무 처리를 위해 각 부서에서 별도의 개인정보 처리방침을 제정·시행하는 경우 그 방침에 따르고 해당 부서가 운영하는 별도 홈페이지에 게시함을 알려드립니다.</v-card-text>
                        <v-card-text
                          class="mt-5"
                        >또한, 관련 법령에서 규정한 바에 따라 보유하고 있는 개인정보에 대한 열람청구권과 정정청구권 등 이용자의 권익을 존중합니다. 정보주체는 이러한 법령상 권익의 침해 등에 대하여 행정심판법이 정하는 바에 따라 행정심판을 청구할 수 있으며, 개인정보 분쟁조정위원회, 개인정보 침해신고센터 등에 분쟁해결이나 상담 등을 신청할 수 있습니다.</v-card-text>
                        <v-card-text class="mt-5">
                          <h4>
                            <v-icon>mdi-pencil</v-icon>제1조. 개인정보의 처리 목적·항목 및 보유기간
                          </h4>
                          <p>북릿지는 정보주체의 동의 또는 관련 법령에 따라 필요 최소한의 개인정보를 수집하며, 처리 목적 및 보유·이용기간 내에서 개인정보를 처리·보유합니다.</p>
                          <p>구미시는 법령에 따른 개인정보 보유·이용기간 또는 정보주체로부터 개인정보를 수집할 때 동의받은 보유·이용기간 내에서 개인정보를 처리·보유합니다.</p>
                        </v-card-text>
                        <v-card-text class="mt-5">
                          <h4>
                            <v-icon>mdi-pencil</v-icon>제2조. 개인정보의 제3자 제공에 관한 사항
                          </h4>
                          <p>북릿지는 원칙적으로 정보주체의 개인정보를 수집․이용 목적으로 명시한 범위 내에서 처리하며 이용자의 사전 동의 없이는 본래의 범위를 초과하여 처리하거나 제3자에게 제공하지 않습니다.</p>
                          <p>입력하신 개인정보는 오로지 추천 서비스를 위해 사용됨을 알립니다.</p>
                        </v-card-text>
                        <v-card-text class="mt-5">감사합니다.</v-card-text>

                        <v-divider></v-divider>

                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="primary" text @click="dialogPolicy = false">확인</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-divider></v-divider>
                    <div class="d-flex justify-end my-5">
                      <v-btn
                        text
                        outlined
                        class="mr-3"
                        color="success"
                        @click="e1 = 1"
                        v-show="!isSocial"
                      >이전 단계</v-btn>
                      <v-btn text outlined color="success" :disabled="!valid2" @click="e1 = 3">다음 단계</v-btn>
                    </div>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card class="mb-12" color height="100%" min-width="900px" min-height="700px">
            <v-container fluid>
              <h3 class="text-center">좋아하는 장르를 선택해주세요.</h3>
              <v-row>
                <v-col v-for="i in 6" :key="i" cols="12" md="4">
                  <v-img
                    :src="`https://picsum.photos/500/300?image=${i * 5 + 10}`"
                    :lazy-src="`https://picsum.photos/10/6?image=${i * 5 + 10}`"
                    aspect-ratio="1"
                  ></v-img>
                </v-col>
              </v-row>
              <v-divider></v-divider>
              <v-row class="d-flex justify-content-center">
                <v-btn class="mr-1" text outlined color="success" @click="e1 = 2">이전 단계</v-btn>
                <v-btn text outlined color="success" @click="e1 = 4">다음 단계</v-btn>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>
        <v-stepper-content step="4">
          <v-card class="mb-12" color height="100%" min-width="900px" min-height="700px">
            <v-container fluid>
              <h3 class="text-center">읽었던 책 중 감명깊었던 책을 선택해주세요.</h3>
              <v-row>
                <v-col v-for="i in 6" :key="i" cols="12" md="4">
                  <v-img
                    :src="`https://picsum.photos/500/300?image=${i * 5 + 10}`"
                    :lazy-src="`https://picsum.photos/10/6?image=${i * 5 + 10}`"
                    aspect-ratio="1"
                  ></v-img>
                </v-col>
              </v-row>
              <v-divider></v-divider>
              <v-row class="d-flex justify-content-center">
                <v-btn class="mr-1" text outlined color="success" @click="e1 = 3">이전 단계</v-btn>
                <v-btn class="ml-1" text outlined color="success" @click="submit">가입</v-btn>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";
import swal from "sweetalert";
export default {
  name: "Signup",
  computed: {
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
    email() {
      if (this.email.length > 15) {
        this.email = this.email.substring(0, 15);
      }
      if (this.email != this.checkedEmail) {
        this.isCheckedEmail = false;
      }
    },
  },

  created() {
    this.isLogin = false;
    if (VueCookies.get("jwt_token")) {
      console.log(VueCookies.get("jwt_token"));
      this.e1 = 2;
      this.isSocial = true;
    } else {
      this.e1 = 1;
    }
  },

  methods: {
    checkEmail() {
      // axios 요청
      console.log(this.email + "@bookridge.com");
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/check_email/`, {
          params: {
            email: this.email + "@bookridge.com",
          },
        })
        // true면 존재X
        .then((res) => {
          if (res.data.result) {
            this.isCheckedEmail = true;
            this.checkedEmail = this.email;
            swal("사용 가능한 이메일입니다.");
          } else {
            swal("이미 존재하는 이메일입니다.");
          }
          console.log(res.data.object);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    test() {
      console.log(document.getElementById("sample5_address").value);
      if (document.getElementById("sample5_address") === null) {
        this.addressRules = [false];
      } else {
        this.addressRules = [true];
      }
    },
    save(date) {
      this.$refs.menu.save(date);
    },
    submit() {
      // 소셜로그인 시 프로필 수정 요청으로 보내기
      if (VueCookies.get("social_id")) {
        axios
          .post(
            `${
              process.env.VUE_APP_SERVER_URL
            }/accounts/profile/${VueCookies.get("user_pk")}/`,
            {
              email: this.$route.params.email,
              birth: this.birth,
              name: this.$route.params.name,
              address: document.getElementById("sample5_address").value,
              latitude: parseFloat(document.getElementById("x").value),
              longitude: parseFloat(document.getElementById("y").value),
              gender: this.gender == "남자" ? 0 : 1,
              social: this.$route.params.social,
              social_id: VueCookies.get("social_id"),
            },
            {
              headers: {
                Authorization: VueCookies.get("jwt_token"),
              },
            }
          )
          .then((res) => {
            swal(`${res.data.name}님 북릿지에 오신걸 환영합니다. `);
            this.$router.push("/main");
            this.$router.go();
          })
          .catch((err) => {
            console.log(err);
          });
        // 일반회원가입 시 요청
      } else {
        axios
          .post(`${process.env.VUE_APP_SERVER_URL}/accounts/signup/`, {
            name: this.name,
            email: this.email + "@bookridge.com",
            password1: this.password1,
            password2: this.password2,
            birth: this.birth,
            gender: this.gender == "남자" ? 0 : 1,
            address: document.getElementById("sample5_address").value,
            latitude: document.getElementById("x").value,
            longitude: document.getElementById("y").value,
          })
          .then((res) => {
            console.log(res);
            swal("회원가입을 정상적으로 마쳤습니다. 로그인해주세요!");
            this.$router.push("/");
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    validate() {
      this.$refs.form1.validate();
    },
    validate2() {
      this.$refs.form2.validate();
    },
  },
  data() {
    return {
      // 백에 보내줘야 하는 데이터 : 데이터타입
      // signUpData: {
      //   name: "string",
      //   email: "string",
      //   password1: "string",
      //   password2: "string",
      //   birth: "string",
      //   gender: "int",
      //   address: "string",
      //   latitude: "float", // 위도
      //   longitude: "float", // 경도
      // },
      isCheckedEmail: true,
      checkedEmail: "정말말도안되는이메일",
      menu: false,
      isSocial: false,
      isLogin: false,
      e1: 1,

      modal: false,
      hide: false,
      locationX: "",
      locationY: "",

      dialogPolicy: false,

      checkbox: false,
      lazy1: false,
      lazy2: false,

      valid1: false,
      valid2: false,
      valid3: true,
      show1: false,
      show2: false,

      email: "",
      emailRules: [
        (v) => !!v || "아이디는 필수값입니다.",
        (v) => (v && v.length <= 15) || "15자 이내로 입력해주세요.",
      ],

      name: "",
      nameRules: [
        (v) => !!v || "이름은 필수값입니다.",
        (v) => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요.",
      ],
      password1: "",
      password1Rules: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],
      password2: "",
      password2Rules: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => this.password1 == v || "잘못된 비밀번호입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],

      gender: null,
      genders: ["남자", "여자"],
      genderRules: [(v) => !!v || "성별은 필수값입니다."],

      birth: null,
      birthdayRules: [(v) => !!v || "생년월일은 필수값입니다."],

      address: "'주소검색' 버튼을 눌러 주소를 검색해주세요.",
      addressRules: [false],

      agreeRules: [(v) => !!v || "약관동의는 필수입니다."],
    };
  },
};
</script>
<style>
.card-img {
  width: 250px;
  height: 250px;
}
.address-btn {
  font-size: 15px;
  border-radius: 5px;
  box-shadow: 0.5px 0.5px 0.5px 0.5px #bdbdbd;
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 6px 14px;

  margin: 4px 2px;
  cursor: pointer;
}
.address-btn:hover {
  opacity: 0.9;
}
.nohover {
  cursor: default;
}
.text-green {
  color: green;
}
.text-red {
  color: red;
}
</style>