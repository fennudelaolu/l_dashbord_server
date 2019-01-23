import pymysql.cursors

config = {
    'host':'192.168.110.129',
    'port': 3306,
    'user': 'admin',
    'password': '123456',
    'database': 'test',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接数据库
conn = pymysql.connect(**config)

conn.autocommit(1)
# 获取游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)



#-------------------------------表操作-----------------------------------#

column_type = {'s':'varchar(255)','n': 'float', 'd': 'Date', '':'varchar(255)'}
#@param String TABLE_NAME, not null
#@param dict columns, not null , example:{"name":'s','age': 'n', 'tel':''}
#result Boolean
def createTable(table_name, columns):
    sql = ''
    for column in columns:

        a = column_type.setdefault(columns[column],'varchar(255)')
        sql += column + ' ' + a + ','
    sql = sql[0:-1]
    print(sql)


    try:
        TABLE_NAME = table_name

        r = cursor.execute('CREATE TABLE %s(%s)' % (TABLE_NAME,sql))
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()

def delTable(table_name):

    try:
        TABLE_NAME = table_name
        r = cursor.execute('drop table %s' %TABLE_NAME)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()

#-----------------------------表中数据操作-------------------------------------

def insert(table_name, data):
    sql = 'select * from user'
    try:
        cursor.execute(sql)
        r = cursor.fetchall()
        return r
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()

def findAll(table_name, filtter, user):
    sql = 'select * from user'
    try:
     cursor.execute(sql)
     r =cursor.fetchall()
     return r
    except Exception as e:
     import traceback
     traceback.print_exc()

     conn.rollback()  # 事务回滚
     print('事务处理失败', e)
    finally:
     cursor.close()
     conn.close()


if __name__ == '__main__':

    TABLE_NAME = 'test'

    createTable(TABLE_NAME,{"name":'s','age': 'n'})
    #delTable(TABLE_NAME)