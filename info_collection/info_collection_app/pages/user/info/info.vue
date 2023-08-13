<template>
  <view>
    <cmd-page-body type="top">
      <cmd-transition name="fade-up">
        <view>
            <cmd-cel-item title="头像" slot-right arrow>
            <cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif"></cmd-avatar>
            </cmd-cel-item>
            <cmd-cel-item title="姓名" :addon="data.name" arrow></cmd-cel-item>
            <cmd-cel-item title="联系方式" :addon="data.phone" arrow></cmd-cel-item>
            <cmd-cel-item title="所属部门/分公司" :addon="data.user_dept" arrow></cmd-cel-item>
            <cmd-cel-item title="承包体" :addon="data.contractor_group" arrow></cmd-cel-item>

            <view style="display: flex;flex-direction: row">
<!--                <button class="btn-logout" @tap="modify_pwd">修改密码</button> -->
                <button class="btn-logout" @tap="logout">退出登录</button>
            </view>
          
        </view>
      </cmd-transition>
    </cmd-page-body>
  </view>
</template>

<script>
  import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
  import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
  import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"
  import cmdCelItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
  import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"

  export default {
    components: {
      cmdNavBar,
      cmdPageBody,
      cmdTransition,
      cmdCelItem,
      cmdAvatar
    },
    data() {
      return {
        data:'',
        token: ''
      };
    },
    mounted() {},
    onShow() {
    	this.data = uni.getStorageSync('user_info');
      this.token = uni.getStorageSync('sec_token');
      this.data.phone = String(this.data.phone)
    },
    methods: {
      logout(){
        uni.removeStorageSync('sec_token');
        uni.reLaunch({
        	url: '/pages/login/login'
        })        
      },
      modify_pwd(){
        uni.reLaunch({
            url: '/pages/user/modify/modify'
        }) 
      }
    }
  }
</script>

<style lang="scss">
  .btn-logout {
    margin-top: 100upx;
    width: 30%;
    border-radius: 50upx;
    font-size: 16px;
    color: #fff;
    background: linear-gradient(to right, #365fff, #36bbff);

    &-hover {
      background: linear-gradient(to right, #365fdd, #36bbfa);
    }
  }
</style>
