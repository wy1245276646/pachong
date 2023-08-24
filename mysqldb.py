import pymysql
from pymysql import IntegrityError


class MysqlDB:
    def __init__(self):
        #连接数据库
        self.mydb = pymysql.connect(host='127.0.0.1', user='root', password='12345678', port=3306,charset='utf8')
        #游标
        self.cursor = self.mydb.cursor()
        #数据库名称
        self.dbname='qqmusicdb'
        #表名
        self.tbname='t1'
        #创建数据库
        self.create_database()
        #创建数据表
        self.create_table()
    #创建数据库
    def create_database(self):
        try:
            self.cursor.execute(f'create database {self.dbname}')
        except Exception as e:
            print('mysql数据库taobao存在')
            # print(e.__traceback__.tb_lineno,e)
        finally:
            self.cursor.execute(f'USE {self.dbname}')

    # 创建数据表
    def create_table(self):
        qqmusic_table = f'''create table {self.tbname} (
                            id int unsigned auto_increment primary key,
                            qname varchar(20) not null,
                            qdate varchar(20) not null,
                            qplace varchar(20) not null,
                            qcontent varchar(500) not null)'''
        try:
            self.cursor.execute(qqmusic_table)
        except Exception as e:
            print("数据表已存在")
            #print(e.__traceback__.tb_lineno,e)
    #插入数据库
    def insertitem(self, item):
        sql = f'insert into {self.tbname} values (null,"%s","%s","%s","%s")' % tuple(item)
        #print('sql=',sql)
        try:

            self.cursor.execute(sql)
            self.mydb.commit()
            print('mysql插入成功')
            return item
        except IntegrityError as e:
            self.mydb.rollback()
    #查找所有数据
    def selectdball(self):
        try:
            sql=f'select * from {self.tbname}'
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            pass
    #关闭数据库
    def closedb(self):
        self.mydb.close()

if __name__ == '__main__':
    mysqldb = MysqlDB()
    print(mysqldb.selectdball())
