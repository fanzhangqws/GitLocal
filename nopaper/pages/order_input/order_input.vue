<template>
    <view v-if="token" class="content">
        <view class="input-group">
            <view class="input-row border">
                <text class="title">抽号号码：</text>
                <m-input class="m-input" type="text" v-model="output_data.sort" placeholder="请输入抽号号码"></m-input>
            </view>
            <view class="input-row border">
                <text class="title">身份证号：</text>
                <m-input type="idcard" v-model="output_data.cert" placeholder="请输入身份证号" class="m-input" />
            </view>
            <view class="input-row border">
                <text class="title">客户姓名：</text>
                <m-input class="m-input" type="text" v-model="output_data.name" placeholder="请输入客户姓名"></m-input>
            </view>

            <view class="input-row border">
                <text class="title">业务类型：</text>
                <picker @change="bindPickerChange" :value="index" :range="array" placeholder="请选择业务类型">
                    <view class="uni-input">{{ array[index] }}</view>
                </picker>
            </view>

            <view class="input-row border" style="padding-top: 10rpx;">
                <text class="title">业务描述</text>
                <textarea type="text" v-model="output_data.desc" />
                </view>

            <view class="input-row border">
                <text class="title">金额：</text>
                <m-input
                    class="m-input"
                    type="digit"
                    v-model="output_data.fee"
                    placeholder="请输入金额"
                ></m-input>
            </view>
        </view>
        <view class="btn-row border">
            <button type="primary" class="primary" @tap="post_data">提交</button>
        </view>
    </view>
</template>

<script>
import { mapState } from 'vuex';
import mInput from '../../components/m-input.vue';

export default {
    components: {
        mInput
    },
    data() {
        return {
            output_data: { sort: '', cert: '', name: '', desc: '', fee: '', service: '' },
            title: 'picker',
            array: ['请选择业务类型','套餐新装', '套餐互转', '套餐改明细', '套餐注销', '套餐停机', '套餐复机', '新套餐新装', '换卡', '补卡', '产品停复机', '叠加包办理', '附属功能办理', '移机', '成品卡返档'],
            index: 0,
            token: ''
        };
    },
    computed: mapState(['forcedLogin', 'hasLogin', 'userName']),
    methods: {
        bindPickerChange: function(e) {
            console.log('picker发送选择改变，携带值为', e.target.value);
            this.index = e.target.value;
            if (e.target.value!=0){
                this.output_data.service = this.array[e.target.value];
            }else{
                uni.showToast({
                    icon: 'none',
                    title: '请选择业务类型!',
                    duration: 8000
                });  
            }
            
        },
        post_data(self) {
            // Promise
            if (this.output_data['service']!='请选择业务类型' && this.output_data['service']!=''){
                uni.request({
                    url: 'http://x.x.x.x/nopaper/api/order/create',
                    data: this.output_data,
                    method: 'POST',
                    header: { 'content-type': 'application/json', 'token': this.token }
                }).then(data => {
                        //data为一个数组，数组第一项为错误信息，第二项为返回数据
                        console.log('token is ', this.token);
                        var [error, res] = data;
                        console.log(res);
                        console.log(error);
                        if (res.statusCode == 200) {
                            console.log(this.output_data, '/n data successfully posted!');
                            uni.showToast({
                                icon: 'none',
                                title: '预受理单录入成功！',
                                duration: 2000,
                            });
                            setTimeout(function() {uni.reLaunch({
                                             url: '../order_list/order_list' 
                                        });}, 2000);

                        } else {
                            console.log(res.data);
                            uni.showToast({
                                icon: 'none',
                                title: '预受理单录入失败！错误原因： '+ res.data,
                                duration: 8000
                            });                        
                        }
                    }).then(data=>{
                        
                    });
            } else {
                uni.showToast({
                    icon: 'none',
                    title: '预受理单录入失败！请选择业务类型!',
                    duration: 8000
                }); 
            }                
        }

    },
    mounted() {},
    onShow() {
        this.token = uni.getStorageSync('token');
    },
    onHide() {
        this.output_data = { sort: '', cert: '', name: '', desc: '', fee: '0', service: '' };
    }
};
</script>

<style>
.title {
    font-size: 30upx;
}
.m-input-view {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    flex: 1;
    padding: 0 1rpx;
}

.m-input-input {
    flex: 1;
    width: 100%;
}

.m-input-icon {
    width: 20px;
}
.action-row {
    display: flex;
    flex-direction: row;
    justify-content: center;
}

.action-row navigator {
    color: #007aff;
    padding: 0 20upx;
}
</style>
