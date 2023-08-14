<template>
    <view v-if="user_info.role.startsWith('客户经理')">
        <view>
            <view class="uni-list">
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        业务类型
                    </view>
                    <view class="uni-list-cell-db">
                        <picker @change="bindPickerChange" :value="index" :range="order_type_list">
                            <view class="uni-input">{{order_type_list[index]}}</view>
                        </picker>
                    </view>
                </view>
        
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        客户名称
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur" auto-height="true" placeholder="请输入客户名称" />
                            </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        客户编码
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur1" auto-height="true" placeholder="请输入客户编码"/>
                        </view>
                    </view>                        
                </view>
        
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        甲端联系人
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur2" auto-height="true" placeholder="请输入甲端联系人"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        甲端联系电话
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur3" auto-height="true" placeholder="请输入甲端联系电话"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        甲端地址
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur4" auto-height="true" placeholder="请输入甲端地址"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        乙端联系人
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur5" auto-height="true" placeholder="请输入乙端联系人"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        乙端联系电话
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur6" auto-height="true" placeholder="请输入乙端联系电话"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list-cell">
                    <view class="uni-list-cell-left">
                        乙端地址
                    </view>
                    <view class="uni-list-cell-db">
                        <view class="uni-textarea">
                            <textarea @blur="bindTextAreaBlur7" auto-height="true" placeholder="请输入乙端地址"/>
                        </view>
                    </view>                        
                </view>
                
                <view class="uni-list">
                    <view class="uni-list-cell cell-pd">
                        <view class="uni-uploader">
                            <view class="uni-uploader-head">
                                <view class="uni-uploader-title">附件上传</view>
                                <view class="uni-uploader-info">{{imageList.length}}/9</view>
                            </view>
                            <view class="uni-uploader-body">
                                <view class="uni-uploader__files">
                                    <block v-for="(image,index) in imageList" :key="index">
                                        <view class="uni-uploader__file">
                                            <image class="uni-uploader__img" :src="image" :data-src="image" @tap="previewImage"></image>
                                        </view>
                                    </block>
                                    <view class="uni-uploader__input-box">
                                        <view class="uni-uploader__input" @tap="chooseImage"></view>
                                    </view>
                                </view>
                            </view>                        
                        </view>
                    </view>
                </view>
            </view>
            
            <!-- 居中 -->
            <uni-popup :show="showPopupMiddle" :type="popType" v-on:hidePopup="hidePopup">
                <view class="uni-common-mt uni-helllo-text uni-center">
                    上传进度
                </view>
                <view>
                    <cmd-progress type="circle" :percent="progress_perct" gap-position="left" stroke-shape="square"></cmd-progress>
                </view>
            </uni-popup>
        </view>
        <view>
            <button  class="btn-logout" @tap="confirm">确认</button>
        </view>	
    </view>
    <view v-else class="uni-common-mt uni-helllo-text uni-center">
        对不起，您没有权限执行该操作！
    </view>
</template>

<script>
    import myIssue from '@/components/myIssue.vue'
    import cmdProgress from "@/components/cmd-progress/cmd-progress.vue"
    import uniPopup from '@/components/uni-popup.vue'
    
	var sourceType = [
		['camera'],
		['album'],
		['camera', 'album']
	]
	var sizeType = [
		['compressed'],
		['original'],
		['compressed', 'original']
	]
        
    export default {
        components: {
            myIssue,
            cmdProgress,
            uniPopup,
        },
        data() {
            return {
                imageList: [],
                sourceTypeIndex: 2,
                sourceType: ['拍照', '相册', '拍照或相册'],
                sizeTypeIndex: 2,
                sizeType: ['压缩', '原图', '压缩或原图'],
                countIndex: 8,
                count: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                index: 0,
                order_type_list: ["数字电路", "出租光纤", "以太专线"],
                order_index_list:["4", "5", "11"],
                order_index: "4",
                cust_name: '',
                cust_id:'',
                a_contact:'',
                a_contact_phone:'',
                a_address:'',
                z_contact:'',
                z_contact_phone:'',
                z_address:'',
                attachment:[],
                progress_perct:0,
                popType: 'middle',
                showPopupMiddle: false,
                indicator: 100,
            };
        },
        onUnload() {
        	this.imageList = [],
            this.sourceTypeIndex = 2,
            this.sourceType = ['拍照', '相册', '拍照或相册'],
            this.sizeTypeIndex = 2,
            this.sizeType = ['压缩', '原图', '压缩或原图'],
            this.countIndex = 8;
        },
        mounted() {},
        onShow() {   
            this.user_info = uni.getStorageSync('user_info');
        },
        methods: {
            //统一的关闭popup方法
            hidePopup: function() {
            	this.showPopupMiddle = false;
            },
            //展示居中 popup
            showMiddlePopup: function() {
            	this.hidePopup();
            	this.popType = 'middle';
            	this.showPopupMiddle = true;
            },
            bindTextAreaBlur: function (e) {
                this.cust_name = e.detail.value
            },
            bindTextAreaBlur1: function (e) {
                this.cust_id = e.detail.value
            },
            bindTextAreaBlur2: function (e) {
                this.a_contact = e.detail.value
            },
            bindTextAreaBlur3: function (e) {
                this.a_contact_phone = e.detail.value
            },
            bindTextAreaBlur4: function (e) {
                this.a_address = e.detail.value
            },
            bindTextAreaBlur5: function (e) {
                this.z_contact = e.detail.value
            },
            bindTextAreaBlur6: function (e) {
                this.z_contact_phone = e.detail.value
            },
            bindTextAreaBlur7: function (e) {
                this.z_address = e.detail.value
            },
            bindPickerChange: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value)
                this.index = e.target.value
                this.order_index = this.order_index_list[e.target.value]
            },
            sourceTypeChange: function(e) {
            	this.sourceTypeIndex = e.target.value
            },
            sizeTypeChange: function(e) {
            	this.sizeTypeIndex = e.target.value
            },
            countChange: function(e) {
            	this.countIndex = e.target.value;
            },
            chooseImage: async function() {
                if (this.imageList.length === 9) {
                    let isContinue = await this.isFullImg();
                    console.log("是否继续?", isContinue);
                    if (!isContinue) {
                        return;
                    }
                }
                uni.chooseImage({
                    sourceType: sourceType[this.sourceTypeIndex],
                    sizeType: sizeType[this.sizeTypeIndex],
                    count: this.imageList.length + this.count[this.countIndex] > 9 ? 9 - this.imageList.length : this.count[this.countIndex],
                    success: (res) => {
                        this.imageList = this.imageList.concat(res.tempFilePaths);
                    }
                })
            },
            isFullImg: function() {
                return new Promise((res) => {
                    uni.showModal({
                        content: "已经有9张图片了,是否清空现有图片？",
                        success: (e) => {
                            if (e.confirm) {
                                this.imageList = [];
                                res(true);
                            } else {
                                res(false)
                            }
                        },
                        fail: () => {
                            res(false)
                        }
                    })
                })
            },
            previewImage: function(e) {
                var current = e.target.dataset.src
                uni.previewImage({
                    current: current,
                    urls: this.imageList
                })
            },
            confirm () {
                this.hidePopup();
                this.popType = 'middle';
                this.showPopupMiddle = true;
                const tempFilePaths = this.imageList;
                this.indicator = this.imageList.length;
                console.log("number of images: "+ this.imageList.length)
                var STOREKEY_LOGIN = 'sec_token'
                var _token = {'token': uni.getStorageSync(STOREKEY_LOGIN) || 'undefined'}
                for (let k in tempFilePaths) {
                	uni.uploadFile({
                	    url: 'http://133.69.3.44:8087/attachement/create', 
                        // url: 'http://127.0.0.1:5000/attachement/create',
                	    filePath: tempFilePaths[k],
                	    name: 'file',
                        header: _token,
                	    formData: {
                	        'user': 'test'
                	    },
                	}).then(data=>{
                        var [err, res]=data;
                        if (err==null) {
                        	this.attachment.push(JSON.parse(res.data).data.attachment_id);
                        } else{
                            uni.showToast({
                                title: '上传失败！'+err,
                                duration: 2000
                            });
                        };
                        this.indicator=this.indicator-1;
                        this.progress_perct= (1-this.indicator/this.imageList.length)*100
                        if (this.indicator==0) {
                            var data = {
                              "order_type": this.order_index,
                              "cust_name": this.cust_name,
                              "cust_id": this.cust_id,
                              "a_contact": this.a_contact,
                              "a_contact_phone": this.a_contact_phone,
                              "a_address": this.a_address,
                              "z_contact": this.z_contact,
                              "z_contact_phone": this.z_contact_phone,
                              "z_address": this.z_address,
                              "attachment": this.attachment
                            };
                            this.$api.request({
                                url: '/order/create',
                                method: 'POST',
                                data:data
                            }).then(()=>{
                                this.hidePopup()
                                uni.reLaunch({
                                	url: "/pages/list_order/list_order"
                                })
                            });
                        }
                    });
                }
            }
        }
    }
</script>

<style lang="scss">
    .btn-logout {
        margin-top: 100upx;
        width: 50%;
        border-radius: 50upx;
        font-size: 16px;
        color: #fff;
        background: linear-gradient(to right, #365fff, #36bbff);
        margin-bottom: 100upx;

        &-hover {
            background: linear-gradient(to right, #365fdd, #36bbfa);
        }
        
    }
    
    .uni-list-cell {
    	position: relative;
    	display: flex;
    	flex-direction: row;
    	justify-content: space-between;
    	align-items: center;
    }
    
    .uni-list-cell-left {
    	font-size:28upx;
    	padding: 0 30upx;
        width: 200upx;
    }
    .uni-list-cell-db,
    .uni-list-cell-right {
    	flex: 10;
    }
    .cell-pd {
    	padding: 22upx 30upx;
    }
    
</style>
