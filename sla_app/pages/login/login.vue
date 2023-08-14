<template>
    <view class="page_login">
        <!-- 头部logo -->
        <view class="head">
            <view class="head_bg">
                <view class="head_inner_bg">
                    <image style="width: 55px;height: 65px;" :src="imgInfo.head" class="head_logo" />
                </view>
            </view>
        </view>
        <!-- 登录form -->
        <view class="login_form">
            <view class="input">
                <view class="img">
                    <image style="width:27px;height: 27px;" :src="imgInfo.icon_user" />
                </view>
                <input type="text" v-model="username" placeholder="请输入用户账号">
                <view class="img">
                    <image @tap="delUser" class="img_del" :src="imgInfo.icon_del" />
                </view>
            </view>
            <view class="line" />
            <view class="input">
                <view class="img">
                    <image style="width:20px;height: 25px;" :src="imgInfo.icon_pwd" />
                </view>
                <input :type="pwdType" :value="userpwd" @input="inputPwd" placeholder="请输入密码">
                <view class="img" @tap="switchPwd">
                    <image class="img_pwd_switch" :src="imgInfo.icon_pwd_switch" />
                </view>
            </view>
            <view class="line" />
            <view class="input">
                <view class="img">
                    <image style="width:20px;height: 25px;" :src="imgInfo.icon_pwd" />
                </view>
                <input class="biaoti" v-model="code" type="text" maxlength="4" placeholder="请输入验证码" />
                <view class="yzm" :class="{ yzms: second>0 }" @tap="getcode">{{yanzhengma}}</view>
            </view>
        </view>
        <!-- 登录提交 -->
        <button class="submit" type="primary" @tap="login">登录</button>
    </view>
</template>
<script>
    export default {
        data() {
            const isUni = typeof(uni) !== 'undefined'
            return {
                username: '',
                userpwd: '',
                pwdType: 'password',
                imgInfo: {
                    head: isUni ? '/static/head.png' : require('./images/head.png'),
                    icon_user: isUni ? '/static/icon_user.png' : require('./images/icon_user.png'),
                    icon_del: isUni ? '/static/icon_del.png' : require('./images/icon_del.png'),
                    icon_pwd: isUni ? '/static/icon_pwd.png' : require('./images/icon_pwd.png'),
                    icon_pwd_switch: isUni ? '/static/icon_pwd_switch.png' : require('./images/icon_pwd_switch.png')
                },
                second:0,
                code:'',
            }
        },
        computed:{
        	yanzhengma(){
        		if(this.second==0){
        			return '获取验证码';
        		}else{
        			if(this.second<10){
        				return '重新获取0'+this.second;
        			}else{
        				return '重新获取'+this.second;
        			}
        		}
        	}
        },
        methods: {
            inputUsername(e) {
                this.username = e.target.value
            },
            inputPwd(e) {
                this.userpwd = e.target.value
            },
            delUser() {
                this.username = ''
            },
            switchPwd() {
                this.pwdType = this.pwdType === 'text' ? 'password' : 'text'
            },
            login() {
                if (this.code!='') {
                    var data = {
                              "account": this.username,
                              "password": this.userpwd,
                              "sms_code": this.code
                            }
                    this.$api.request({
                        url: '/user/login',
                        method: 'POST',
                        data: data
                    }).then((data) => {
                        console.log(data.token)
                        uni.setStorageSync('sec_token', data.token);
                        // get user info
                        this.$api.request({
                            url: '/user/info',
                            method: 'GET',
                            data: data
                        }).then((data)=>{
                            uni.setStorageSync('user_info', data);
                            uni.switchTab({
                            	url: '/pages/list_order/list_order'
                            })
                        })
                    })                	
                } else{
                	uni.showToast({
                	    icon: 'none',
                	    title: '验证码不能为空，请重新输入！'
                	});
                }
            },
            onUnload(){
            	clearInterval(js)
            	this.second = 0;
            },
            getcode(){
            	if(this.second>0){
            		return;
            	}
            	this.second = 60;
                var data = {
                          "account": this.username,
                          "password": this.userpwd
                        }
                this.$api.request({
                    url: '/user/get_sms_code',
                    method: 'POST',
                    data: data
                }).then((data)=> {
                    var js = setInterval(() => {
                    	this.second--;
                    	if(this.second==0){
                    		clearInterval(js)
                    	}
                    },1000);
                })
            },
        }
    }
</script>
<style>
    page {
        height: auto;
        min-height: 100%;
        background-color: #f5f6f8;
    }
</style>
<style lang="scss" scoped>
    $logo-padding: 60px;
    $form-border-color: rgba(214, 214, 214, 1);
    $text-color: #B6B6B6;

    .page_login {
        padding: 10px;
    }

    .head {
        display: flex;
        align-items: center;
        justify-content: center;
        padding-top: $logo-padding;
        padding-bottom: $logo-padding;

        .head_bg {
            border: 1px solid #fbecf1;
            border-radius: 50px;
            width: 100px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;

            .head_inner_bg {
                border-radius: 40px;
                width: 80px;
                height: 80px;
                display: flex;
                background-color: #fc2c5d;
                align-items: flex-end;
                justify-content: center;
                overflow: hidden;
            }
        }
    }

    .login_form {
        display: flex;
        margin: 20px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid $form-border-color;
        border-radius: 10px;

        .line {
            width: 100%;
            height: 1px;
            background-color: $form-border-color;
        }

        .input {
            width: 100%;
            max-height: 45px;
            display: flex;
            padding: 3px;
            flex-direction: row;
            align-items: center;
            justify-content: center;

            .img {
                min-width: 40px;
                min-height: 40px;
                margin: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .img_del {
                width: 21px;
                height: 21px;
            }

            .img_pwd_switch {
                width: 28px;
                height: 12px;
            }

            input {
                outline: none;
                height: 30px;
                width: 100%;

                &:focus {
                    outline: none;
                }
            }
        }
    }

    .submit {
        margin-top: 30px;
        margin-left: 20px;
        margin-right: 20px;
        color: white;
        background-color: rgba(252, 44, 93, 1.0);
        -webkit-tap-highlight-color: rgba(252, 44, 93, 1.0);

        &:active {
            color: #B6B6B6;
            background-color: rgba(252, 44, 93, 0.8);
        }
    }

    .opts {
        margin-top: 5px;
        margin-left: 25px;
        margin-right: 25px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        .text {
            font-size: 13px;
            color: $text-color;
        }
    }

    .quick_login_line {
        margin-top: 40px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;

        .line {
            height: 1px;
            width: 38%;
            background-color: rgba(211, 211, 213, 1);
        }

        .text {
            font-size: 13px;
            color: rgba(200, 200, 200, 1);
            margin: 2px;
        }
    }

    .quick_login_list {
        margin-top: 30px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;

        .item {
            width: 50px;
            height: 50px;
            margin: 20px;
        }
    }
	.yzm {
		color: #fc2c5d;
		font-size: 24upx;
		line-height: 64upx;
		padding-left: 10upx;
		padding-right: 10upx;
		width:auto;
		height:64upx;
		border:1upx solid #fc2c5d;
		border-radius: 50upx;
	}
	.yzms {
		color: #999999 !important;
		border:1upx solid #999999;
	}
    .biaoti{
    	flex: 1;
    	text-align: left;
    	line-height: 100upx;
        outline: none;
        height: 30px;
        width: 100%;
        font-size: 13px;
        &:focus {
            outline: none;
        }
    }
</style>
