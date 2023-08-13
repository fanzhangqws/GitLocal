### NavBar 导航栏

导航栏组件，组件名：``cmd-nav-bar``，代码块： cmdNavBar。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdNavBar from "@/components/cmd-nav-bar/cmd-nav-bar.vue"
export default {
    components: {cmdNavBar}
}
```

用法：    
在内容区加入样式避免覆盖,top根据情况调整     
padding-top: 90upx;
margin-top: var(--status-bar-height);

```html
<cmd-nav-bar :fixed="false" back left-text="Back" title="场景管理" iconTwo="settings" font-color="#fff" background-color="linear-gradient(to right, rgb(17, 153, 142), rgb(56, 239, 125))"></cmd-nav-bar>
<cmd-nav-bar :fixed="false" leftTitle="HELLO" iconTwo="add"></cmd-nav-bar>
<cmd-nav-bar :fixed="false" right-color="#2196f3" right-text="添加场景" back title="场景管理"></cmd-nav-bar>
<cmd-nav-bar iconOne="menu" title="基本" iconTwo="share" iconThree="reload" iconFour="help"></cmd-nav-bar>
```
 
**属性说明：**

|属性名						|类型		|默认值	|说明																		|
|---							|----		|---		|---																		|
|fixed						|Boolean|true		|固定到页面顶部													|
|back							|Boolean|false	|导航栏左侧返回按钮，默认点击返回上层		|
|left-text				|String	|-			|左侧文字，可同显返回按钮								|
|left-title				|String	|-			|左侧显示标题，不可显示左侧文字图标标题	|
|right-text				|String	|-			|右侧文字																|
|right-color			|String	|-			|右侧文字颜色														|
|title						|String	|-			|导航栏标题															|
|font-color				|String	|-			|文字图标颜色														|
|background-color	|String	|-			|导航栏背景颜色													|
|icon-one					|String	|-			|图标一，不可与返回按钮,左侧标题同显		|
|icon-two					|String	|-			|图标二																	|
|icon-three				|String	|-			|图标三，须显有图标二										|
|icon-four				|String	|-			| 图标四，不可与右侧文字同显						|

**事件说明：**

|事件名称	|说明										|
|---			|---										|
|iconOne	|点击 图标一 触发事件		|
|iconTwo	|点击 图标二 触发事件		|
|iconThree|点击 图标三 触发事件		|
|iconFour	|点击 图标四 触发事件		|
|leftText	|点击 左侧文字 触发事件	|
|rightText|点击 右侧文字 触发事件	|
