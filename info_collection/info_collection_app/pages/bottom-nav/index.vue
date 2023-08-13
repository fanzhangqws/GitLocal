<template>
  <view>
    <!-- 顶部导航栏组件 -->
    <cmd-nav-bar :title="title"></cmd-nav-bar>
    <!-- 内容区 start -->
    <cmd-page-body type="top-bottom">
      <!-- #ifdef H5 -->
      <cmd-transition name="fade-up">
        <home v-if="current == 0"></home>
        <person v-if="current == 1"></person>
      </cmd-transition>
      <!-- #endif -->
      <!-- #ifndef H5 -->
      <cmd-transition v-if="current == 0" name="fade-up">
        <home></home>
      </cmd-transition>
      <cmd-transition v-if="current == 1" name="fade-up">
        <person></person>
      </cmd-transition>
      <!-- #endif -->
    </cmd-page-body>
    <!-- 内容区 end -->
    <!-- 底部导航栏组件 -->
    <cmd-bottom-nav background-color="#ffffff" font-color="#3665ff" active-font-color="#3669ff" @click="getBottomNavCurrent"
      :current="current" :list="list"></cmd-bottom-nav>
  </view>
</template>

<script>
  import home from "./home/home.vue"
  import person from "./person/person.vue"
  import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
  import cmdBottomNav from "@/components/cmd-bottom-nav/cmd-bottom-nav.vue"
  import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
  import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"

  export default {
    components: {
      home,
      person,
      cmdBottomNav,
      cmdNavBar,
      cmdPageBody,
      cmdTransition
    },

    data() {
      return {
        bodyHeight: 0,
        title: '首页',
        current: 0,
        list: [{
            "pagePath": "/pages/bottom-nav/home/home",
            "text": "工单查询",
            "icon": "home"
          },
          {
            "pagePath": "/pages/bottom-nav/person/person",
            "text": "个人",
            "icon": "user"
          }
        ]
      };
    },

    methods: {
      /**
       * 获取导航栏选项
       */
      getBottomNavCurrent(e) {
        this.current = e.select;
        this.title = e.list.text;
      }
    }
  }
</script>

<style lang="scss">
</style>
