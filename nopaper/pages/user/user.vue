<template>
    <view class="content">
        <view class="btn-row">
            <button v-if="!token" type="primary" class="primary" @tap="bindLogin">登录</button>
            <button v-if="token" type="default" @tap="bindLogout">退出登录</button>
        </view>
    </view>
</template>

<script>
    import {
        mapState,
        mapMutations
    } from 'vuex'

    export default {
        computed: {
            ...mapState(['hasLogin', 'forcedLogin'])
        },
        data() {
            return {
                token: ''
            };
        },
        methods: {
            ...mapMutations(['logout']),
            bindLogin() {
                uni.navigateTo({
                    url: '../login/login',
                });
            },
            bindLogout() {
                this.logout();
                uni.removeStorageSync('token')
                uni.reLaunch({
                    url: '../login/login',
                });

            }
        },
        onShow() {
            this.token = uni.getStorageSync('token')
        }
    }
</script>

<style>

</style>
