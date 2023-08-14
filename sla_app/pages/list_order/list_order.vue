<template>
	<view class="uni-padding-wrap uni-common-mt">
		<view>
			<uni-segmented-control :current="current" :values="items" v-on:clickItem="onClickItem" ></uni-segmented-control>
		</view>
		<view class="content">
			<view v-show="current === 0">                
                <cmd-page-body type="top">
                  <cmd-transition name="fade-up">
                    <view>
                        <view class="input-view">
                          	<uni-icon type="search" size="22" color="#666666"></uni-icon>
                          	<input confirm-type="done" v-model="condition0" class="input" type="text" placeholder="输入搜索信息" />
                        </view>
                        <view class="cust-list">
                            <view class="cust-list-cell">
                                <view class="cust-cell-divide">
                                    开始时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_start0" :start="startDate" :end="endDate" @change="bindDateChange1">
                                        <view class="cust-uni-input">{{date_start0}}</view>
                                    </picker>
                                </view>
                                <view class="cust-cell-divide">
                                    结束时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_end0" :start="startDate" :end="endDate" @change="bindDateChange2">
                                        <view class="cust-uni-input">{{date_end0}}</view>
                                    </picker>
                                </view>
                                <view  class="cust-button">
                                    <button type="primary" plain="true" @click="search0">查询</button>
                                </view>
                            </view>
                        </view>
                        <mescroll-uni :down="downOption0" @down="downCallback0" :up="upOption0" @up="upCallback0" @init="mescrollInit0">
                            <view>
                            	<cmd-cel-item v-for="item in myorder_list" :title="item.id" :addon="item.update_time" :addon2="item.workarea" arrow 
                                @click="detail_search(item.id, current)"></cmd-cel-item>
                            </view>
                        </mescroll-uni>                       
                    </view>
                  </cmd-transition>
                </cmd-page-body>
			</view>
			<view v-show="current === 1">
                <cmd-page-body type="top">
                  <cmd-transition name="fade-up">
                    <view>
                        <view class="input-view">
                          	<uni-icon type="search" size="22" color="#666666"></uni-icon>
                          	<input confirm-type="done" v-model="condition1" class="input" type="text" placeholder="输入搜索信息" />
                        </view>
                        <view class="cust-list">
                            <view class="cust-list-cell">
                                <view class="cust-cell-divide">
                                    开始时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_start1" :start="startDate" :end="endDate" @change="bindDateChange3">
                                        <view class="cust-uni-input">{{date_start1}}</view>
                                    </picker>
                                </view>
                                <view class="cust-cell-divide">
                                    结束时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_end1" :start="startDate" :end="endDate" @change="bindDateChange4">
                                        <view class="cust-uni-input">{{date_end1}}</view>
                                    </picker>
                                </view>
                                <view  class="cust-button">
                                    <button type="primary" plain="true" @click="search1">查询</button>
                                </view>
                            </view>
                        </view>
                        <mescroll-uni :down="downOption1" @down="downCallback1" :up="upOption1" @up="upCallback1" @init="mescrollInit1">
                            <view>
                            	<cmd-cel-item v-for="item in pending_list" :title="item.id" :addon="item.update_time" arrow 
                            	@click="detail_search(item.id, current)"></cmd-cel-item>
                            </view>
                        </mescroll-uni>
                    </view>
                  </cmd-transition>
                </cmd-page-body>
			</view>
			<view v-show="current === 2">
				<cmd-page-body type="top">
				  <cmd-transition name="fade-up">
				    <view>
                        <view class="input-view">
                          	<uni-icon type="search" size="22" color="#666666"></uni-icon>
                          	<input confirm-type="done" v-model="condition2" class="input" type="text" placeholder="输入搜索信息" />
                        </view>
                        <view class="cust-list">
                            <view class="cust-list-cell">
                                <view class="cust-cell-divide">
                                    开始时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_start2" :start="startDate" :end="endDate" @change="bindDateChange5">
                                        <view class="cust-uni-input">{{date_start2}}</view>
                                    </picker>
                                </view>
                                <view class="cust-cell-divide">
                                    结束时间
                                </view>
                                <view class="uni-list-cell-db">
                                    <picker mode="date" :value="date_end2" :start="startDate" :end="endDate" @change="bindDateChange6">
                                        <view class="cust-uni-input">{{date_end2}}</view>
                                    </picker>
                                </view>
                                <view  class="cust-button">
                                    <button type="primary" plain="true" @click="search2">查询</button>
                                </view>
                            </view>
                        </view>
                        <mescroll-uni :down="downOption2" @down="downCallback2" :up="upOption2" @up="upCallback2" @init="mescrollInit2">
                            <view>
                            	<cmd-cel-item class="cmd-finish" v-for="item in history_list" :title="item.id" :addon="item.status"
                            	 :addon2="item.workarea" arrow @click="detail_search(item.id, current)"></cmd-cel-item>
                            </view>
                        </mescroll-uni>
				    </view>
				  </cmd-transition>
				</cmd-page-body>
			</view>
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
		data() {
            const currentDate = this.getDate({
                format: true
            })
			return {
				items: [
					'我的已办',
					'我的待办',
					'历史订单'
				],
				current: 1,
				activeColor: '#007aff',
                pending_list:[],
                myorder_list:[],
                history_list:[],
                date_start0: currentDate,
                date_end0: currentDate,
                condition0:'',
                date_start1: currentDate,
                date_end1: currentDate,
                condition1:'',
                date_start2: currentDate,
                date_end2: currentDate,
                condition2:'',
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
                mescroll1: null, //mescroll实例对象
                // 下拉刷新的配置
                downOption1: { 
                    use: true, // 是否启用下拉刷新; 默认true
                    auto: false, // 是否在初始化完毕之后自动执行下拉刷新的回调; 默认true
                },
                // 上拉加载的配置
                upOption1: {
                    use: true, // 是否启用上拉加载; 默认true
                    auto: false, // 是否在初始化完毕之后自动执行上拉加载的回调; 默认true
                    isLock: false, // 是否锁定上拉加载 (可用于不触发upCallback,只保留回到顶部按钮的场景)
                    page: {
                        num: 1, // 当前页码,默认0,回调之前会加1,即callback(page)会从1开始
                        size: 10 // 每页数据的数量,默认10
                    },
                    noMoreSize: 3, // 配置列表的总数量要大于等于5条才显示'-- END --'的提示
                    empty: {
                        tip: '暂无相关数据'
                    }
                },
                mescroll2: null, //mescroll实例对象
                // 下拉刷新的配置
                downOption2: { 
                    use: true, // 是否启用下拉刷新; 默认true
                    auto: false, // 是否在初始化完毕之后自动执行下拉刷新的回调; 默认true
                },
                // 上拉加载的配置
                upOption2: {
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
            if (this.current==1){
                this.mescroll1 && this.mescroll1.onReachBottom();
            }
            if (this.current==2){
                this.mescroll2 && this.mescroll2.onReachBottom();
            }           
            if (this.current==0){
                this.mescroll0 && this.mescroll0.onReachBottom();
            }
        },
        // 必须注册列表滚动事件,使下拉刷新生效
        onPageScroll(e) {
            if (this.current==2){
                this.mescroll2 && this.mescroll2.onPageScroll(e);
            }
            if (this.current==1){
                this.mescroll1 && this.mescroll1.onPageScroll(e);
            }
            if (this.current==0){
                this.mescroll0 && this.mescroll0.onPageScroll(e);
            }
        },
        computed: {
            startDate() {
                return this.getDate('start');
            },
            endDate() {
                return this.getDate('end');
            },
        },
		methods: {
            // mescroll组件初始化的回调,可获取到mescroll对象
            mescrollInit2(mescroll2) {
                this.mescroll2 = mescroll2;
            },
            mescrollInit1(mescroll1) {
                this.mescroll1 = mescroll1;
            },
            mescrollInit0(mescroll0) {
                this.mescroll0 = mescroll0;
            },
            /*下拉刷新的回调, 有三种处理方式: */
            downCallback0(mescroll0){
                var data = {
                    "query": this.condition0,
                    "stime":this.date_start0,
                    "etime":this.date_end0,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/order/myorder',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.myorder_list = data.orders
                    let curPageData = data.orders;
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    mescroll0.endByPage(curPageData.length, totalPage);
                    mescroll0.endSuccess()
                });
            },
            /*下拉刷新的回调, 有三种处理方式: */
            downCallback1(mescroll1){
                var data = {
                    "query": this.condition1,
                    "stime":this.date_start1,
                    "etime":this.date_end1,
                    "pageNum": 1,
                    "pageSize": 10,
                }
                this.$api.request({
                    url: '/order/pending',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.pending_list = data.orders
                    let curPageData = data.orders;
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    mescroll1.endByPage(curPageData.length, totalPage);
                    mescroll1.endSuccess()
                });
            },
            /*下拉刷新的回调, 有三种处理方式: */
            downCallback2(mescroll2){
                var data = {
                    "query": this.condition2,
                    "stime":this.date_start2,
                    "etime":this.date_end2,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/order/history',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.history_list = data.orders
                    let curPageData = data.orders;
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    mescroll2.endByPage(curPageData.length, totalPage);
                    mescroll2.endSuccess()
                });
            },
            /*上拉加载的回调*/
            upCallback0(mescroll0) {
                // 此时mescroll会携带page的参数:
                let pageNum = mescroll0.num; // 页码, 默认从1开始
                let pageSize = mescroll0.size; // 页长, 默认每页10条
                var data = {
                    "query": this.condition0,
                    "stime":this.date_start0,
                    "etime":this.date_end0,
                    "pageNum": mescroll0.num,
                    "pageSize": mescroll0.size,
                }
                this.$api.request({
                    url: '/order/myorder',
                    method: 'POST',
                    data:data
                }).then((data)=>{                    
                    // 接口返回的当前页数据列表 (数组)
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    
                    // 成功隐藏下拉加载状态
                    //方法一(推荐): 后台接口有返回列表的总页数 totalPage
                    mescroll0.endByPage(curPageData.length, totalPage); 
                    
                    //设置列表数据
                    // if(mescroll.num == 1) this.dataList = []; //如果是第一页需手动制空列表
                    if(mescroll0.num > 1){
                        this.myorder_list = this.myorder_list.concat(curPageData); //追加新数据
                    }
                    
                });
            },
            /*上拉加载的回调*/
            upCallback1(mescroll1) {
                // 此时mescroll会携带page的参数:
                let pageNum = mescroll1.num; // 页码, 默认从1开始
                let pageSize = mescroll1.size; // 页长, 默认每页10条
                var data = {
                    "query": this.condition1,
                    "stime":this.date_start1,
                    "etime":this.date_end1,
                    "pageNum": mescroll1.num,
                    "pageSize": mescroll1.size,
                }
                this.$api.request({
                    url: '/order/pending',
                    method: 'POST',
                    data:data
                }).then((data)=>{                    
                    // 接口返回的当前页数据列表 (数组)
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    
                    // 成功隐藏下拉加载状态
                    //方法一(推荐): 后台接口有返回列表的总页数 totalPage
                    mescroll1.endByPage(curPageData.length, totalPage); 
                    
                    //设置列表数据
                    // if(mescroll.num == 1) this.dataList = []; //如果是第一页需手动制空列表
                    if(mescroll1.num > 1){
                        this.pending_list = this.pending_list.concat(curPageData); //追加新数据
                    }
                    
                });
            },
            /*上拉加载的回调*/
            upCallback2(mescroll2) {
                // 此时mescroll会携带page的参数:
                let pageNum = mescroll2.num; // 页码, 默认从1开始
                let pageSize = mescroll2.size; // 页长, 默认每页10条
                var data = {
                    "query": this.condition2,
                    "stime":this.date_start2,
                    "etime":this.date_end2,
                    "pageNum": mescroll2.num,
                    "pageSize": mescroll2.size,
                }
                this.$api.request({
                    url: '/order/history',
                    method: 'POST',
                    data:data
                }).then((data)=>{                    
                    // 接口返回的当前页数据列表 (数组)
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    
                    // 成功隐藏下拉加载状态
                    //方法一(推荐): 后台接口有返回列表的总页数 totalPage
                    mescroll2.endByPage(curPageData.length, totalPage); 
                    
                    //设置列表数据
                    // if(mescroll.num == 1) this.dataList = []; //如果是第一页需手动制空列表
                    if(mescroll2.num > 1){
                        this.history_list = this.history_list.concat(curPageData); //追加新数据
                    }
                    
                });
            },
            detail_search(id, seg_id){
                uni.navigateTo({
                	url:"/pages/detail/detail?id="+id+"&segment_id="+seg_id
                })
            },
            bindDateChange1: function(e) {
                this.date_start0 = e.target.value
            },
            bindDateChange2: function(e) {
                this.date_end0 = e.target.value
            },
            bindDateChange3: function(e) {
                this.date_start1 = e.target.value
            },
            bindDateChange4: function(e) {
                this.date_end1 = e.target.value
            },
            bindDateChange5: function(e) {
                this.date_start2 = e.target.value
            },
            bindDateChange6: function(e) {
                this.date_end2 = e.target.value
            },
            getDate(type) {
                const date = new Date();
                let year = date.getFullYear();
                let month = date.getMonth() + 1;
                let day = date.getDate();

                if (type === 'start') {
                    year = year - 60;
                } else if (type === 'end') {
                    year = year + 2;
                }
                month = month > 9 ? month : '0' + month;;
                day = day > 9 ? day : '0' + day;
                return `${year}-${month}-${day}`;
            },
			onClickItem(index) {
				if (this.current !== index) {
					this.current = index;
				}
			},
            search0() {
                var data = {
                    "query": this.condition0,
                    "stime":this.date_start0,
                    "etime":this.date_end0,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/order/myorder',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.myorder_list = data.orders
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    this.mescroll0.endByPage(curPageData.length, totalPage);
                });
            },
            search1() {
                var data = {
                    "query": this.condition1,
                    "stime":this.date_start1,
                    "etime":this.date_end1,
                    "pageNum": 1,
                    "pageSize": 10,
                }
                this.$api.request({
                    url: '/order/pending',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.pending_list = data.orders
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    this.mescroll1.endByPage(curPageData.length, totalPage);
                });
            },
            search2() {
                var data = {
                    "query": this.condition2,
                    "stime":this.date_start2,
                    "etime":this.date_end2,
                    "pageNum": 1,
                    "pageSize": 9,
                }
                this.$api.request({
                    url: '/order/history',
                    method: 'POST',
                    data:data
                }).then((data)=>{
                    this.history_list = data.orders
                    let curPageData = data.orders; 
                    // 接口返回的总页数 (比如列表有26个数据,每页10条,共3页; 则totalPage值为3)
                    let totalPage = data.totalPage; 
                    this.mescroll2.endByPage(curPageData.length, totalPage);
                });
            },
            yyyymmddhhmmss(dateIn) {
                var yyyy = dateIn.getFullYear();
                var mm = dateIn.getMonth() < 9 ? "0" + (dateIn.getMonth() + 1) : (dateIn.getMonth() + 1); // getMonth() is zero-based
                var dd  = dateIn.getDate() < 10 ? "0" + dateIn.getDate() : dateIn.getDate();
                var hh = dateIn.getHours() < 10 ? "0" + dateIn.getHours() : dateIn.getHours();
                var min = dateIn.getMinutes() < 10 ? "0" + dateIn.getMinutes() : dateIn.getMinutes();
                var ss = dateIn.getSeconds() < 10 ? "0" + dateIn.getSeconds() : dateIn.getSeconds();
                return "".concat(yyyy).concat(mm).concat(dd).concat(hh).concat(min).concat(ss);
            },
		},
        onShow() {
                    	
        },
	}
</script>

<style>
    .input-view {
    	display: flex;
    	align-items: center;
    	flex-direction:row;
    	background-color: #e7e7e7;
    	height: 30px;
    	border-radius: 15px;
    	padding: 0 10px;
    	flex: 1;
        margin-left: 20upx;
        margin-right: 20upx;
    }
    
    .input {
    	flex: 1;
    	padding: 0 5px;
    	height: 24px;
    	line-height: 24px;
    	font-size: 14px;
    }

    .cust-uni-input {
        height: 50upx;
        padding: 10upx 10upx;
        font-size:14px;
        background:#FFF;
        flex: 1;
        border-bottom: 2upx solid #007aff;
    }

    .cust-list {
    	background-color: #FFFFFF;
    	position: relative;
    	width: 95%;
    	display: flex;
        margin: 5px;
    	flex-direction: column;
    }
    
    .cust-list-cell {
    	position: relative;
    	display: flex;
    	flex-direction: row;
    	justify-content: space-between;
    	align-items: center;
        margin-left: 20upx;
    }
    
    .cust-cell-divide {
    	position: relative;
    	display: block;
    	color: #007aff;
        box-sizing: border-box;
        border-color: #007aff;
        border-radius: 25px;
    	padding:0upx 10upx;
        border-width: 1cm;
    }
    
    .cust-button {
    }
    
    .cust-button > button {
        line-height: 30px;
        font-size: 14px;
        padding: 0 10px 0 10px;
    }
</style>
