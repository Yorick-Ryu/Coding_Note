# 共享参数SharedPreferences

[TOC]

[数据和文件存储概览  | Android 开发者  | Android Developers](https://developer.android.com/training/data-storage)

## 安卓存储的4种方式

Android 使用的文件系统类似于其他平台上基于磁盘的文件系统。该系统为您提供了以下几种保存应用数据的选项：

- **应用专属存储空间**：存储仅供应用使用的文件，可以存储到内部存储卷中的专属目录或外部存储空间中的其他专属目录。使用内部存储空间中的目录保存其他应用不应访问的敏感信息。
- **共享存储**：存储您的应用打算与其他应用共享的文件，包括媒体、文档和其他文件。
- **偏好设置**：以键值对形式存储私有原始数据。
- **数据库**：使用 Room 持久性库将结构化数据存储在专用数据库中。

下表汇总了这些选项的特点：

|                                                              | 内容类型                                 | 访问方法                                                     | 所需权限                                                     | 其他应用是否可以访问？                          | 卸载应用时是否移除文件？ |
| :----------------------------------------------------------- | :--------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------- | :----------------------- |
| [应用专属文件](https://developer.android.com/training/data-storage/app-specific) | 仅供您的应用使用的文件                   | 从内部存储空间访问，可以使用 `getFilesDir()` 或 `getCacheDir()` 方法  从外部存储空间访问，可以使用 `getExternalFilesDir()` 或 `getExternalCacheDir()` 方法 | 从内部存储空间访问不需要任何权限  如果应用在搭载 Android 4.4（API 级别 19）或更高版本的设备上运行，从外部存储空间访问不需要任何权限 | 否                                              | 是                       |
| [媒体](https://developer.android.com/training/data-storage/shared/media) | 可共享的媒体文件（图片、音频文件、视频） | `MediaStore` API                                             | 在 Android 11（API 级别 30）或更高版本中，访问其他应用的文件需要 `READ_EXTERNAL_STORAGE`  在 Android 10（API 级别 29）中，访问其他应用的文件需要 `READ_EXTERNAL_STORAGE` 或 `WRITE_EXTERNAL_STORAGE`  在 Android 9（API 级别 28）或更低版本中，访问**所有**文件均需要相关权限 | 是，但其他应用需要 `READ_EXTERNAL_STORAGE` 权限 | 否                       |
| [文档和其他文件](https://developer.android.com/training/data-storage/shared/documents-files) | 其他类型的可共享内容，包括已下载的文件   | 存储访问框架                                                 | 无                                                           | 是，可以通过系统文件选择器访问                  | 否                       |
| [应用偏好设置](https://developer.android.com/training/data-storage/shared-preferences) | 键值对                                   | [Jetpack Preferences](https://developer.android.com/guide/topics/ui/settings/use-saved-values) 库 | 无                                                           | 否                                              | 是                       |
| 数据库                                                       | 结构化数据                               | [Room](https://developer.android.com/training/data-storage/room) 持久性库 | 无                                                           | 否                                              | 是                       |

您应根据自己的具体需求选择解决方案：

- 您的数据需要占用多少空间？

  内部存储空间中用于存储应用专属数据的空间有限。如果您需要保存大量数据，请使用其他类型的存储空间。

- 数据访问需要达到怎样的可靠程度？

  如果应用的基本功能需要某些数据（例如应用启动时需要的数据），可以将相应数据存放到内部存储目录或数据库中。存储在外部存储空间中的应用专属文件并非一直可以访问，因为有些设备允许用户移除提供外部存储空间的实体设备。

- 您需要存储哪类数据？

  如果数据仅供您的应用使用，应使用应用专属存储空间。对于可分享的媒体内容，应使用共享的存储空间，以便其他应用可以访问相应内容。对于结构化数据，应使用偏好设置（适合键值对数据）或数据库（适合包含 2 个以上列的数据）。

- 数据是否应仅供您的应用使用？

  在存储敏感数据（不可通过任何其他应用访问的数据）时，应使用内部存储空间、偏好设置或数据库。内部存储空间的一个额外优势是用户无法看到相应数据。

## 存储位置的类别

Android 提供两类物理存储位置：内部存储空间和外部存储空间。在大多数设备上，内部存储空间小于外部存储空间。不过，所有设备上的内部存储空间都是始终可用的，因此在存储应用所依赖的数据时更为可靠。

可移除卷（例如 SD 卡）在文件系统中属于外部存储空间。Android 使用路径（例如 `/sdcard`）表示这些存储设备。

**注意**：可用于保存文件的确切位置可能因设备而异。因此，请勿使用硬编码的文件路径。

默认情况下，应用本身存储在内部存储空间中。不过，如果您的 APK 非常大，也可以在应用的清单文件中指明偏好设置，以便将应用安装到外部存储空间：

```xml
<manifest ...
  android:installLocation="preferExternal">
  ...
</manifest>
```

## 对外部存储空间的访问和所需权限

Android 定义了以下与存储相关的权限：[`READ_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#READ_EXTERNAL_STORAGE)、[`WRITE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE) 和 [`MANAGE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#MANAGE_EXTERNAL_STORAGE)。

在较低版本的 Android 系统中，应用需要声明 `READ_EXTERNAL_STORAGE` 权限才能访问位于外部存储空间中[应用专属目录](https://developer.android.com/training/data-storage/app-specific#external)之外的任何文件。此外，应用需要声明 `WRITE_EXTERNAL_STORAGE` 权限才能向应用专属目录以外的任何文件写入数据。

Android 系统的版本越新，就越依赖于文件的用途而不是位置来确定应用对特定文件的访问和写入能力。特别是，如果您的应用以 Android 11（API 级别 30）或更高版本为目标平台，`WRITE_EXTERNAL_STORAGE` 权限完全不会影响应用对存储的访问权限。这种基于用途的存储模型可增强用户隐私保护，因为应用只能访问其在设备文件系统中实际使用的区域。

Android 11 引入了 `MANAGE_EXTERNAL_STORAGE` 权限，该权限提供对应用专属目录和 `MediaStore` 之外文件的写入权限。如需详细了解此权限，以及为何大多数应用无需声明此权限即可实现其用例，请参阅有关如何[管理存储设备上所有文件](https://developer.android.com/training/data-storage/manage-all-files)的指南。

### 分区存储

为了让用户更好地管理自己的文件并减少混乱，以 Android 10（API 级别 29）及更高版本为目标平台的应用在默认情况下被授予了对外部存储空间的分区访问权限（即分区存储）。此类应用只能访问外部存储空间上的应用专属目录，以及本应用所创建的特定类型的媒体文件。

**注意**：如果您的应用在运行时请求与存储空间相关的权限，面向用户的对话框会表明您的应用正在请求对外部存储空间的广泛访问，即使已启用分区存储也是如此。

除非您的应用需要访问存储在[应用专属目录](https://developer.android.com/training/data-storage/app-specific)和 [`MediaStore`](https://developer.android.com/reference/android/provider/MediaStore) API 可以访问的目录之外的文件，否则请使用分区存储。如果您将应用专属文件存储在外部存储空间中，则可以将这些文件存放在[外部存储空间中的应用专属目录](https://developer.android.com/training/data-storage/app-specific#external)内，以便更加轻松地采用分区存储。这样，在启用分区存储后，您的应用将可以继续访问这些文件。

如需让您的应用适合分区存储，请参阅[存储用例和最佳实践](https://developer.android.com/training/data-storage/use-cases)指南。如果您的应用有其他用例未包含在分区存储范围内，请[提交功能请求](https://source.android.com/setup/contribute/report-bugs)。您可以[暂时选择停用分区存储](https://developer.android.com/training/data-storage/use-cases#opt-out-scoped-storage)。

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

共享参数的存储介质是符合XML规范的配置文件。保存路径是：`/data/data/应用包名/shared_prefs/文件名.xml`

## 使用ViewModel和SharedPreference存储数据

使用ViewModel和SharedPreference以键值对的形式存储数据

开始前要开启dataBinding并引入`lifecycle-extensions`库

1. 创建ViewModel，注意这里继承的是AndroidViewModel类

   ```kotlin
   package com.yorick.viewmodelshp
   
   import android.app.Application
   import android.content.Context
   import androidx.lifecycle.AndroidViewModel
   import androidx.lifecycle.LiveData
   import androidx.lifecycle.SavedStateHandle
   
   class MyViewModel(
       application: Application,
       private val handle: SavedStateHandle
   ) : AndroidViewModel(application) {
       private val key = application.resources.getString(R.string.data_key)
       private val shpName = application.resources.getString(R.string.shp_name)
       private val shp = application.getSharedPreferences(shpName, Context.MODE_PRIVATE)
   
       init {
           if (!handle.contains(key)) {
               load()
           }
       }
   
       fun getNumber(): LiveData<Int> {
           return handle.getLiveData<Int>(key)
       }
   
       private fun load() {
           handle[key] = shp.getInt(key, 0)
       }
   
       fun save() {
           with(shp.edit()) {
               getNumber().value?.let { putInt(key, it) }
               apply()
           }
       }
   
       fun add(x: Int) {
           handle[key] = getNumber().value?.plus(x)
           // save() // 每次改变都会保存，可靠但是资源消耗大
       }
   }
   ```

2. 布局文件，包括按钮和文本视图，反向数据绑定

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <layout xmlns:android="http://schemas.android.com/apk/res/android"
       xmlns:app="http://schemas.android.com/apk/res-auto"
       xmlns:tools="http://schemas.android.com/tools">
   
       <data>
   
           <variable
               name="data"
               type="com.yorick.viewmodelshp.MyViewModel" />
       </data>
   
       <androidx.constraintlayout.widget.ConstraintLayout
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           tools:context=".MainActivity">
   
           <TextView
               android:id="@+id/textView"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:text="@{data.number.toString()}"
               android:textSize="34sp"
               app:layout_constraintBottom_toBottomOf="parent"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintHorizontal_bias="0.498"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="parent"
               app:layout_constraintVertical_bias="0.364" />
   
           <Button
               android:id="@+id/button"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:onClick="@{()->data.add(1)}"
               android:text="@string/btn_plus"
               android:textSize="24sp"
               app:layout_constraintBottom_toBottomOf="@+id/button2"
               app:layout_constraintEnd_toStartOf="@+id/guideline3"
               app:layout_constraintHorizontal_bias="0.413"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="@+id/button2"
               app:layout_constraintVertical_bias="0.0" />
   
           <Button
               android:id="@+id/button2"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:onClick="@{()->data.add(-1)}"
               android:text="@string/btn_minus"
               android:textSize="24sp"
               app:layout_constraintBottom_toTopOf="@+id/guideline2"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintStart_toStartOf="@+id/guideline3"
               app:layout_constraintTop_toTopOf="@+id/guideline2" />
   
           <androidx.constraintlayout.widget.Guideline
               android:id="@+id/guideline2"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:orientation="horizontal"
               app:layout_constraintGuide_percent="0.65" />
   
           <androidx.constraintlayout.widget.Guideline
               android:id="@+id/guideline3"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:orientation="vertical"
               app:layout_constraintGuide_percent="0.5" />
   
       </androidx.constraintlayout.widget.ConstraintLayout>
   </layout>
   ```

3. Activity，常在`onPause`方法中保存数据，但是设备意外断电等情况可能导致数据丢失。

   ```kotlin
   package com.yorick.viewmodelshp
   
   import android.os.Bundle
   import androidx.appcompat.app.AppCompatActivity
   import androidx.databinding.DataBindingUtil
   import androidx.lifecycle.SavedStateViewModelFactory
   import androidx.lifecycle.ViewModelProvider
   import com.yorick.viewmodelshp.databinding.ActivityMainBinding
   
   class MainActivity : AppCompatActivity() {
       private lateinit var myViewModel: MyViewModel
       private lateinit var binding: ActivityMainBinding
       override fun onCreate(savedInstanceState: Bundle?) {
           super.onCreate(savedInstanceState)
           setContentView(R.layout.activity_main)
           binding = DataBindingUtil.setContentView(
               this,
               R.layout.activity_main
           )
           myViewModel = ViewModelProvider(
               this,
               SavedStateViewModelFactory(application, this)
           )[MyViewModel::class.java]
           binding.data = myViewModel
           binding.lifecycleOwner = this
       }
   
       // 常用来数据保存
       override fun onPause() {
           super.onPause()
           myViewModel.save()
       }
   }
   ```

