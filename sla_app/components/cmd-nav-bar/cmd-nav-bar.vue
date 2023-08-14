<template>
  <view :class="fixed ? 'cmd-nav-bar-fixed' : ''" :style="setBackgroundColor">
    <view class="status-bar"></view>
    <view class="cmd-nav-bar">
      <view class="cmd-nav-bar-left">
        <view v-if="leftTitle" class="cmd-nav-bar-left-title" :style="'color:'+setFontColor">{{leftTitle}}</view>
        <view v-if="back && !leftTitle || iconOne && !leftTitle " @tap="$_iconOneClick" class="cmd-nav-bar-left-icon">
          <cmd-icon :type="back ?'chevron-left' : iconOne" size="24" :color="setFontColor"></cmd-icon>
        </view>
        <text v-if="leftText && !leftTitle" @tap="$_leftTextClick" :style="'color:'+setFontColor">{{leftText}}</text>
      </view>
      <view v-if="!leftTitle" class="cmd-nav-bar-title" :style="'color:'+setFontColor">{{title}}</view>
      <view class="cmd-nav-bar-right">
        <view v-if="iconThree && iconFour && !rightText" @tap="$_iconFourClick" class="cmd-nav-bar-right-icon" style="margin-left: 0;">
          <cmd-icon :type="iconFour" size="24" :color="setFontColor"></cmd-icon>
        </view>
        <view v-if="iconTwo && iconThree" @tap="$_iconThreeClick" class="cmd-nav-bar-right-icon">
          <cmd-icon :type="iconThree" size="24" :color="setFontColor"></cmd-icon>
        </view>
        <view v-if="iconTwo" @tap="$_iconTwoClick" class="cmd-nav-bar-right-icon">
          <cmd-icon :type="iconTwo" size="24" :color="setFontColor"></cmd-icon>
        </view>
        <text v-if="rightText" @tap="$_rightTextClick" class="cmd-nav-bar-right-text" :style="(rightColor != '' ? 'color:'+rightColor : 'color:'+setFontColor)">{{rightText}}</text>
      </view>
    </view>
  </view>
</template>

<script>
  import cmdIcon from "../cmd-icon/cmd-icon.vue"
  export default {
    name: 'cmd-nav-bar',

    components: {
      cmdIcon
    },

    props: {
      /**
       * 固定到页面顶部
       */
      fixed: {
        type: Boolean,
        default: true
      },
      /**
       * 文字图标颜色
       */
      fontColor: {
        type: String,
        default: ''
      },
      /**
       * 导航栏背景颜色
       */
      backgroundColor: {
        type: String,
        default: ''
      },
      /**
       * 导航栏标题
       */
      title: {
        type: String,
        default: ''
      },
      /**
       * 导航栏左侧返回按钮，默认点击返回上层
       */
      back: {
        type: Boolean,
        default: false
      },
      /**
       * 左侧文字可同显返回按钮
       */
      leftText: {
        type: String,
        default: ''
      },
      /**
       * 左侧显示标题，不可显示左侧文字图标
       */
      leftTitle: {
        type: String,
        default: ''
      },
      /**
       * 右侧文字
       */
      rightText: {
        type: String,
        default: ''
      },
      /**
       * 右侧文字颜色
       */
      rightColor: {
        type: String,
        default: ''
      },
      /**
       * 图标一，不可与返回按钮,左侧标题同显
       */
      iconOne: {
        type: String,
        default: ''
      },
      /**
       * 图标二
       */
      iconTwo: {
        type: String,
        default: ''
      },
      /**
       * 图标三，须显有图标二
       */
      iconThree: {
        type: String,
        default: ''
      },
      /**
       * 图标四，不可与右侧文字同显
       */
      iconFour: {
        type: String,
        default: ''
      }
    },

    computed: {
      /**
       * 设置标题图标颜色
       */
      setFontColor() {
        let fontColor = '#000';
        if (this.fontColor != '') {
          fontColor = this.fontColor;
        }
        return fontColor;
      },
      /**
       * 设置背景颜色
       */
      setBackgroundColor() {
        let backgroundColor = '#fff';
        if (this.backgroundColor != '') {
          backgroundColor = `background: ${this.backgroundColor};`;
        }
        return backgroundColor;
      }
    },

    methods: {
      /**
       * 图标一点击事件
       */
      $_iconOneClick() {
        if (this.back) {
          uni.navigateBack()
        } else {
          this.$emit("iconOne");
        }
      },
      /**
       * 图标二点击事件
       */
      $_iconTwoClick() {
        this.$emit("iconTwo");
      },
      /**
       * 图标三点击事件
       */
      $_iconThreeClick() {
        this.$emit("iconThree");
      },
      /**
       * 图标四点击事件
       */
      $_iconFourClick() {
        this.$emit("iconFour");
      },
      /**
       * 左侧文字点击事件
       */
      $_leftTextClick() {
        this.$emit("leftText");
      },
      /**
       * 右侧文字点击事件
       */
      $_rightTextClick() {
        this.$emit("rightText");
      }
    }

  }
</script>

<style lang="scss">
  /* 导航栏样式变量 */
  $cmd-nav-bar-color : #000;
  $cmd-nav-bar-background : #fff;
  $cmd-nav-bar-font-size : 32upx;

  /* 固定到页面顶部 */
  .cmd-nav-bar-fixed {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: $cmd-nav-bar-background;
  }

  /*沉浸状态栏变化*/
  .status-bar {
    box-sizing: border-box;
    display: block;
    width: 100%;
    margin-bottom: -3upx;
    height: var(--status-bar-height);
    line-height: var(--status-bar-height);
    background: transparent;
  }

  /*导航栏默认*/
  .cmd-nav-bar {
    display: flex;
    align-items: center;
    height: 92upx;
    line-height: 92upx;
    color: $cmd-nav-bar-color;
    background: transparent;
    box-shadow: 0 6upx 6upx -3upx rgba(0, 0, 0, .2);

    /*所有都垂直占比*/
    &-left,
    &-title,
    &-right {
      flex: 1;
      height: 100%;
      display: flex;
      align-items: center;
    }

    /*左侧*/
    &-left {
      justify-content: flex-start;
      font-size: $cmd-nav-bar-font-size;
      padding-left: 30upx;

      &-icon {
        margin-right: 10upx;
        display: inherit;
      }

      &-title {
        font-size: 48upx;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

    }

    /*标题部分 */
    &-title {
      justify-content: center;
      font-size: 36upx;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    /*右侧*/
    &-right {
      justify-content: flex-end;
      font-size: $cmd-nav-bar-font-size;
      margin-right: 30upx;

      &-icon {
        margin-left: 20upx;
        display: inherit;
      }

      &-text {
        margin-left: 20upx;
        font-weight: 500;
      }

    }

  }
</style>
