from src.util import mysqlPool, mUtil
import time, random, json

# 创建表文件夹
def createFolder(email, folder_name):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:
        r = cursor.execute("insert into table_schema (user, name, type) values (%s, %s, %s)",
                           [email, folder_name, 'folder' ])
        return r

    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
        result = {'code': -1, 'msg': e}
    finally:
        cursor.close()
        conn.close()

    return -1

# 创建表
# Todo 添加表头信息
#@param dict columns, not null , example:{"name":'s','age': 'n', 'tel':''}
column_type = {'s':'varchar(255)','n': 'float', 'd': 'Date', '':'varchar(255)'}
def createTable(email, folder_name, table_name, columns, note, head):

    real_name = email + '_' +  mUtil.getUUid() # 实际创建的表名

    sql = '' # 循环拼接要插入的字段，生成sql
    for column in columns:
        a = column_type.setdefault(columns[column], 'varchar(255)')
        sql += column + ' ' + a + ','
    sql = sql[0:-1]

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        # 创建表
        TABLE_NAME = email + '_' + table_name
        r = cursor.execute('CREATE TABLE %s(%s)' % (real_name, sql))

        # 插入一条新目录
        r = cursor.execute("insert into table_schema (user, name, real_name, type, pname, note, head) values (%s, %s, %s, %s, %s, %s, %s)",
                           [email, table_name, real_name, 'table', folder_name, note, head])

        conn.commit()
        return r

    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
        result = {'code': -1, 'msg': e}
    finally:
        cursor.close()
        conn.close()

    return -1

# 删除文件夹及文件夹下所有表格
def delFolder(email, folder_name):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:
        # no.2 删除目录
        r = cursor.execute("delete from table_schema where user=%s and (pname=%s or (name=%s and type='folder'))"
                           , [email, folder_name, folder_name])
        conn.commit()
        return r
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚

        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()
    return -1

# 删除表格
def delTables(email, folder_name, table_names):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        r = cursor.execute("delete from table_schema where user=%s and pname=%s and name in %s"
                           , [email, folder_name, table_names])

        conn.commit()
        return r
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚

        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()
    return -1

# 查询某用户拥有的目录
# Todo 获取表头信息
def findTree(email):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        cursor.execute("SELECT * FROM table_schema WHERE user=%s ORDER BY type ASC"
                           , [email])
        r = cursor.fetchall();

        tree = {}
        for item in r :
            if item['type'] == 'folder':
                tree[item['name']] = {'name': item['name'], 'child':[]}
            else :
                parent = tree[item['pname']]
                parent['child'].append(item)

        return tree
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚

        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()
    return -1

# 导入数据

def input_data(email, folder, table_name, up_data):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:


        # no.1 查询插入表的表名
        cursor.execute("select real_name from table_schema where user=%s and pname=%s and name=%s and type='table' limit 1"
                           , [email, folder, table_name])
        r = cursor.fetchone();
        sql = "insert into "+ str(r['real_name']) +"  values %s"

        # no.2 循环插入
        for row in up_data:
            columns = []
            values = []
            for c in row:
                columns.append(c)
                v = row[c]
                values.append(v)

            cursor.execute(sql, [ values])

        conn.commit()

        return 0
    except Exception as e:
        import traceback
        traceback.print_exc()

        conn.rollback()  # 事务回滚

        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()
    return -1

# 某用户是否拥有指定文件夹
def findFolderCountByUser(email, folder_name):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        # 查询是否有同名文件夹
        cursor.execute("select count(*) as count from table_schema where user=%s and name=%s",
                       [email, folder_name])
        r = cursor.fetchone()

        folder_count = r['count']
        return folder_count

    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
        result = {'code': -1, 'msg': e}
    finally:
        cursor.close()
        conn.close()

    return -1

# 查询表中数据
def getTable(real_name, start, end):


    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:
        sql = 'select * from ' + real_name + ' limit %s OFFSET  %s'

        # 查询是否有同名文件夹
        cursor.execute(sql, [end,start ])
        data = cursor.fetchall()

        cursor.execute("select head from table_schema where real_name=%s and type='table'", [real_name])
        head = cursor.fetchone()

        return {'data':data, 'head': json.loads(head['head'])}

    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
        result = {'code': -1, 'msg': e}
    finally:
        cursor.close()
        conn.close()

    return -1


if __name__ == '__main__':
    input_data('a', 'test', '新建 XLS 工作表.xls_Sheet1', [{'ff': 'a', 'b': 'b'}, {'ff': 'a2', 'b': 'b2'}])


