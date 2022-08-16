# 应用组件Application

## Application的生命周期

Application是Android的一大组件，在App运行过程中有且仅有一个Application对象贯穿整个生命周期。

```java
@Override
public void onCreate() {
    super.onCreate();
    Log.d("yu", "MyApp.onCreate: ");
}
```

```java
// 在配置改变时调用，例如从竖屏变为横屏。
@Override
public void onConfigurationChanged(@NonNull Configuration newConfig) {
    super.onConfigurationChanged(newConfig);
    Log.d("yu", "onConfigurationChanged: ");
}
```
## 利用Application操作全局变量

全局的意思是其他代码都可以引用该变量，因此全局变量是共享数据和消息传递的好帮手。适合在Application中保存的全局变量主要有下面3类数据：

- 会频繁读取的信息，如用户名、手机号等。
- 不方便由意图传递的数据，例如位图对象、非字符串类型的集合对象等。
- 容易因频繁分配内存而导致内存泄漏的对象，如Handler对象等。


注意：不建议放太多数据到内存中，可能导致应用闪退。

## 利用Room简化数据库操作


Room是谷歌公司推出的数据库处理框架，该框架同样基于SQLite，但它通过注解技术极大简化了数据库操作，减少了原来相当一部分编码工作量。

在使用Room之前，要先修改模块的build.gradle文件，往dependencies节点添加下面两行配置,表示导入指定版本的Room库：
```groovy
implementation 'androidx.room:room-runtime:2.2.5'
annotationProcessor 'androidx.room:room-compiler:2.2.5'
```
### Room框架的编码步骤

以录入书籍信息为例，使用Room框架的编码过程分为下列五步:

编写书籍信息表对应的实体类，该类添加“@Entity”注解。
编写书籍信息表对应的持久化类,该类添加“@Dao”注解。
编写书籍信息表对应的数据库类，该类从RoomDatabase派生而来，并添加“@Database”注解。

在自定义的Application类中声明书籍数据库的唯一实例。在操作书籍信息表的地方获取数据表的持久化对象。