<template>
	<view class="uni-padding-wrap uni-common-mt">
		<view class="content">
                <cmd-transition name="fade-up">
                    <view>
                        <view  class="uni-flex uni-row">
                            <view  class="flex-item">
                                <button class="btn-logout" type="primary" @tap="new_client(building_id)">新增客户</button>
                            </view>
                            <view  class="flex-item" style="width: 50upx;">
                            </view>
                        	<view class="flex-item input-view">
                        	    <uni-icon type="search" size="22" color="#666666"></uni-icon>
                        	    <input confirm-type="done" v-model="condition0" class="input" type="text" placeholder="输入搜索信息" @confirm="search0()" />
                        	</view>
                        </view>
                        
                        <view>
                            <cmd-cel-item title="物业信息"  arrow  @click="building_detail_search(building_id)"></cmd-cel-item>
                        </view>
                        <mescroll-uni :down="downOption0" @down="downCallback0" :up="upOption0" @up="upCallback0" @init="mescrollInit0">
                            <view>
                                <cmd-cel-item v-for="item in client_list" :title="item.company_name"  arrow  @click="client_detail_search(item.id)"></cmd-cel-item>
                            </view>
                        </mescroll-uni>                       
                    </view>
                </cmd-transition>
		</view>
	</view>
</template>

<script>
    import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
    import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
    import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"
    import cmdCelItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
	import uniSegmentedControl from '@/components/uni-segmented-control.vue'
    import MescrollUni from '@/components/wenju-mescroll/mescroll-uni.vue'
    import uniIcon from '@/components/uni-icon.vue'
      
	export default {
        components: {
          cmdNavBar,
          cmdPageBody,
          cmdTransition,
          cmdCelItem,
          uniSegmentedControl,
          uniIcon,
          MescrollUni
        },
        onLoad: function(option) {
            this.building_id = option.building_id;
        },
		data() {
			return {
				activeColor: '#007aff',
                client_list:[],
                condition0:'',
                building_id:0,
                mescroll0: null, //mescroll实例对象
                // 下拉刷新的配置
                downOption0: { 
                    use: true, // 是否启用下拉刷新; 默认true
                    auto: false, // 是否在初始化完毕之后自动执行下拉刷新的回调; 默认true
                },
                // 上拉加载的配置
                upOption0: {
                    use: true, // 是否启用上拉加载; 默认true
                    auto: false, // 是否在初始化完毕之后自动执行上拉加载的回调; 默认true
                    isLock: false, // 是否锁定上拉加载 (可用于不触发upCallback,只保留回到顶部按钮的场景)
                    page: {
                        num: 1, // 当前页码,默认0,回调之前会加1,即callback(page)会从1开始
                        size: 9 // 每页数据的数量,默认10
                    },
                    noMoreSize: 3, // 配置列表的总数量要大于等于5条才显示'-- END --'的提示
                    empty: {
                        tip: '暂无相关数据'
                    }
                },
			}
		},
        // 必须注册滚动到底部的事件,使上拉加载生效
        onReachBottom() {
            this.mescroll0 && this.mescroll0.onReachBottom();
        },
        // 必须注册列表滚动事件,使下拉刷新生效
        onPageScroll(e) {
            this.mescroll0 && this.mescroll0.onPageScroll(e);
        },
		methods: {
            // mescroll组件初始化的回调,可获取到mescroll对象
            mescrollInit0(mescroll0) {
                this.mescroll0 = mescroll0;
            },
            /*下拉刷新的回调, 有三种处理方式: */
            downCallback0(mescroll0){
                var data = {
                    "query": this.condition0,
                    'building_id':this.building_id,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/infocollect/clientlist',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.client_list = data.client
                    let curPageData = data.client;
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    mescroll0.endByPage(curPageData.length, totalPage);
                    mescroll0.endSuccess()
                });
            },
            /*上拉加载的回调*/
            upCallback0(mescroll0) {
                // 此时mescroll会携带page的参数:
                let pageNum = mescroll0.num; // 页码, 默认从1开始
                let pageSize = mescroll0.size; // 页长, 默认每页10条
                var data = {
                    "query": this.condition0,
                    'building_id':this.building_id,
                    "pageNum": mescroll0.num,
                    "pageSize": mescroll0.size,
                }
                this.$api.request({
                    url: '/infocollect/clientlist',
                    method: 'POST',
                    data:data
                }).then((data)=>{                    
                    // 接口返回的当前页数据列表 (数组)
                    let curPageData = data.client; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    
                    // 成功隐藏下拉加载状态
                    //方法一(推荐): 后台接口有返回列表的总页数 totalPage
                    mescroll0.endByPage(curPageData.length, totalPage); 
                    
                    //设置列表数据
                    // if(mescroll.num == 1) this.dataList = []; //如果是第一页需手动制空列表
                    if(mescroll0.num > 1){
                        this.client_list = this.client_list.concat(curPageData); //追加新数据
                    }
                    
                });
            },
            new_client(id){
                uni.navigateTo({
                	url:"/pages/new_client/new_client?building_id="+id
                })
            },
            building_detail_search(id){
                uni.navigateTo({
                	url:"/pages/building_detail/building_detail?building_id="+id
                })
            },
            client_detail_search(id){
                uni.navigateTo({
                	url:"/pages/client_detail/client_detail?client_detail_id="+id + "&building_id=" + this.building_id
                })
            },
            search0() {
                var data = {
                    "query": this.condition0,
                    'building_id':this.building_id,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/infocollect/clientlist',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.client_list = data.client
                    let curPageData = data.client;
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage;
                    this.mescroll0.endByPage(curPageData.length, totalPage);
                });
            },
		},
        onShow() {

        },
	}
</script>

<style>
    .btn-logout {
    	display: flex;
    	align-items: center;        
        flex-direction:row;
        width: 105%;
        height: 30px;
        border-radius: 50upx;
        font-size: 10px;
        color: #FFFFFF;
        text-align: center;
        /* padding: 10upx 5upx; */
        background: linear-gradient(to right, #365fff, #36bbff);
        &-hover {
            background: linear-gradient(to right, #365fdd, #36bbfa);
        }
    },
    .input-view {
    	display: flex;
    	align-items: center;
    	flex-direction:row;
    	background-color: #e7e7e7;
    	height: 30px;
    	border-radius: 15px;
        padding: 0 10px;
    	flex: 1;
        margin-left: 5upx;
        margin-right: 10upx;
    }
    
    .input {
    	flex: 1;
    	padding: 0 5px;
    	height: 24px;
    	line-height: 24px;
    	font-size: 14px;
    }
</style>
