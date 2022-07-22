# 活动(Activity)

- [活动(Activity)](#活动activity)
  - [启停活动页面](#启停活动页面)
    - [Activity的启动和结束](#activity的启动和结束)
    - [Activity的生命周期](#activity的生命周期)
    - [Activity的启动模式](#activity的启动模式)
  - [在活动之间传递消息](#在活动之间传递消息)
    - [显式lntent和隐式Intent](#显式lntent和隐式intent)
    - [向下一个Activity发送数据](#向下一个activity发送数据)
    - [向上一个Activity返回数据](#向上一个activity返回数据)
  - [为活动补充附加信息](#为活动补充附加信息)
    - [利用资源文件配置字符串](#利用资源文件配置字符串)
    - [利用元数据传递配置信息](#利用元数据传递配置信息)
    - [给应用页面注册快捷方式](#给应用页面注册快捷方式)


## 启停活动页面

- 从当前页面跳到新页面，跳转代码如下：
`startActivity(new Intent(源页面.this,目标页面.class));`
- 从当前页面回到上一个页面，相当于关闭当前页面，返回代码如下：
  `finish();//结束当前的活动页面`
### Activity的启动和结束
### Activity的生命周期
### Activity的启动模式
## 在活动之间传递消息
### 显式lntent和隐式Intent
### 向下一个Activity发送数据
### 向上一个Activity返回数据
## 为活动补充附加信息
### 利用资源文件配置字符串
### 利用元数据传递配置信息
### 给应用页面注册快捷方式


