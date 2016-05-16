#coding=utf-8
import mysql.connector
#import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoushiPipeline(object):

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(user='root', password='lacom159753', database='smarthome', use_unicode=True)
            self.cursor = self.conn.cursor()
            self.cursor.execute("truncate table menu;")
            self.conn.commit()
        except mysql.connector.Error as e:
            print('query error!{}'.format(e))
        finally:
            self.close_db()

    #savePro方法     将数据存入数据库中。注意：目前使用此方法将节目单存入数据库。
    def savePro(self, menus):
        try:
            self.conn = mysql.connector.connect(user='root', password='lacom159753', database='smarthome', use_unicode=True)
            self.cursor = self.conn.cursor()
            for p in menus:
                self.cursor.execute('insert into menu(time, name ,nexttime, cid, channel) values (%s, %s, %s, %s, %s);', [p.time, p.name, p.end, p.cid, p.channel])
                self.conn.commit()
        except mysql.connector.Error as e:
            print('save error!{}'.format(e))
        finally:
            self.close_db()
    #关闭数据库相关资源
    def close_db(self):
        self.cursor.close()
        self.conn.close()
