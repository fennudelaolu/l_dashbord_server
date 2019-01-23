from src.util import mysqlPool, mUtil
import time, random, json

# 创建表文件夹
def createFolder(email, folder_name):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:
        r = cursor.execute("insert into screen (user, name, type) values (%s, %s, %s)",
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

# 创建大屏幕
def createScreen(email, folder_name, screen_name, option,img, note ):
    option = json.dumps(option)

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        sql = "insert into screen (user, pname, name, type, screen_option, img, note,isfree) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        r = cursor.execute(sql,[email, folder_name, screen_name, 'screen',option, img, note,0])
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

        r = cursor.execute("delete from screen where user=%s and (pname=%s or (name=%s and type='folder'))"
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

# 删除大屏幕
def delScreen(email, folder_name, screens):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        r = cursor.execute("delete from screen where user=%s and pname=%s and name in %s"
                           , [email, folder_name, screens])

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
def findTree(email):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        cursor.execute("SELECT * FROM screen WHERE user=%s ORDER BY FIELD(`type`, 'folder', 'screen')"
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

# 某用户是否拥有指定文件夹
def findFolderCountByUser(email, folder_name):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:

        # 查询是否有同名文件夹
        cursor.execute("select count(*) as count from screen where user=%s and name=%s",
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



if __name__ == '__main__':
    input_data('a', 'test', '新建 XLS 工作表.xls_Sheet1', [{'ff': 'a', 'b': 'b'}, {'ff': 'a2', 'b': 'b2'}])


