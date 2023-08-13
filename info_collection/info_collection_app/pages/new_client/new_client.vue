<template>
	<view class="uni-padding-wrap uni-common-mt">
		<view class="content">
                <view class="input-group">
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">公司名称：{{item_list[0]}}</text>
                        </view>                     
                    </view>
                   <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">员工数量：</text>
                        </view>
                        <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[1]" ></m-input>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">客户行业：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange" :value="index" :range="array">
                        	    <view class="uni-input">{{ array[index] }}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">客户主营业务：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[3]"></m-input>
                        </view>                       
                    </view>  
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">客户营销模式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[4]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">关键人：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[5]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">职务：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[6]"></m-input>
                        </view>                       
                    </view>                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">办公电话：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[7]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">手机号码：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[8]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">客户类型：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange1" :value="index1" :range="array1">
                        	    <view class="uni-input">{{ array1[index1] }}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">营销服务客户经理：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[10]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">营服客户经理联系方式：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[11]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">CRM系统客户名称：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[12]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">客户ID：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[13]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">代表号码：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[14]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">付费编码：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[15]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">月收入：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[16]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">宽带数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[17]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">宽带号：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[18]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">宽带归属：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange7" :value="index7" :range="array7">
                        	    <view class="uni-input">{{ array7[index7] }}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">宽带带宽：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[35]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">宽带费用：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[36]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">固话数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[19]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">固话号：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[20]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">固话月消费：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[37]"></m-input>
                        </view>                       
                    </view>
                    
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">天翼数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[21]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">智慧企业：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange2" :value="index2" :range="array2">
                        	    <view class="uni-input">{{array2[index2]}}</view>
                        	</picker>
                        </view>                        
                    </view> 
                                       
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">智慧企业套餐：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[38]"></m-input>
                        </view>                       
                    </view>                   
                                                                             
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">智慧企业数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[23]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">是否有光纤专线接入：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange3" :value="index3" :range="array3">
                        	    <view class="uni-input">{{array3[index3]}}</view>
                        	</picker>
                        </view>                        
                    </view>                     
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">专线接入号：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[25]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">是否有IP：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange4" :value="index4" :range="array4">
                        	    <view class="uni-input">{{array4[index4]}}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">IP数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[27]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">是否有数字电路：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange8" :value="index8" :range="array8">
                        	    <view class="uni-input">{{array8[index8]}}</view>
                        	</picker>
                        </view>                        
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">数字电路数量：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[40]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">数字电路条数：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="number" v-model="item_list[41]"></m-input>
                        </view>                       
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">数字电路总费用：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[42]"></m-input>
                        </view>
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">异网数字电路情况：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[43]"></m-input>
                        </view>
                    </view>
                    
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">是否有网站：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange5" :value="index5" :range="array5">
                        	    <view class="uni-input">{{array5[index5]}}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">是否有服务器：</text>
                        </view>
                        <view class="flex-item">
                            <picker @change="bindPickerChange6" :value="index6" :range="array6">
                        	    <view class="uni-input">{{array6[index6]}}</view>
                        	</picker>
                        </view>                        
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">问题清单：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[30]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">业务需求及商机描述：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[31]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">商机推进情况：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[32]"></m-input>
                        </view>                       
                    </view>
                    <view class="input-row border uni-flex uni-row">
                        <view class="flex-item" style="margin-top: 5upx;">
                        	<text class="title">存在的问题及支撑需求：</text>
                        </view>
                       <view class="flex-item">
                        	<m-input class="m-input" type="text" v-model="item_list[33]"></m-input>
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
                item_list:["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""],
                building_id:0,
                array: ['','党政军','制造业', '科技类', '金融投资', '地产物管', '教育', '医疗', '酒店', '餐饮', '互联网', '电商'],
                array1:['','他网用户','清单客户','忠诚客户','普通客户','预警客户','异动客户'],
                array2:['','有','无'],
                array3:['','是','否'],
                array4:['','是','否'],
                array5:['','是','否'],
                array6:['','是','否'],
                array7:['','本网','异网','本网+异网'],
                array8:['','是','否'],
                index: 0,
                index1:0,
                index2:0,
                index3:0,
                index4:0,
                index5:0,
                index6:0,
                index7:0,
                index8:0,
			}
		},
        computed:{
            
        },
		methods: {
            post_data(self) {
                var verify_input = true
                if (this.item_list[0]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：公司名称不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[2]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：客户行业不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[3]=='') {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：客户主营业务不能为空！',
                        duration: 4000
                    });
                }
                else if (this.item_list[1]!='' && !(this.item_list[1]>=0 && this.item_list[1]<=500)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：员工数量必须在0至500之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[7]!='' && (isNaN(this.item_list[7])| !((this.item_list[7]).startsWith('029')) | this.item_list[7].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：办公电话必须用11位数字表示，以029开始！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[8]!='' && (isNaN(this.item_list[8])| this.item_list[8].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：手机号码必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[11]!='' && (isNaN(this.item_list[11])| this.item_list[11].length!=11 )) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：营服客户经理联系方式必须用11位数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[13]!='' && isNaN(this.item_list[13])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：客户ID必须用数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[14]!='' && isNaN(this.item_list[14])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：代表号码必须用数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[15]!='' && isNaN(this.item_list[15])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：付费编码必须用数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[16]!='' && isNaN(this.item_list[16])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：月收入必须用数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[17]!='' && !(this.item_list[17]>=0 && this.item_list[17]<=20)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：宽带数量必须在0至20之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[19]!='' && !(this.item_list[19]>=0 && this.item_list[19]<=200)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：固话数量必须在0至200之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[20]!='' && isNaN(this.item_list[20])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：固话号必须用数字表示！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[21]!='' && !(this.item_list[21]>=0 && this.item_list[21]<=300)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：天翼数量必须在0至300之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[23]!='' && !(this.item_list[23]>=0 && this.item_list[23]<=20)) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：智慧企业数量必须在0至20之间！',
                        duration: 4000
                    });
                }
                else if  (this.item_list[27]!='' && isNaN(this.item_list[27])) {
                	verify_input = false
                    uni.showToast({
                        icon: 'none',
                        title: '提交失败！错误原因：IP数量必须用数字表示！',
                        duration: 4000
                    });
                } else {
                    var post_data = {
                        "item_list": this.item_list,
                        'building_id':this.building_id
                    }
                    this.$api.request({
                        url: '/infocollect/newclient',
                        data: post_data,
                        method: 'POST',
                        // header: { 'content-type': 'application/json', 'token': this.token }
                    }).then(data => {
                        //data为一个数组，数组第一项为错误信息，第二项为返回数据
                        uni.showToast({
                            icon: 'success',
                            title: '新增客户成功!',
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
                this.item_list[2] = this.array[e.target.value];                
            },
            bindPickerChange1: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index1 = e.target.value;
                this.item_list[9] = this.array1[e.target.value];                
            },
            bindPickerChange2: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index2 = e.target.value;
                this.item_list[22] = this.array2[e.target.value];                
            },
            bindPickerChange3: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index3 = e.target.value;
                this.item_list[24] = this.array3[e.target.value];                
            },
            bindPickerChange4: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index4 = e.target.value;
                this.item_list[26] = this.array4[e.target.value];                
            },
            bindPickerChange5: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index5 = e.target.value;
                this.item_list[28] = this.array5[e.target.value];                
            },
            bindPickerChange6: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index6 = e.target.value;
                this.item_list[29] = this.array6[e.target.value];                
            },
            bindPickerChange7: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index7 = e.target.value;
                this.item_list[34] = this.array7[e.target.value];                
            },
            bindPickerChange8: function(e) {
                console.log('picker发送选择改变，携带值为', e.target.value);
                this.index8 = e.target.value;
                this.item_list[39] = this.array8[e.target.value];                
            },
		},
        onShow() {
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
