### Progress 进度条

进度条组件，组件名：``cmd-progress``，代码块： cmdProgress。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdProgress from "@/components/cmd-progress/cmd-progress.vue"
export default {
    components: {cmdProgress}
}
```

用法：
非H5端动态绘制会有卡顿情况，H5端没有。    
非H5端使用image/svg+xml背景方式，H5端正常使用svg。    

```html
<!-- 进度条 --> 
<cmd-progress :percent="30"></cmd-progress>
<cmd-progress :percent="59" :success-percent="10"></cmd-progress>
<cmd-progress :percent="50" :showInfo="false"></cmd-progress>
<cmd-progress :percent="80" status="active"></cmd-progress>
<cmd-progress :percent="50" status="success"></cmd-progress>
<cmd-progress :percent="70" status="exception"></cmd-progress>
<cmd-progress :percent="25" :stroke-width="24"></cmd-progress>
<cmd-progress :percent="68" stroke-color="linear-gradient(to right, #ef32d9, #89fffd)"></cmd-progress>
<cmd-progress :percent="88" stroke-shape="square"></cmd-progress>
<!-- 进度圈 -->
<cmd-progress type="circle" :percent="75"></cmd-progress>
<cmd-progress type="circle" :percent="75" :showInfo="false"></cmd-progress>
<cmd-progress type="circle" :percent="30" status="exception"></cmd-progress>
<cmd-progress type="circle" :percent="60" status="success"></cmd-progress>
<cmd-progress type="circle" :percent="0"></cmd-progress>
<cmd-progress type="circle" :percent="76" :stroke-width="24"></cmd-progress>
<cmd-progress type="circle" :percent="45" :gapDegree="66" stroke-color="#ef32d9"></cmd-progress>
<cmd-progress type="circle" :percent="88" gap-position="left" stroke-shape="square"></cmd-progress>
<cmd-progress type="circle" :percent="76" :width="40" stroke-shape="square"></cmd-progress>
<!-- 仪表盘 -->
<cmd-progress type="dashboard" :percent="75"></cmd-progress>
<cmd-progress type="dashboard" :percent="68" status="exception"></cmd-progress>
<cmd-progress type="dashboard" :percent="88" status="success"></cmd-progress>
<cmd-progress type="dashboard" :percent="43" :stroke-width="24"></cmd-progress>
<cmd-progress type="dashboard" :percent="30" stroke-color="#ef32d9"></cmd-progress>
<cmd-progress type="dashboard" :percent="34" stroke-shape="square"></cmd-progress>
<cmd-progress type="dashboard" :percent="p" :stroke-width="12"></cmd-progress>
```
 
**属性说明：**

|属性名					|类型		|默认值	|说明																																								|
|---						|----		|---		|---																																								|
|type						|String	|line		|类型默认：line，可选 line circle dashboard																					|
|percent				|Number	|0			|百分比值0-100 ，可能需要自己转成百分比的值																					|
|success-percent|Number	|0			|已完成的分段百分，仅支持类型line																										|
|show-info			|Boolean|true		|是否显示进度数值或状态图标																													|
|status					|String	|normal	|进度状态，可选：normal success exception （active仅支持类型line										|
|stroke-width		|Number	|6			|条线的宽度1-50，与width有关																												|
|stroke-color		|String	|-			|条线的颜色，渐变色仅支持类型line																										|
|stroke-shape		|String	|round	|条线两端的形状 可选：'round', 'square'																							|
|width					|Number	|80			|圆形进度条画布宽度,支持类型circle dashboard																				|
|gap-degree			|Number	|0			|圆形进度条缺口角度，可取值 0 ~ 360,支持类型circle dashboard												|
|gap-position		|String	|top		|圆形进度条缺口位置,可取值'top', 'bottom', 'left', 'right' ,支持类型circle dashboard|
