### PageBody 导航栏内容页

导航栏内容页组件，组件名：``cmd-page-body``，代码块： cmdPageBody。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdPageBody from "@/components/cmd-page-body/cmd-page-body.vue"
export default {
    components: {cmdPageBody}
}
```

**用法**  
使用底部导航栏 ``cmd-bottom-nav`` 或顶部导航栏 ``cmd-nav-bar`` 自定义导航栏时，内容区默认充满屏幕。   
内容区使用过渡动画效果减少页面的闪烁，配合动画``cmd-transition``使用。

```html
<!-- 在使用顶部和底部导航栏时 -->
<cmd-page-body type="top-bottom">
  <!-- #ifdef H5 -->
  <cmd-transition name="fade-up">
    <home v-if="current == 0"></home>
    <person v-if="current == 1"></person>
  </cmd-transition>
  <!-- #endif -->
  <!-- 单使用顶部导航时，非H5端下v-if显示，可以在mounted后 -->
  <!-- #ifndef H5 -->
  <cmd-transition v-if="current == 0" name="fade-up">
    <home></home>
  </cmd-transition>
  <cmd-transition v-if="current == 1" name="fade-up">
    <person></person>
  </cmd-transition>
  <!-- #endif -->
</cmd-page-body>
```
 
**属性说明：**

|属性名				|类型	|默认值	|说明									|
|---				|----	|---	|---									|
|type				|String	|top	|使用导航栏类型：top、bottom、top-bottom|
|background-color	|String	|#ffffff|内容区背景颜色							|

