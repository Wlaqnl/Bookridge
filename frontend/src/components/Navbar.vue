<template>
  <mdb-navbar color="rgba-teal-strong" dark>
    <mdb-navbar-brand active to="/main" style="font-family:'HangeulNuri-Bold'; ">BOOKRIDGE</mdb-navbar-brand>
    <mdb-navbar-toggler>
      <mdb-navbar-nav>
        <mdb-nav-item>
          <router-link
            active
            to="/analyze"
            style="color:white;font-family: 'HangeulNuri-Bold';"
          >Analyze</router-link>
        </mdb-nav-item>
        <mdb-nav-item>
          <router-link
            active
            to="/community"
            style="color:white;font-family: 'HangeulNuri-Bold'; "
          >Community</router-link>
        </mdb-nav-item>
        <form>
          <div class="input-group md-form form-sm form-2 pl-0">
            <input
              class="form-control my-0 py-1 cyan-border lucky"
              type="text"
              placeholder="Search"
              aria-label="Search"
              v-model="bookKeyword"
              style="font-family: 'HangeulNuri-Bold'; text-align:center;"
              @keydown.enter="searchWord"
            />
            <mdb-dropdown>
              <mdb-dropdown-toggle
                slot="toggle"
                color="teal"
                style="font-family: 'HangeulNuri-Bold'; text-align:center;"
              >{{ dropDown }}</mdb-dropdown-toggle>
              <mdb-dropdown-menu>
                <mdb-dropdown-item
                  style="font-family: 'HangeulNuri-Bold'; text-align:center;"
                  @click="searchList(0)"
                >제목</mdb-dropdown-item>
                <mdb-dropdown-item
                  style="font-family: 'HangeulNuri-Bold'; text-align:center;"
                  @click="searchList(1)"
                >작가</mdb-dropdown-item>
                <mdb-dropdown-item
                  style="font-family: 'HangeulNuri-Bold'; text-align:center;"
                  @click="searchList(2)"
                >출판사</mdb-dropdown-item>
              </mdb-dropdown-menu>
            </mdb-dropdown>
            <div class="input-group-append" @click="searchWord" @keypress.enter="searchWord">
              <span class="input-group-text teal lighten-3 lighten-3" id="basic-text1">
                <mdbIcon icon="search" />
              </span>
            </div>
          </div>
        </form>
      </mdb-navbar-nav>
      <v-avatar color="indigo" class="user_pic cursor" @click="goToProfile" uk-tooltip="프로필 바로가기">
        <img src="../assets/img/chimmy.jpeg" alt />
      </v-avatar>
      <div
        v-if="isLogin"
        @click="logout"
        class="logout"
        style="font-family: 'HangeulNuri-Bold';"
      >로그아웃</div>
    </mdb-navbar-toggler>
  </mdb-navbar>
</template>

<script>
import swal from "sweetalert";
import VueCookies from "vue-cookies";
// import axios from "axios";
import {
  mdbNavbar,
  mdbNavbarBrand,
  mdbNavbarToggler,
  mdbNavbarNav,
  mdbNavItem,
  mdbIcon,
  mdbDropdown,
  mdbDropdownItem,
  mdbDropdownMenu,
  mdbDropdownToggle,
} from "mdbvue";
export default {
  name: "Navbar",
  components: {
    mdbNavbar,
    mdbNavbarBrand,
    mdbNavbarToggler,
    mdbNavbarNav,
    mdbNavItem,
    mdbIcon,
    mdbDropdown,
    mdbDropdownItem,
    mdbDropdownMenu,
    mdbDropdownToggle,
  },
  props: {
    isLogin: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    loginCheck() {
      return this.isLogin;
    },
  },
  data() {
    return {
      bookKeyword: "",
      searchType: 0,
      dropDown: "제목",
    };
  },
  methods: {
    test() {
      console.log(this.bookKeyword);
    },
    goToProfile() {
      this.$router.push({
        name: "Profile",
        params: {
          pk: VueCookies.get("user_pk"),
        },
      });
    },
    logout() {
      VueCookies.keys().forEach((cookie) => VueCookies.remove(cookie));
      this.closeLoginModal();
      swal("정상적으로 로그아웃이 되었습니다!", {
        buttons: false,
        timer: 5000,
      });
      this.$router.push({ name: "Home" });
      this.$router.go();
    },
    closeLoginModal() {
      this.userId = "";
      this.password = "";
      this.$emit("closeLoginModal");
    },
    searchWord(e) {
      e.preventDefault();
      if (this.bookKeyword == "") {
        swal("검색어를 최소 한 자 이상 입력해주세요.");
      } else {
        if (
          this.$router.currentRoute.fullPath !=
          `/search/${this.bookKeyword}/${this.searchType}`
        ) {
          console.log(this.$router.currentRoute.fullPath);
          this.$router.push(`/search/${this.bookKeyword}/${this.searchType}`);
        }
      }
    },
    searchList(id) {
      if (id == 0) {
        this.dropDown = "제목";
        this.searchType = id;
        console.log(this.searchType);
      } else if (id == 1) {
        this.dropDown = "작가";
        this.searchType = id;
      } else {
        this.dropDown = "출판사";
        this.searchType = id;
      }
    },
  },
};
</script>

<style scoped>
.logout {
  color: white;
}
.logout:hover {
  cursor: pointer;
}
.input-group.md-form.form-sm.form-2 input.amber-border {
  border: 1px solid cyan;
}
.input-group.md-form.form-sm.form-2.pl-0 {
  margin: 0;
}
.user_pic {
  margin-right: 15px;
}
.cursor:hover {
  cursor: pointer;
}
@font-face {
  font-family: "MaplestoryOTFBold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFBold.woff")
    format("woff");
  font-weight: 100;
  font-style: normal;
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
