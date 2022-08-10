# 数据库SQLite

- [数据库SQLite](#数据库sqlite)
  - [SQL的基本语法](#sql的基本语法)
    - [数据库定义语言](#数据库定义语言)
    - [数据操纵语言](#数据操纵语言)
  - [数据库管理器SQLiteDatabase](#数据库管理器sqlitedatabase)
  - [数据库帮助器SQLiteOpenHelper](#数据库帮助器sqliteopenhelper)
  - [优化记住密码功能](#优化记住密码功能)

## SQL的基本语法

### 数据库定义语言

SQLite语法与其他数据库的SQL语法有所出入，相关的注意点说明见下：

（1）SQL语句不区分大小写，无论是create与table这类关键词，还是表格名称、字段名称，都不区分大小写。唯一区分大小写的是被单引号括起来的字符串值。

（2）为避免重复建表，应加上IF NOT EXISTS关键词，例如`CREATE TABLE IF NOT EXISTS 表格名称.....`

（3）SQLite支持整型NTEGER、长整型LONG、字符串VARCHAR、浮点数FLOAT，但不支持布尔类型。布尔类型的数据要使用整型保存，如果直接保存布尔数据，在入库时SQLite会自动将它转为0或1，其中0表示false，1表示true。

（4）建表时需要唯一标识字段，它的字段名为id。创建新表都要加上该字段定义，例如入`id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL`

**删除表格**

表格的删除动作由drop命令完成，格式为`DROP TABLE IF EXISTS 表格名称;`。下面是删除用户信息表的SQL语句例子:

`DROP TABLE TF EXISTS user_info;`

**修改表结构**

表格的修改动作由alter命令完成，格式为ALTER TABLE 表格名称 修改操作。不过sQLite只支持增加字段，不支持修改字段，也不支持删除字段。对于字段增加操作，需要在alter之后补充add命令，具体格式如`ALTER TABLE 表格名称 ADD COLUMN 字段名称 字段类型;`。下面是给用户信息表增加手机号字段的SQL语句例子:

`ALTER TABLE user_info ADD COLUMN phone VARCHAR;`

注意，SQLite的ALTER语句每次只能添加一列字段，若要添加多列，就得分多次添加。

### 数据操纵语言

数据操纵语言全称Data Manipulation Language，简称DML，它描述了怎样处理数据实体的内部记录。表格记录的操作类型包括添加.删除、修改、查询4类，分别说明如下:

（1）添加记录

记录的添加动作由insert命令完成，格式为"INSERT INTO 表格名称(以逗号分隔的字段名列表) VALUES (以逗号分隔的字段值列表);"。下面是往用户信息表插入一条记录的SQL语句例子:
```sql
INSERT INTO user_info (name,age,height,weight,married,update_time) VALUES ('张三',20,170,50,0,'20200504');
```
（2）删除记录

记录的删除动作由delete命令完成，格式为"DELETE FROM 表格名称 WHERE 查询条件;"，其中查询条件的表达式形如"字段名=字段值"，多个字段的条件交集通过"AND"连接，条件并集通过"OR"连接。下面是从用户信息表删除指定记录的SQL语句例子:
```sql
DELETE FROM user_info WHERE name='张三';
```
（3）修改记录

记录的修改动作由update命令完成，格式为"UPDATE 表格名称 SET字段名=字段值 WHERE 查询条件;"。下面是对用户信息表更新指定记录的SQL语句例子:
```sql
UPDATE user_info SET married=1 wHERE name='张三';
```
（4）查询记录

记录的查询动作由select命令完成，格式为"SELECT 以逗号分隔的字段名列表 FROM 表格名称 WHERE查 询条件;"。如果字段名列表填星号“*”，则表示查询该表的所有字段。下面是从用户信息表查询指定记录的SQL语句例子:
```sql
SELECT name FROM user_info wHERE name='张三';
```

查询操作除了比较字段值条件之外，常常需要对查询结果排序，此时要在查询条件后面添加排序条件，对应的表达式为"ORDER BY 字段名 ASC 或者 DESC"，意指对查询结果按照某个字段排序，其中ASC代表升序，DESC代表降序。下面是查询记录并对结果排序的5QL语句例子:

```sql
SELECT *FROM user_info ORDER BY age ASC;
```

## 数据库管理器SQLiteDatabase

SQLiteDatabase是SQLite的数据库管理类，它提供了若干操作数据表的API，常用的方法有3类：

（1）管理类，用于数据库层面的操作。

- openDatabase：打开指定路径的数据库。
- isOpen：判断数据库是否已打开。
- close：关闭数据库。
- getVersion：获取数据库的版本号。
- setVersion：设置数据库的版本号。

（2）事务类，用于事务层面的操作。

- beginTransaction：开始事务。
- setTransactionSuccessful：设置事务的成功标志。
- endTransaction：结束事务。

## 数据库帮助器SQLiteOpenHelper

示例：

```java
public class UserDBHelper extends SQLiteOpenHelper {

    private static final String DB_NAME = "user.db";
    private static final String TABLE_NAME = "user_info";
    private static final int DB_VERSION = 1;
    private static UserDBHelper mHelper = null;
    private SQLiteDatabase mRDB = null;
    private SQLiteDatabase mWDB = null;

    private UserDBHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    // 使用单例模式获取唯一实例
    public static UserDBHelper getInstance(Context context) {
        if (mHelper == null) {
            mHelper = new UserDBHelper(context);
        }
        return mHelper;
    }

    // 打开数据库的读连接
    public SQLiteDatabase openReadLink() {
        if (mRDB == null || !mRDB.isOpen()) {
            mRDB = mHelper.getReadableDatabase();
        }
        return mRDB;
    }

    // 打开数据库的写连接
    public SQLiteDatabase openWriteLink() {
        if (mWDB == null || !mWDB.isOpen()) {
            mWDB = mHelper.getReadableDatabase();
        }
        return mWDB;
    }

    // 关闭数据库连接
    public void closeLink() {
        if (mRDB != null && mRDB.isOpen()) {
            mRDB.close();
            mRDB = null;
        }

        if (mWDB != null && mWDB.isOpen()) {
            mWDB.close();
            mWDB = null;
        }
    }

    // 创建数据库，执行建表语句
    @Override
    public void onCreate(SQLiteDatabase db) {
        String sql = "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " (\n" +
                "  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n" +
                "  NAME VARCHAR NOT NULL,\n" +
                "  gender INTEGER NOT NULL,\n" +
                "  age INTEGER NOT NULL,\n" +
                "  height LONG NOT NULL,\n" +
                "  weight FLOAT NOT NULL,\n" +
                "  update_time VARCHAR NOT NULL);";
        db.execSQL(sql);
    }

    // 更新数据库
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }

    public long insert(User user) {
        ContentValues values = new ContentValues();
        values.put("name", user.name);
        values.put("age", user.age);
        values.put("gender", user.gender);
        values.put("weight", user.weight);
        values.put("height", user.height);
        values.put("update_time", DateUtil.getCurrentTime());
        return mWDB.insert(TABLE_NAME, null, values);

        // 事务示例，同生共死
//        try {
//            mWDB.beginTransaction();
//            mWDB.insert(TABLE_NAME, null, values);
//            int i = 10/0
//            mWDB.insert(TABLE_NAME, null, values);
//            mWDB.setTransactionSuccessful();
//        } catch (Exception e) {
//            e.printStackTrace();
//        } finally {
//            mWDB.endTransaction();
//        }
    }

    public long deleteByName(String name) {
        // 删除所有
        // mWDB.delete(TABLE_NAME, "1=1", null);
        return mWDB.delete(TABLE_NAME, "name=?", new String[]{name});
    }

    public long update(User user) {
        ContentValues values = new ContentValues();
        values.put("name", user.name);
        values.put("age", user.age);
        values.put("gender", user.gender);
        values.put("weight", user.weight);
        values.put("height", user.height);
        values.put("update_time", DateUtil.getCurrentTime());
        return mWDB.update(TABLE_NAME, values, "name=?", new String[]{user.name});
    }

    public List<User> queryAll() {
        List<User> users = new ArrayList<>();
        Cursor cursor = mRDB.query(TABLE_NAME, null, null, null, null, null, null);
        while (cursor.moveToNext()) {
            User user = new User();
            user.id = cursor.getInt(0);
            user.name = cursor.getString(1);
            user.gender = cursor.getInt(2);
            user.age = cursor.getInt(3);
            user.height = cursor.getLong(4);
            user.weight = cursor.getFloat(5);
            users.add(user);
        }
        return users;
    }

    public List<User> queryByName(String name) {
        List<User> users = new ArrayList<>();
        Cursor cursor = mRDB.query(TABLE_NAME, null, "name=?", new String[]{name}, null, null, null);
        while (cursor.moveToNext()) {
            User user = new User();
            user.id = cursor.getInt(0);
            user.name = cursor.getString(1);
            user.gender = cursor.getInt(2);
            user.age = cursor.getInt(3);
            user.height = cursor.getLong(4);
            user.weight = cursor.getFloat(5);
            users.add(user);
        }
        return users;
    }
}
```

## 优化记住密码功能


