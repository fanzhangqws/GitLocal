### Input 输入框

输入框 组件名：``cmd-input``，代码块： cmdInput。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdInput from "@/components/cmd-input/cmd-input.vue"
export default {
    components: {cmdInput}
}
```

在 ``template`` 中使用组件

```html
<cmd-input placeholder="聚焦移除输入提交监听" :placeholder-style="{'color':'#f44336'}" @focus="fnFocus" @blur="fnBlur" @input="fnInput"
@confirm="fnConfirm"></cmd-input>
<cmd-input placeholder="聚焦输入默认值并清空输入框" type="text" value="聚焦输入默认值" focus clearable></cmd-input>
<cmd-input placeholder="聚焦输入并清空输入框" type="text" focus clearable></cmd-input>
<cmd-input placeholder="密码可见" type="password" v-model="password" displayable></cmd-input>
```


**Input 属性说明：**

|属性名						|类型						|默认值	|说明																				|
|---							|----						|---		|---																				|
|type							|String					|text		|输入类型 digit idcard number text password	|
|placeholder			|String					|-			|占位符																			|
|placeholder-style|Object					|-			|占位符样式																	|
|disabled					|Boolean				|false	|是否为禁用状态															|
|focus						|Boolean				|false	|自动获取焦点																|
|value						|String, Number	|-			|默认初始内容																|
|maxlength				|String, Number	|-			|最大输入长度																|
|clearable				|Boolean				|false	|是否显示清除按钮														|
|displayable			|Boolean				|false	|是否显示密码可见按钮												|

**事件说明：**

|事件名称	|说明					|
|---		|---					|
|focus		|键入聚焦输入框 监听事件|
|blur		|键出移除输入框 监听事件|
|input		|键入输入 监听事件		|
|confirm	|输入框提交 监听事件	|