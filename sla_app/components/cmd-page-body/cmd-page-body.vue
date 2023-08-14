<template>
  <view :class="setBodyClass" :style="setBackgroundColor+bodyHeight">
    <slot></slot>
  </view>
</template>

<script>
  export default {
    name: 'cmd-page-body',

    props: {
      /**
       * 使用导航栏类型,默认top，top、bottom、top-bottom
       */
      type: {
        type: String,
        default: 'top'
      },
      /**
       * 内容区背景颜色,默认#ffffff
       */
      backgroundColor: {
        type: String,
        default: ''
      }
    },

    data() {
      return {
        bodyHeight: 0
      }
    },

    computed: {
      /**
       * 内容区样式根据导航类型设置
       */
      setBodyClass() {
        let bodyClass = ['cmd-page-body', 'cmd-page-body-top-bottom']
        if (this.type == 'top') {
          bodyClass.splice(1)
          bodyClass.push('cmd-page-body-top');
        }
        if (this.type == 'bottom') {
          bodyClass.splice(1)
          bodyClass.push('cmd-page-body-bottom');
        }
        return bodyClass;
      },
      /**
       * 内容区背景颜色
       */
      setBackgroundColor() {
        let backgroundColor = "background: #ffffff;";
        if (this.backgroundColor) {
          backgroundColor = `background: ${this.backgroundColor};`;
        }
        return backgroundColor;
      }
    },

    mounted() {
      // 初始默认内容高度
      this.bodyHeight = `min-height:${this.$_getBodyHeight()}px`;
    },

    methods: {
      /**
       * 获取默认内容高度
       * 由于由于节点原因，请在vue生命周期mounted中取返回值
       */
      $_getBodyHeight() {
        // 屏幕高度获取
        let windowHeight = uni.getSystemInfoSync().windowHeight;
        // 只用顶部导航
        if (this.type == 'top') {
          let topH = windowHeight - uni.upx2px(88);
          // #ifndef H5
          topH -= uni.getSystemInfoSync().statusBarHeight;
          // #ifdef MP
          topH -= 5;
          // #endif
          // #endif 
          return topH;
        }
        // 只用底部导航
        if (this.type == 'bottom') {
          let bottomH = windowHeight - uni.upx2px(118);
          // #ifndef H5
          bottomH -= uni.getSystemInfoSync().statusBarHeight;
          // #ifdef MP
          bottomH -= 5;
          // #endif
          // #endif 
          return bottomH;
        }
        // 默认上下使用导航栏
        windowHeight -= uni.upx2px(206);
        // #ifndef H5
        windowHeight -= uni.getSystemInfoSync().statusBarHeight;
        // #ifdef MP
        windowHeight -= 5;
        // #endif
        // #endif 
        return windowHeight;
      }
    }

  }
</script>

<style lang="scss">
  /*导航栏内容区*/
  .cmd-page-body {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: #f5f5f5;

    &-top-bottom {
      margin-bottom: 118upx;
      margin-top: 88upx;
      top: var(--status-bar-height);
    }

    &-bottom {
      margin-bottom: 118upx;
      bottom: 0;
    }

    &-top {
      margin-top: 88upx;
      top: var(--status-bar-height);
    }
  }
</style>
