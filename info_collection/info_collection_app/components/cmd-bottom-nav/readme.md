### BottomNav 底部导航栏

底部导航栏组件，组件名：``cmd-bottom-nav``，代码块： cmdBottomNav。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdBottomNav from "@/components/cmd-bottom-nav/cmd-bottom-nav.vue"
export default {
    components: {cmdBottomNav}
}
```

用法在内容区加入样式避免覆盖：margin-bottom: 118upx;

```html
<cmd-bottom-nav></cmd-bottom-nav>
<cmd-bottom-nav background-color="linear-gradient(to right, rgb(17, 153, 142), rgb(56, 239, 125))" :current="current" :list="list" text-auto></cmd-bottom-nav>
<cmd-bottom-nav :current="current" :list="list" border-color="red" background-color="#795548" font-color="#fff" active-font-color="rgb(255, 106, 68)"></cmd-bottom-nav>
```

```json
current: 0,
list:[{
	"pagePath": "/pages/tabbar/home/home",
	"text": "首页", 
	// 字体图标不可与图片共显
	"icon": "home",
	// src 大小限制为40kb，建议尺寸为 81px * 81px
	"src": "../../static/iocn-tabbar/home.png",
	"srcSelect": "../../static/iocn-tabbar/homeHL.png"
}]
```

**属性说明：**

|属性名						|类型		|默认值	|说明									|
|---							|----		|---		|---									|
|current					|Number	|0			|导航列表选中项				|
|list							|Array	|[]			|导航列表							|
|font-color				|String	|-			|文字颜色							|
|border-color			|String	|-			|底部上边线颜色				|
|background-color	|String	|-			|背景颜色							|
|active-font-color|String	|-			|激活文字颜色					|
|text-auto				|Boolean|false	|只在激活状态显示文本	|
|fixed						|Boolean|true		|固定到页面底部				|

**事件说明：**

|事件名称	|说明						|
|---		|---						|
|click		|点击 底部导航栏项 触发事件	|
