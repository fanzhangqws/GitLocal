<template>
  <view>
    <view class="person-head">
      <cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif" @click="fnInfoWin" size="lg" :make="{'background-color': '#fff'}"></cmd-avatar>
      <view class="person-head-box">
        <view class="person-head-nickname">{{data.name}}</view>
        <view class="person-head-username">ID：{{data.saler_code}}</view>
      </view>
    </view>
    <view class="person-list">
      <cmd-cell-item title="我的设备" slot-left arrow>
        <cmd-icon type="bullet-list" size="24" color="#368dff"></cmd-icon>
      </cmd-cell-item>
      <cmd-cell-item title="消息通知" slot-left arrow>
        <cmd-icon type="message" size="24" color="#368dff"></cmd-icon>
      </cmd-cell-item>
      <cmd-cell-item title="系统设置" slot-left arrow>
        <cmd-icon type="settings" size="24" color="#368dff"></cmd-icon>
      </cmd-cell-item>
      <cmd-cell-item title="检查版本" addon="v1.0" slot-left arrow>
        <cmd-icon type="alert-circle" size="24" color="#368dff"></cmd-icon>
      </cmd-cell-item>
    </view>
  </view>
</template>

<script>
  import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"
  import cmdIcon from "@/components/cmd-icon/cmd-icon.vue"
  import cmdCellItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
  
  export default {
    components: {
      cmdAvatar,
      cmdCellItem,
      cmdIcon
    },
    data() {
      return {
        data:'',
        token: ''        
      };
    },
    methods: {
      /**
       * 打开用户信息页
       */
      fnInfoWin() {
        uni.navigateTo({
          url: '/pages/user/info/info'
        })
      }
    },
    onShow() {
    	this.data = uni.getStorageSync('user_info');
      this.token = uni.getStorageSync('sec_token');
      if (this.token) {
      	
      } else{
      	uni.showToast({
      		icon: 'none',
      		title: '您未登录,请登录！'
      	});
        uni.reLaunch({
            url: '/pages/login/login',
        });
      }
    },
  }
</script>

<style lang="scss">
  .person {
    &-head {
      display: flex;
      flex-direction: row;
      align-items: center;
      height: 150px;
      padding-left: 20px;
      background: linear-gradient(to right, #365fff, #36bbff);

      &-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        margin-left: 10px;
      }

      &-nickname {
        font-size: 18px;
        font-weight: 500;
        color: #fff;
      }

      &-username {
        font-size: 14px;
        font-weight: 500;
        color: #fff;
      }
    }

    &-list {
      line-height: 0;
    }
  }
</style>
