# 使用MySQL

# 导入MySQL驱动:
import mysql.connector
# 注意把password设为你的root口令:
conn = mysql.connector.connect(user='root', password='964538',auth_plugin='mysql_native_password',database='testing')
# cursor = conn.cursor()

# # 创建user表:
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# # 插入一行记录，注意MySQL的占位符是%s:
# cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Yorick'])
# print(cursor.rowcount)
# # 提交事务:
# conn.commit()
# cursor.close()

# 运行查询
cursor = conn.cursor()
cursor.execute('select * from user where id = %s',('1',))
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()

# 由于Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似。

# 执行INSERT等操作后要调用commit()提交事务；

# MySQL的SQL占位符是%s。

