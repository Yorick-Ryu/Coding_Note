# 共享参数SharedPreferences

## 共享参数的用法

SharedPreferences是Android的一个轻量级存储工具，采用的存储结构是Key-Value的键值对方式。

共享参数的存储介质是符合XML规范的配置文件。保存路径是：/data/data/应用包名/shared_prefs/文件名.xml

共享参数主要适用于如下场合：

- 简单且孤立的数据。若是复杂且相互间有关的数据，则要保存在数据库中
- 文本形式的数据。若是二进制数据,则要保存在文件中。
- 需要持久化存储的数据。在App退出后再次启动时，之前保存的数据仍然有效。


实际开发中，共享参数经常存储的数据有App的个性化配置信息、用户使用App的行为信息、临时需要保存的片段信息等。

示例：
```java
private SharedPreferences preferences = getSharedPreferences("config", Context.MODE_PRIVATE);
// 放数据
SharedPreferences.Editor editor = preferences.edit();
editor.putString("phone", etPhone.getText().toString());
editor.putString("pwd", etPwd.getText().toString());
editor.putBoolean("isRem", ckRem.isChecked());
// 提交数据
editor.commit();
// 取数据
etPhone.setText(preferences.getString("phone", null));
etPwd.setText(preferences.getString("pwd", null));
```

## 利用设备浏览器寻找共享参数文件

共享参数的存储介质是符合XML规范的配置文件。保存路径是：/data/data/应用包名/shared_prefs/文件名.xml
