<template>
  <view class="cmd-avatar" :class="setShapeSizeClass" :style="setIconTextStyle+setNumSizeStyle" :id="elId" @tap="$_click">
    <image v-if="src != ''" class="cmd-avatar__img" mode="aspectFit" :src="src" @load="$_imageLoad" @error="$_imageError"></image>
    <cmd-icon v-else-if="icon != ''" :type="icon" :size="iconSize" :color="make.color"></cmd-icon>
    <text v-else-if="text != ''" v-text="text"></text>
  </view>
</template>

<script>
  import cmdIcon from '../cmd-icon/cmd-icon.vue'

  export default {
    name: 'cmd-avatar',

    components: {
      cmdIcon
    },

    props: {
      /**
       * 大小 sm md lg Number
       */
      size: {
        validator: val => {
          return typeof val === 'number' || ['sm', 'lg', 'md'].includes(val);
        },
        default: 'md'
      },
      /**
       * 形状 circle圆形 square矩形
       */
      shape: {
        validator: val => ['circle', 'square'].includes(val),
        default: 'circle'
      },
      /**
       * 样式属性style
       */
      make: {
        type: Object,
        default: () => {
          return {
            'color': ''
          };
        }
      },
      /**
       * 图片网络地址
       */
      src: {
        type: String,
        default: ''
      },
      /**
       * 图标type名称
       */
      icon: {
        type: String,
        default: ''
      },
      /**
       * 文本名字建议取首位text[0],长度小于3位
       */
      text: {
        type: [String,Number],
        default: ''
      }
    },

    data() {
      const elId = `Cmd_${Math.ceil(Math.random() * 10e5).toString(36)}`
      return {
        elId: elId,
        iconSize: 40
      }
    },

    computed: {
      // 形状大小
      setShapeSizeClass() {
        let classList = []
        if (['circle', 'square'].includes(this.shape)) {
          classList.push(`cmd-avatar--${this.shape}`)
        }
        if (['sm', 'lg', 'md'].includes(this.size)) {
          classList.push(`cmd-avatar--${this.size}`)
        }
        return classList
      },
      // 自定义大小
      setNumSizeStyle() {
        return typeof this.size === 'number' ?
          `width:${this.size}px;` +
          `height:${this.size}px;` +
          `font-size:${(this.size / 2)}px;` +
          `line-height:${this.size}px;` :
          '';
      },
      // 图标文本样式
      setIconTextStyle() {
        let styleString = '';
        for (let it in this.make) {
          styleString += `${it}:${this.make[it]};`;
        }
        return styleString;
      }
    },

    // #ifdef H5
    mounted() { //分平台吧，在h5的时候走mounted，app和小程序走onReady
      // 当前对象el
      let view = uni.createSelectorQuery().select(`#${this.elId}`);
      view.fields({
        size: true
      }, data => {
        this.iconSize = data.width / 2;
      }).exec();
    },
    // #endif
    // #ifndef H5
    onReady() {
      // 当前对象el
      let view = uni.createSelectorQuery().select(`#${this.elId}`);
      view.fields({
        size: true
      }, data => {
        this.iconSize = data.width / 2;
      }).exec();
    },
    // #endif

    methods: {
      // 当图片载入完毕时
      $_imageLoad(e) {
        this.$emit('load', e);
      },
      // 当错误发生时
      $_imageError(e) {
        this.$emit('error', e);
      },
      // 点击事件
      $_click(e) {
        this.$emit('click',e)
      }
    }
  }
</script>

<style lang="scss">
  /**
   * 头像样式属性变量
   */
  $cmd-avatar-color: #FFF;
  $cmd-avatar-bg-color: #E5E5E5;
  $cmd-avatar-size-sm: 64upx;
  $cmd-avatar-size-md: 80upx;
  $cmd-avatar-size-lg: 128upx;
  $cmd-avatar-spape-radius: 6upx;

  .cmd-avatar {
    color: $cmd-avatar-color;
    text-align: center;
    border-radius: $cmd-avatar-spape-radius;
    background: $cmd-avatar-bg-color;
    box-shadow: 0 0 50px 0 rgba(0, 0, 0, 0.05);
    overflow: hidden;
    // 私有属性
    &__img {
      width: 100%;
      height: 100%;
    }
    // 公共属性
    &--lg {
      width: $cmd-avatar-size-lg;
      height: $cmd-avatar-size-lg;
      font-size: $cmd-avatar-size-lg / 2;
      line-height: $cmd-avatar-size-lg;
    }

    &--sm {
      width: $cmd-avatar-size-sm;
      height: $cmd-avatar-size-sm;
      font-size: $cmd-avatar-size-sm / 2;
      line-height: $cmd-avatar-size-sm;
    }

    &--md {
      width: $cmd-avatar-size-md;
      height: $cmd-avatar-size-md;
      font-size: $cmd-avatar-size-md / 2;
      line-height: $cmd-avatar-size-md;
    }

    &--square {
      border-radius: $cmd-avatar-spape-radius;
      background-clip: border-box;
      overflow: hidden;
    }

    &--circle {
      border-radius: 50%;
      background-clip: border-box;
      overflow: hidden;
    }
  }
</style>
