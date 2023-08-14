<template>
  <view class="cmd-input">
    <input class="cmd-input-input" :disabled="disabled" :focus="isFocus" :type="type === 'password' ? 'text' : type"
      :password="type==='password' && !showPassword" :value="inputValue" :maxlength="maxlength" :placeholder="placeholder"
      :placeholder-style="setPlaceholderStyle" @input="$_onInput" @focus="$_onFocus" @blur="$_onBlur" @confirm="$_onConfirm" />
    <view v-if="inputValue.length" class="cmd-input-icon">
      <cmd-icon v-if="displayable&&!clearable" type="eye" size="24" :color="showPassword ? '#111a34':'#c5cad5'" @click="$_display"></cmd-icon>
      <cmd-icon v-if="clearable" type="close-circle" size="24" color="#c5cad5" @click="$_clear"></cmd-icon>
    </view>
  </view>
</template>

<script>
  import cmdIcon from '@/components/cmd-icon/cmd-icon.vue'

  export default {
    name: 'cmd-input',

    components: {
      cmdIcon
    },

    props: {
      /**
       * 输入类型 digit idcard number text password
       */
      type: {
        type: String,
        default: 'text'
      },
      /**
       * 占位符
       */
      placeholder: {
        type: String,
        default: ''
      },
      /**
       * 占位符样式
       */
      placeholderStyle: {
        type: Object,
        default: () => {
          return {}
        }
      },
      /**
       * 最大输入长度
       */
      maxlength: {
        type: [String, Number],
        default: '',
      },
      /**
       * 是否为禁用状态
       */
      disabled: {
        type: Boolean,
        default: false
      },
      /**
       * 自动获取焦点
       */
      focus: {
        type: Boolean,
        default: false
      },
      /**
       * 默认初始内容
       */
      value: {
        type: [String, Number],
        default: ''
      },
      /**
       * 是否显示清除按钮
       */
      clearable: {
        type: Boolean,
        default: false
      },
      /**
       * 是否显示密码可见按钮
       */
      displayable: {
        type: Boolean,
        default: false
      }
    },

    data() {
      return {
        /**
         * 显示密码明文
         */
        showPassword: false,
        /**
         * 输入框的值
         */
        inputValue: this.value,
        /**
         * 是否聚焦
         */
        isFocus: this.focus
      }
    },

    /**
     * 监听输入值
     */
    watch: {
      value(v) {
        this.inputValue = v;
      }
    },

    computed: {
      /**
       * 设置占位符样式
       */
      setPlaceholderStyle() {
        let placeholderStyle = '';
        for (let it in this.placeholderStyle) {
          placeholderStyle += `${it}:${this.placeholderStyle[it]}`;
        }
        return placeholderStyle;
      }
    },

    methods: {
      /**
       * 清除输入框
       */
      $_clear() {
        this.inputValue = ''
        this.isFocus = true
      },
      /**
       * 密码可见状态
       */
      $_display() {
        this.showPassword = !this.showPassword
      },
      /**
       * 键入聚焦输入框
       */
      $_onFocus(e) {
        this.$emit('focus', e.target.value)
      },
      /**
       * 键出移除输入框
       */
      $_onBlur(e) {
        this.$emit('blur', e.target.value)
      },
      /**
       * 键入输入监听
       */
      $_onInput(e) {
        this.$emit('input', e.target.value)
      },
      /**
       * 输入框提交监听
       */
      $_onConfirm(e) {
        this.$emit('confirm', e.target.value)
      }
    }
  }
</script>

<style lang="scss">
  /**
	 * 输入框样式属性变量
	 */
  $cmd-input-height: 90upx;
  $cmd-input-font-size: 36upx;
  $cmd-input-line-height: 1.2;

  .cmd-input {
    display: flex;
    flex-direction: row;
    align-items: center;

    &-input {
      flex: 1;
      text-align: left;
      width: 100%;
      height: $cmd-input-height;
      color: #111a34;
      font-size: $cmd-input-font-size;
      font-weight: 500;
      line-height: $cmd-input-line-height;
      font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, 微软雅黑, Arial, sans-serif;
      border: none;
      background: 0 0;
      outline: 0;
      box-sizing: border-box;
      appearance: none;
    }

    &-icon {
      width: 48upx;
      margin-left: 8upx;
      text-align: center;
      font-size: $cmd-input-font-size;
      font-weight: 500;
      line-height: $cmd-input-line-height;
    }

  }
</style>
