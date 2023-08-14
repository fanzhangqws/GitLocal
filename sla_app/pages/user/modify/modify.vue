<template>
    <view>
        <view class="modify">
            <view class="modify-password">
                <cmd-input v-model="oldpassword" type="password" displayable maxlength="26" placeholder="请输入旧密码"></cmd-input>
            </view>
            <view class="modify-password">
                <cmd-input v-model="passwordOne" type="password" displayable maxlength="26" placeholder="请输入新密码"></cmd-input>
            </view>
            <view class="modify-password">
                <cmd-input v-model="passwordTwo" type="password" displayable maxlength="26" placeholder="请再次确认新密码"></cmd-input>
            </view>
            <button class="btn-modify" @tap="fnModify">提交</button>
        </view>
    </view>
</template>

<script>
  import cmdInput from "@/components/cmd-input/cmd-input.vue"

  export default {
    components: {
      cmdInput
    },
    data() {
      return {
        oldpassword: '',
        passwordOne: '',
        passwordTwo: ''
      };
    },
    methods: {
        /**
         * 提交按钮点击执行
         */
        fnModify() {
            var data = {
                "old_password": this.oldpassword,
                "new_password": this.passwordOne,
                "confirm_password": this.passwordTwo
            }
            this.$api.request({
                url: '/user/changepassword',
                method: 'POST',
                data: data
            }).then((data) => {
                uni.removeStorageSync('sec_token');
                uni.reLaunch({
                	url: '/pages/login/login'
                }) 
            })
        },    
    },
  }
</script>

<style lang="scss">
  $modify-margin-h: 72upx;
  $modify-margin-v: 118upx;

  .modify {
    margin-top: $modify-margin-v;
    margin-right: $modify-margin-h;
    margin-left: $modify-margin-h;


    &-password,
    &-code {
      margin-bottom: 40upx;
      border-bottom: 2upx #dedede solid;
    }

    .btn-modify {
      margin-top: 100upx;
      border-radius: 50upx;
      font-size: 16px;
      color: #fff;
      background: linear-gradient(to right, #365fff, #36bbff);
    }

    button[disabled] {
      color: #fff;
    }
  }
</style>
