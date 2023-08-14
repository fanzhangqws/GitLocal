<template>
    <view>
        <view>
            <view>
                <cmd-cel-item v-for="item in data" :title="item.label" :addon="item.value"></cmd-cel-item>
            </view>
            
            <view v-if="user_info.role.startsWith('客户经理') && segment_id==2">
                <view class="uni-title uni-center">订单状态</view>
                <view class="uni-timeline" style="padding: 30upx 20upx;background-color: #fff;">
                
                    <view class="uni-timeline-item" v-for="(item, index) in log_data">
                
                        <view class="uni-timeline-item uni-timeline-first-item" v-if="index==0">
                            <view class="uni-timeline-item-divider"></view>
                            <view class="uni-timeline-item-content">
                                <view>{{log_data[0].workarea}} {{log_data[0].status}}</view>                                                                    
                                <view class="datetime">
                                    {{log_data[0].status_date}}
                                </view>
                                <my-issue :infoReceive='evaluate_list[0].star_value'/>
                            </view>
                        </view>
                
                        <view class="uni-timeline-item-divider" v-if="index!=0 && index!=log_data.length-1"></view>
                        <view class="uni-timeline-item-content" v-if="index!=0 && index!=log_data.length-1">
                            <view>
                                {{item.workarea}} {{item.status}}
                            </view>
                            <view class="datetime">
                                {{item.status_date}}
                            </view>
                            <my-issue :infoReceive='evaluate_list[index].star_value'/>
                        </view>
                
                        <view class="uni-timeline-item uni-timeline-last-item" v-if="index==log_data.length-1">
                            <view class="uni-timeline-item-divider"></view>
                            <view class="uni-timeline-item-content">
                                <view>
                                    {{log_data[log_data.length-1].workarea}} {{log_data[log_data.length-1].status}}
                                </view>
                                <view class="datetime">
                                    {{log_data[log_data.length-1].status_date}}
                                </view>
                                <my-issue :infoReceive='evaluate_list[log_data.length-1].star_value'/>
                            </view>
                        </view>
                    </view>
                </view>                
            </view>
            <view v-else>
                <view class="uni-title uni-center">订单状态</view>
                <view class="uni-timeline" style="padding: 30upx 20upx;background-color: #fff;">
                
                    <view class="uni-timeline-item" v-for="(item, index) in log_data">
                
                        <view class="uni-timeline-item uni-timeline-first-item" v-if="index==0">
                            <view class="uni-timeline-item-divider"></view>
                            <view class="uni-timeline-item-content">
                                <view>{{log_data[0].workarea}} {{log_data[0].status}}</view>                                                                    
                                <view class="datetime">
                                    {{log_data[0].status_date}}
                                </view>
                            </view>
                        </view>
                
                        <view class="uni-timeline-item-divider" v-if="index!=0 && index!=log_data.length-1"></view>
                        <view class="uni-timeline-item-content" v-if="index!=0 && index!=log_data.length-1">
                            <view>
                                {{item.workarea}} {{item.status}}
                            </view>
                            <view class="datetime">
                                {{item.status_date}}
                            </view>
                        </view>
                
                        <view class="uni-timeline-item uni-timeline-last-item" v-if="index==log_data.length-1">
                            <view class="uni-timeline-item-divider"></view>
                            <view class="uni-timeline-item-content">
                                <view>
                                    {{log_data[log_data.length-1].workarea}} {{log_data[log_data.length-1].status}}
                                </view>
                                <view class="datetime">
                                    {{log_data[log_data.length-1].status_date}}
                                </view>
                            </view>
                        </view>
                    </view>
                </view>  
            </view>
            <!-- 居中 -->
            <uni-popup :show="showPopupMiddle" :type="popType" v-on:hidePopup="hidePopup">
                <view class="uni-common-mt uni-helllo-text uni-center">
                    撤单原因
                </view>
                <view class="uni-form-item uni-column">
                    <input class="uni-input" @blur="bindTextBlur" bindTextAreaBlur confirm-type="done" placeholder="请输入撤单原因" />
                </view>
                <button class="btn-logout" @tap="cancel_order(cancel_msg)">确定</button>
            </uni-popup>
            <view>
                <button v-if="user_info.role.startsWith('客户经理') && segment_id==1" class="btn-logout" @tap="process_order">转派</button>
                <button v-if="!user_info.role.startsWith('客户经理') && segment_id==1" class="btn-logout" @tap="process_order">回单</button>
                <button v-if="user_info.role.startsWith('客户经理') && segment_id!=2" class="btn-logout" @tap="showMiddlePopup">撤单</button>
                <button v-if="user_info.role.startsWith('客户经理') && segment_id==2" class="btn-logout" @tap="evaluate">评价打分</button>
            </view>
        </view>

    </view>
</template>

<script>
    import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
    import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
    import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"
    import cmdCelItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
    import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"
    import uniPopup from '@/components/uni-popup.vue'
    import myIssue from '@/components/myIssue2.vue'

    export default {
        components: {
            cmdNavBar,
            cmdPageBody,
            cmdTransition,
            cmdCelItem,
            cmdAvatar,
            myIssue,
            uniPopup
        },
        data() {
            return {
                data: [],
                id: '',
                segment_id: '',
                log_data: [],
                user_info: [],
                popType: 'middle',
                showPopupMiddle: false,
                cancel_msg: '',
                star_value: {"score":0},
                return_id: '',
                evaluate_list:[]
            };
        },
        mounted() {},
        onLoad: function(option) {
            this.id = option.id;
            this.segment_id = option.segment_id;

        },
        onShow() {
            this.$api.request({
                url: '/order/detail?id=' + this.id,
                method: 'GET'
            }).then((data) => {
                // console.log(data)
                this.data = data.info
                this.return_id = data.id
                this.log_data = data.logs.sort(this.sortFunc)
                for(var item of this.log_data) {
                    var item_dict = {"id": item.id, "star_value":{"score":0}}
                    this.evaluate_list.push(item_dict)
                }
            });

            this.user_info = uni.getStorageSync('user_info');
        },
        methods: {
            evaluate:function(){
                console.log(this.evaluate_list)
                var data=[];
                for(var item of this.evaluate_list){
                    var temp={"id": item.id, "score":item.star_value.score};
                    data.push(temp)
                };
                this.$api.request({
                    url: '/order/score',
                    method: 'POST',
                    data:data
                }).then(()=>{
                    uni.reLaunch({
                    	url: "/pages/list_order/list_order"
                    })
                });
            },
            bindTextBlur: function(e) {
                this.cancel_msg = e.detail.value
            },
            sortFunc(x, y) {
                if (x.status_date > y.status_date) {
                    return 1
                } else if (x.status_date < y.status_date) {
                    return -1
                } else {
                    return 0
                }
            },
            //统一的关闭popup方法
            hidePopup: function() {
                this.showPopupMiddle = false;
                this.cancel_msg = ''
            },
            //展示居中 popup
            showMiddlePopup: function() {
                this.hidePopup();
                this.popType = 'middle';
                this.showPopupMiddle = true;
            },

            cancel_order(cancel_msg) {
                var data = {
                    "id": this.id,
                    "reason": cancel_msg
                };
                this.$api.request({
                    url: '/order/cancel',
                    method: 'POST',
                    data: data
                }).then(() => {
                    this.hidePopup();
                    uni.reLaunch({
                        url: "/pages/list_order/list_order"
                    })
                });
            },

            process_order() {
                uni.navigateTo({
                    url: "/pages/order_process/order_process?id=" + this.id + "&return_id=" + this.return_id
                })
            }
        }
    }
</script>

<style lang="scss">
    $backgroundC:#f9f9f9;
    $borderColor:#f5f5f5;
    $white:#ffffff;
    $fontSize:28upx;
    
    .btn-logout {
        margin-top: 100upx;
        width: 50%;
        border-radius: 50upx;
        font-size: 16px;
        color: #fff;
        background: linear-gradient(to right, #365fff, #36bbff);

        &-hover {
            background: linear-gradient(to right, #365fdd, #36bbfa);
        }
    },
    .uni-timeline-item-content {
        flex-direction: column;
    },
    

	.issue {
		background-color: $backgroundC;
		
		&-head{
			background-color: $white;
			height: 55upx;
            border-top: 0;
            border-bottom: 0;
            padding: 0;

			
			&-pic{
				width: 70upx;
				height: 70upx;
				border-radius: 50%;
				vertical-align: middle;
				margin-right: 17upx;
			}
			&-title{
				line-height: 100upx;
				font-size: 30upx;
				vertical-align: middle;
				margin-right: 35upx;
			}
			
			&-star-box{
				
				image{
					width: 32upx;
					height: 32upx;
					vertical-align: middle;
					margin-right: 14upx;
				}
				image.active{
					animation: star_move ease-in 1 1s,star_rotate ease 1.5s infinite 1s;
				}
			}
		}
		textarea{
			width: 100%;
			height: 420upx;
			background-color: $white;
			font-size: $fontSize;
			color: #898989;
			padding: 24upx;
			line-height: 40upx
		}
		&-btn-box{
			padding: 54upx 30upx;
			
			button{
				width: 100%;
				height: 80upx;
				border-radius: 80upx;
				font-size: $fontSize;
				background-color: #3682FF;
				line-height: 80upx
			}
		}
	},
    .issue-head {
        border-top: 0;
        border-bottom: 0;
        padding: 0;
    }
    
</style>
