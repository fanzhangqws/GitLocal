<template>
	<view class="uni-padding-wrap uni-common-mt">
		<view class="content">
                <view class="input-group">
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">楼宇名称：{{item_list[0]}}</text>
                        </view>
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">网格编号：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[1]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">楼宇栋数：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[2]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">楼层数：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[3]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">交付年限：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[4]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">FTTH接入：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange" :value="index" :range="array">
                        	    <view class="uni-input">{{ array[index] }}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">商户数：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[6]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">平均租金（元/平方米）：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[7]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">线路接入方式：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange1" :value="index1" :range="array1">
                        	    <view class="uni-input">{{ array1[index1] }}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">线路产权：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange2" :value="index2" :range="array2">
                        	    <view class="uni-input">{{array2[index2]}}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">井道的线槽归属：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange3" :value="index3" :range="array3">
                        	    <view class="uni-input">{{array3[index3]}}</view>
                        	</picker>
                        </view>                        
                    </view> 
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">物管公司：{{item_list[11]}}</text>
                        </view>
<!--                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[11]"></m-input>
                        </view> -->                      
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">员工数：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[12]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">物管决策联系人：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[13]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">物管决策联系人联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[14]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">招商/中介/客服负责人：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[15]"></m-input>
                        </view>                       
                    </view>                    
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">招商/中介/客服联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[16]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">工程部负责人：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[17]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">工程部负责人联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[18]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">财务部负责人：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[19]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">财务部负责人联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[20]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">所在分公司：{{item_list[21]}}</text>
                        </view>
<!--                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[21]"></m-input>
                        </view> -->                      
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">所在承包体/中心：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[22]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">营销服务经理：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[23]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">营销服务联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[24]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">装维人员：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[25]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">装维人员联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[26]"></m-input>
                        </view>                       
                    </view>
                </view>
               <view>
                    <button class="btn-logout" type="primary" @tap="post_data">提交修改</button>
                </view>
		</view>
	</view>
</template>

<script>
    import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
    import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
    import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"
    import cmdCelItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
    import MescrollUni from '@/components/wenju-mescroll/mescroll-uni.vue'
    import uniIcon from '@/components/uni-icon.vue'
    import mInput from '../../components/m-input.vue';
      
	export default {
        components: {
          cmdNavBar,
          cmdPageBody,
          cmdTransition,
          cmdCelItem,
          uniIcon,
          mInput
        },
        onLoad: function(option) {
            this.building_id = option.building_id;            
        },
		data() {
			return {
				activeColor: '#007aff',
                item_list:[],
                building_id:0,
                array: ['','是','否'],
                array1:['','电信独家','电信+移动','电信+联通','移动独进','联通独进','移动+联通'],
                array2:['','开发商投资','电信投资','移动投资','联通独资','第三方'],
                array3:['','开发商','电信','电信+移动','电信+联通','移动','联通'],
                index: 0,
                index1:0,
                index2:0,
                index3:0,
			}
		},
		methods: {
            post_data(self) {
                var verify_input = true
                if (this.item_list[1]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：网格编号不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[22]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：所在承包体/中心不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[23]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：营销服务经理不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[24]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：营销服务联系方式不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[25]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：装维人员不能为空！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[26]=='' | (isNaN(this.item_list[26])| this.item_list[26].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '装维人员联系方式更新失败！错误原因：装维人员联系方式不能为空且必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if (this.item_list[2]=='' | !(this.item_list[2]>=1 && this.item_list[2]<=50)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '楼宇栋数更新失败！错误原因：楼宇栋数不能为空且必须在1至50之间！',
                        duration: 4000
                    });
                }
                else if (this.item_list[3]!='' && !(this.item_list[3]>=1 && this.item_list[3]<=50)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '楼层数更新失败！错误原因：楼层数必须在1至50之间！',
                        duration: 4000
                    });
                }
                else if (this.item_list[4]!='' && !(this.item_list[4]>=1 && this.item_list[4]<=50)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '交付年限更新失败！错误原因：交付年限必须在1至50之间！',
                        duration: 4000
                    });
                }
                else if (this.item_list[12]!='' && !(this.item_list[12]>=1 && this.item_list[12]<=200)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '员工数更新失败！错误原因：员工数必须在1至200之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[14]!='' && (isNaN(this.item_list[14])| this.item_list[14].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '物管决策联系人联系方式更新失败！错误原因：物管决策联系人联系方式必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[16]!='' && (isNaN(this.item_list[16])| this.item_list[16].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '招商部/中介/客服部负责人联系方式更新失败！错误原因：招商部/中介/客服部负责人联系方式必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[18]!='' && (isNaN(this.item_list[18])| this.item_list[18].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '工程部负责人联系方式更新失败！错误原因：工程部负责人联系方式必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[20]!='' && (isNaN(this.item_list[20])| this.item_list[20].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '财务部负责人联系方式更新失败！错误原因：财务部负责人联系方式必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else {
                    console.log(this.item_list)
                    var post_data = {
                        "item_list": this.item_list,
                        'building_id':this.building_id
                    }
                    this.$api.request({
                        url: '/infocollect/updatebuildingdetail',
                        data: post_data,
                        method: 'POST',
                        // header: { 'content-type': 'application/json', 'token': this.token }
                    }).then(data => {
                        //data为一个数组，数组第一项为错误信息，第二项为返回数据
                        uni.showToast({
                            icon: 'success',
                            title: '物业信息详情更新成功!',
                            duration: 2000,
                        });
                        setTimeout(function() {
                            uni.navigateBack({
                                delta: 1,
                            });}, 2000);
                    });
                }               
            },
            bindPickerChange: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index = e.target.value;
                this.item_list[5] = this.array[e.target.value];                
            },
            bindPickerChange1: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index1 = e.target.value;
                this.item_list[8] = this.array1[e.target.value];                
            },
            bindPickerChange2: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index2 = e.target.value;
                this.item_list[9] = this.array2[e.target.value];                
            },
            bindPickerChange3: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index3 = e.target.value;
                this.item_list[10] = this.array3[e.target.value];                
            },
		},
        onShow() {
            var data = {
                "id": this.building_id
            }
            this.$api.request({
                url: '/infocollect/buildingdetail',
                method: 'POST',
                data:data
            }).then((data)=>{
                this.item_list = data.item_list
                var int_index = [2,3,4,6,7,12]
                for (let x in int_index) {
                	this.item_list[int_index[x]] = String(this.item_list[int_index[x]])
                }
                this.index = this.array.findIndex((value)=>value==this.item_list[5])
                this.index1 = this.array1.findIndex((value)=>value==this.item_list[8])
                this.index2 = this.array2.findIndex((value)=>value==this.item_list[9])
                this.index3 = this.array3.findIndex((value)=>value==this.item_list[10])
            });
        },
	}
</script>

<style>
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
