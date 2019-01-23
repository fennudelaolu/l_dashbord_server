import pymysql
from DBUtils.PooledDB import PooledDB

cur = pymysql.cursors.DictCursor

pool = PooledDB(pymysql,
                5,                      #最少连接数
                host='rm-uf6w69tb8fhnca0311o.mysql.rds.aliyuncs.com',
                user='user1',
                passwd='LuLu1234',
                db='lu_dashboard',
                port=3306,
                setsession=['SET AUTOCOMMIT = 1'] #setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
                )

def getConn():
    conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    return conn



#*---------------------公用方法------------------------*#
data_type = {}
def insert_or_update(table_name, val_map):

    conn = getConn()
    cursor = conn.cursor(cursor=cur)

    columns = ''
    values = ''
    for c in val_map:
        columns += str(c) + ','
        v = val_map[c]['val']
        t = val_map[c]['type']
        if(t == 's'):
            values += '\"' +str(v) + '\",'
        else:
            values += str(v) + ','

    columns = columns[0:-1]
    values = values[0:-1]

    try:
        sql = ('REPLACE into %s (%s) values (%s)' % (table_name, columns, values))
        r = cursor.execute(sql)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()



# cur=conn.cursor()
#
# SQL="select * from table"
#
# count=cur.execute(SQL)
#
# results=cur.fetchall()
#
# cur.close()
#
# conn.close()
