class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, "varchar(100)")


class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, "bigint")


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 排除掉对Model类的修改，只修改其子类
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        # 查找Field属性
        for k,v in attrs.items():
            if isinstance(v,Field):
                print("Found mapping: %s ==> %s" % (k,v))
                mappings[k] = v
        # 从类属性中删除该Field属性
        for k in mappings.keys():
            attrs.pop(k)
        # 为Model的子类添加新属性
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)
        
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    # 把一个类的所有属性和方法调用全部动态化处理
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 生成实例化对象时调用
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name) # 等同于fields.append(k)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建一个实例：
u = User(id=12345, name='Yorick', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()