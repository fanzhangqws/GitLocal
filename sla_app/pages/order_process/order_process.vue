<template>
    <view>
        <view class="uni-list">
            <view class="uni-list-cell">
                <view class="uni-list-cell-left">
                    处理类型
                </view>
                <view class="uni-list-cell-db">
                    <picker @change="bindPickerChange" :value="index" :range="path_list">
                        <view class="uni-input">{{path_list[index]}}</view>
                    </picker>
                </view>
            </view>
            <view class="uni-list-cell">
                <view class="uni-list-cell-left">
                    目的部门
                </view>
                <view class="uni-list-cell-db">
                    <checkbox-group @change="checkboxChange">
                        <label class="uni-list-cell uni-list-cell-pd" v-for="item in target_list[index]" :key="item.target_id">
                            <view>{{item.name}} </view>
                            <view><checkbox :value="item.target_id" :checked="item.checked" /></view>                            
                        </label>
                    </checkbox-group>
                </view>
            </view>
            <view class="uni-list-cell">
                <view class="uni-list-cell-left">
                     备注信息
                </view>
                <view class="uni-list-cell-db">
                    <view class="uni-textarea">
                        <textarea @blur="bindTextAreaBlur" auto-height="true" placeholder="备注"/>
                    </view>
                </view>                        
            </view>
            <view class="uni-list-cell">
                <view class="uni-list-cell-left">
                     对上一部门评价
                </view>
                <view class="uni-list-cell-db">
                    <my-issue :infoReceive='star_value'/>
                </view>                        
            </view>
        </view>
        <view>
        	<button  class="btn-logout" @tap="confirm">确认</button>
        </view>
    </view>
</template>

<script>
    import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
    import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
    import cmdTransition from "@/components/cmd-transition/cmd-transition.vue"
    import cmdCelItem from "@/components/cmd-cell-item/cmd-cell-item.vue"
    import cmdCelItem2 from "@/components/cmd-cell-item/mod-cmd-cell-item.vue"
    import myIssue from '@/components/myIssue.vue'
    import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"
    
    export default {
        components: {
            cmdNavBar,
            cmdPageBody,
            cmdTransition,
            cmdCelItem,
            cmdAvatar,
            cmdCelItem2,
            myIssue,
        },
        data() {
            return {
                id: '',
                return_id: '',
                index: 0,
                path_list: [],
                note: '',
                star_value: {"score":0},
                current_path:'',
                current_id_list: [],
                target_list: []
            };
        },
        mounted() {},
        onLoad: function(option) {
            this.id = option.id;
            this.return_id = option.return_id;
            // console.log("return_id: "+this.return_id)
        },
        onShow() {
            this.$api.request({
                url: '/order/get_next?id=' + this.id,
                method: 'GET'
            }).then((data) => {
                for (let item in data) {
                	// console.log(item);
                	this.path_list.push(data[item].path);
                    this.target_list.push(data[item].targets)
                }                
            });
            
        },
        methods: {
            bindTextAreaBlur: function (e) {
                this.note = e.detail.value
            },
            checkboxChange: function (e) {
                var items = this.target_list[this.index];
                this.current_id_list = e.detail.value;
                for (let i in items) {
                    items[i].checked = false;
                    for (let j in this.current_id_list) {
                        if (items[i].value == this.current_id_list[j]) {
                            items[i].checked = true;
                            break
                        }
                    }
                }
            },
            bindPickerChange: function(e) {
                // console.log('picker发送选择改变，携带值为', e.target.value)
                this.index = e.target.value
                this.current_path = this.path_list[e.target.value]
            },
            confirm () {
                var data = {
                    "id": this.return_id,
                    "path": this.current_path,
                    "targets": this.current_id_list,
                    "memo": this.note,
                    "score": this.star_value.score
                };
                // console.log(data)
                this.$api.request({
                    url: '/order/process',
                    method: 'POST',
                    data:data
                }).then(()=>{
                    uni.reLaunch({
                    	url: "/pages/list_order/list_order"
                    })
                });
            }
        }
    }
</script>

<style lang="scss">
    .btn-logout {
        margin-top: 100upx;
        width: 30%;
        border-radius: 50upx;
        font-size: 16px;
        color: #fff;
        background: linear-gradient(to right, #365fff, #36bbff);

        &-hover {
            background: linear-gradient(to right, #365fdd, #36bbfa);
        }
    }
</style>
