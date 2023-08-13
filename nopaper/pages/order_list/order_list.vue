<template>
    <view v-if="token" class="content">
        <uni-list v-for="(item, index) in list_data" :key="index">
            <uni-list-item :title="item.name" :note="item.note"></uni-list-item>
        </uni-list>
    </view>
</template>

<script>
import { mapState } from 'vuex';
import mSearch from '../../components/mehaotian-search/mehaotian-search.vue';
import { uniList, uniListItem } from '@dcloudio/uni-ui';

export default {
    components: { uniList, uniListItem },
    data() {
        return {
            list_data: [],
            token: ''
        };
    },
    computed: mapState(['forcedLogin', 'hasLogin', 'userName']),
    methods: {
        get_data() {
            
            // Promise
            uni.request({
                url: 'http://x.x.x.x/nopaper/api/order/list',
                method: 'GET',
                header: { 'content-type': 'application/json', token: this.token },
                success: res => {
                    
                    for (var item of res.data.data) {
                        console.log(item.name);
                        var temp = {};
                        temp['name'] = '客户名称: ' + item.name;
                        temp['note'] = '身份证后4位: ' + item.cert + '，预受理单状态: ' + item.status;
                        this.list_data.push(temp);
                    }

                    console.log(this.list_data);
                },
                fail: res => {
                    console.log(res);
                }
            });
        }
    },
    onShow() {
        this.token = uni.getStorageSync('token');
        if (this.token) {
        	this.get_data(), console.log('load data');
        };
    },
    onHide(){
        this.list_data=[]
    }
};
</script>

<style></style>
