<template>
    <view class="content">
        <view class="input-group">
            <view class="input-row">
                <text class="title">旧密码：</text>
                <m-input type="password" focus clearable v-model="old_password" placeholder="请输入旧密码"></m-input>
            </view>
            <view class="input-row">
                <text class="title">新密码：</text>
                <m-input type="password" focus clearable v-model="new_password" placeholder="请输入新密码"></m-input>
            </view>
            <view class="input-row">
                <text class="title">确认新密码：</text>
                <m-input type="password" focus clearable v-model="confirm_password" placeholder="请输入新密码"></m-input>
            </view>
        </view>

        <view class="btn-row">
            <button type="primary" class="primary" @tap="findPassword">提交</button>
        </view>
    </view>
</template>

<script>
    import service from '../../service.js';
    import mInput from '../../components/m-input.vue';

    export default {
        components: {
            mInput
        },
        data() {
            return {
                old_password: '',
                new_password: '',
                confirm_password: '',
            }
        },
        methods: {
            findPassword() {
                /**
                 * 仅做示例
                 */
                if (this.new_password!=this.new_password) {
                    uni.showToast({
                        icon: 'none',
                        title: '两次新密码输入不一致！',
                        duration: 8000
                    });
                } else{
                    uni.showToast({
                        icon: 'none',
                        title: '已修改成功！',
                        duration: 8000
                    });
                    uni.reLaunch({ url: '../login/login' });
                }
                
            }
        }
    }
</script>

<style>

</style>
