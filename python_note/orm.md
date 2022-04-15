# 编写ORM框架

ORM全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表，这样，写代码更简单，不用直接操作SQL语句。

要编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来。

首先来定义Field类，它负责保存数据库表的字段名和字段类型：
```py
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    # __str__方法，重写print()函数返回值
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
```
在Field的基础上，进一步定义各种类型的Field，比如StringField，IntegerField等等：
```py
class StringField(Field):

    def __init__(self, name):
        # 用super()调用父类方法
        super().__init__(name, 'varchar(100)')

class IntegerField(Field):

    def __init__(self, name):
        super().__init__(name, 'bigint')
```
下一步，就是编写最复杂的ModelMetaclass了：
```py
class 