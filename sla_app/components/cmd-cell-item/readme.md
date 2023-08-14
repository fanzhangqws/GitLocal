### CellItem 列表单元

列表单元组件，组件名：``cmd-cell-item``，代码块： cmdCellItem。

**使用方式：**

在 ``script`` 中引用组件 

```javascript
import cmdCellItem from '@/components/cmd-cell-item/cmd-cell-item.vue'
export default {
    components: {cmdCellItem}
}
```

一般用法

```html
<cmd-cell-item addon="附加文案" arrow></cmd-cell-item>
<cmd-cell-item title="普通条目" />
<cmd-cell-item title="动作条目" arrow @click="fnClick" />
<cmd-cel-item title="昵称" addon="Slimmer" arrow hover-class="cel-item-hover"></cmd-cel-item>
```

带描述信息、开关、禁用

```html
<cmd-cell-item title="交通银行(尾号3089)" brief="展示摘要描述" addon="附加文案" arrow />
<cmd-cell-item title="交通银行(尾号3089)" brief="展示摘要描述" disabled addon="禁用项" />
<cmd-cell-item title="交通银行(尾号3089)" brief="展示摘要描述" show-switch @switch="fnClick" switch-color="#2f86f6" />
```


附加文案2

```html
<cmd-cell-item title="普通条目" addon="附加文案" addon2="面向金融场景的Vue移动端UI组件库，丰富、灵活、实用，快速搭建优质的金融类产品，让复杂的金融场景变简单。基于「合理、好用」设计价值观，从交互操作、视觉抽象、图形可视等角度共同解决问题。" />
```

插槽

```html
<cmd-cell-item title="插槽" slot-left addon="附加文案">
    <cmd-avatar icon='user' :size="50" :make="{'color':'#2f86f6','background':'#111a34'}"></cmd-avatar>
</cmd-cell-item>
```

**cmdCellItem 属性说明：**

|属性名			|类型	|默认值	|说明								|
|---			|----	|---	|---								|
|title			|String	|-		|标题								|
|brief			|String	|-		|标题描述文本						|
|addon			|String	|-		|附加文本 右侧						|
|addon2			|String	|-		|附加文本2 item下文字说明			|
|arrow			|Boolean|false	|动作箭头标识						|
|disabled		|Boolean|false	|是否禁用项							|
|no-border		|Boolean|false	|无边框项							|
|show-switch	|Boolean|false	|显示开关Switch						|
|switch-state	|Boolean|false	|开关状态Switch是否被选中			|
|switch-color	|String	|-		|开关颜色							|
|slot-left		|Boolean|false	|插槽左 不可同时打开两个插槽		|
|slot-right		|Boolean|false	|插槽右 不可再使用switch addon|

**cmdCellItem 事件说明：**

|事件称名	|说明					|返回参数		|
|---		|----					|---			|
|click		|点击 item项 触发事件	|-				|
|switch		|点击切换 Switch 时触发	|{value:checked}|
