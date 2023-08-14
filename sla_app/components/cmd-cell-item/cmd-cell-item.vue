<template>
    <view class="cmd-cell-item" :class="{'is-disabled': disabled,'no-border': noBorder }" @tap="$_click" :hover-class="hoverClass">
        <view class="cmd-cell-item-body">
            <view class="cmd-cell-item-left" v-if="slotLeft">
                <slot></slot>
            </view>
            <view class="cmd-cell-item-content">
                <view class="cmd-cell-item-title" v-if="title" v-text="title"></view>
                <view class="cmd-cell-item-brief" v-if="brief" v-text="brief"></view>
            </view>
            <view class="cmd-cell-item-right" v-if="slotRight">
                <slot></slot>
                <view class="cmd-cell-icon-arrow-right">
                    <cmd-icon v-if="arrow" type="chevron-right" size="24" color="#C5CAD5"></cmd-icon>
                </view>
            </view>
            <view class="cmd-cell-item-right" style="width: 450upx;" v-if="!slotRight">
                <view style="display: flex;flex-direction: column;align-items: flex-end;">
                    <view>{{addon}}</view>
                    <!-- <text >{{addon}}</text> -->
                    <view v-if="addon2" v-text="addon2" class="uni-common-pl" style="font-size: 24upx;color: #858b9c;"></view>
                </view>
                <view class="cmd-cell-icon-arrow-right">
                    <switch v-if="showSwitch" :color="switchColor" :disabled='disabled' :checked="switchState" @change="$_switch" />
                    <cmd-icon v-if="arrow" type="chevron-right" size="24" color="#C5CAD5"></cmd-icon>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
    import cmdIcon from '../cmd-icon/cmd-icon.vue'

    export default {
        name: 'cmd-cell-item',

        components: {
            cmdIcon
        },

        props: {
            prefix: {
                type: String,
                default: ''
            },
            /**
             * 标题
             */
            title: {
                type: String,
                default: ''
            },
            /**
             * 标题描述文本
             */
            brief: {
                type: String,
                default: ''
            },
            /**
             * 附加文本
             */
            addon: {
                type: String,
                default: ''
            },
            /**
             * 附加文本2 item下文字说明
             */
            addon2: {
                type: String,
                default: ''
            },
            /**
             * 动作箭头标识
             */
            arrow: {
                type: Boolean,
                default: false
            },
            /**
             * 是否禁用项
             */
            disabled: {
                type: Boolean,
                default: false
            },
            /**
             * 无边框项
             */
            noBorder: {
                type: Boolean,
                default: false
            },
            /**
             * 显示开关
             */
            showSwitch: {
                type: Boolean,
                default: false
            },
            /**
             * 开关状态 是否被选中
             */
            switchState: {
                type: Boolean,
                default: false
            },
            /**
             * 开关颜色
             */
            switchColor: {
                type: String,
                default: ''
            },
            /**
             * 插槽左 不可同时打开两个插槽
             */
            slotLeft: {
                type: Boolean,
                default: false
            },
            /**
             * 插槽右 不可再使用switch addon
             */
            slotRight: {
                type: Boolean,
                default: false
            },
            /**
             * 指定按钮按下去的样式类
             */
            hoverClass: {
                type: String,
                default: 'cmd-cell-item-hover'
            }
        },

        methods: {
            /**
             * item项点击事件
             */
            $_click(e) {
                if (!this.disabled) {
                    this.$emit('click', e)
                }
            },
            /**
             * 开关触发改变事件
             */
            $_switch(e) {
                if (!this.disabled) {
                    this.$emit('switch', e)
                }
            }
        }

    }
</script>

<style lang="scss">
    /**
   * 列表单元样式属性变量
   */
    $cmd-cell-item-min-height:100upx;
    $cmd-cell-item-padding-v:20upx;
    $cmd-cell-item-margin-h:20upx;
    $cmd-cell-item-title-color:#111A34;
    $cmd-cell-item-title-font-size:32upx;
    $cmd-cell-item-brief-color:#858B9C;
    $cmd-cell-item-brief-font-size:24upx;
    $cmd-cell-item-right-color:#858B9C;
    $cmd-cell-item-right-font-size:32upx;
    $cmd-cell-item-border-color:#E2E4EA;

    .cmd-cell-item {
        position: relative;

        &.no-border .cmd-cell-item-body {
            &::before {
                display: none;
            }
        }

        &-body {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: $cmd-cell-item-min-height;
            padding-top: $cmd-cell-item-padding-v;
            padding-bottom: $cmd-cell-item-padding-v;
            margin-left: $cmd-cell-item-margin-h;
            margin-right: $cmd-cell-item-margin-h;
            box-sizing: border-box;

            &::before {
                content: '';
                position: absolute;
                z-index: 2;
                background-color: $cmd-cell-item-border-color;
                transform-origin: 100% 50%;
                transform: scaleY(0.5) translateY(100%);

                @media (min-resolution: 3dppx) {
                    transform: scaleY(0.33) translateY(100%)
                }

                bottom: 0;
                left: 0;
                right: auto;
                top: auto;
                width: 100%;
                height: 2upx;
                transform-origin: 50% 100%;
            }
        }

        &-left {
            flex-shrink: 0;
            margin-right: 32upx;
        }

        &-title {
            line-height: 1.2;
        }

        &-brief {
            color: $cmd-cell-item-brief-color;
            font-size: $cmd-cell-item-brief-font-size;
            line-height: 1.4;
            margin-top: 8upx;
        }

        &-content {
            flex: 1 1 0%;
            color: $cmd-cell-item-title-color;
            font-size: $cmd-cell-item-title-font-size;
            line-height: 1.2;
        }

        &-right {
            flex-shrink: 0;
            margin-left: 12upx;
            display: inline-flex;
            align-items: center;
            justify-content: flex-end;
            color: $cmd-cell-item-right-color;
            font-size: $cmd-cell-item-right-font-size;

            .cmd-cell-addon-text {
                font-size: $cmd-cell-item-brief-font-size;
            }

            .cmd-cell-icon-arrow-right {
                margin-left: 6upx;
                margin-right: -6upx;
                color: #C5CAD5;
            }
        }

        &-children {
            padding: $cmd-cell-item-padding-v 0;
        }

        &.is-disabled {

            &,
            .cmd-cell-item-content,
            .cmd-cell-item-title,
            .cmd-cell-item-brief,
            .cmd-cell-item-left,
            .cmd-cell-item-right,
            .cmd-cell-item-children {
                color: #C5CAD5;
            }
        }

        &-hover {
            background: #efefef;
        }

    }
</style>
