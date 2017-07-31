import MySQLdb
import time
from infos import *

class loadaverage(object):
    def sql_loadaverage(self):
        conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
        cur = conn.cursor()

        create_loadaveage_table = 'create table if not exists t_loadaveage (laid int PRIMARY KEY AUTO_INCREMENT,serverid int,la1 float(5,2),la5 float(5,2),la15 float(5,2),curr datetime, foreign key(serverid) references t_systeminfo(serverid))'
        try:
            cur.execute(create_loadaveage_table)
        except Exception as e:
            print 'Create Table t_loadaveage Success!'

        while True:
            try:
                la = dynamicinfo().getloadaveage()
                insert_loadaveage_table = 'insert into t_loadaveage(serverid,la1,la5,la15,curr) values (1,"%s","%s","%s",now())' % (la)
                select_loadaveage_table = 'select loadaveage.* from (select laid,serverid,la1,la5,la15,curr from t_loadaveage where serverid = 1 order by laid  desc limit 50) loadaveage order by laid'
                cur.execute(insert_loadaveage_table)
                conn.commit()
                cur.execute(select_loadaveage_table)
                data_loadaveage = cur.fetchall()
                # for row in data_loadaveage:
                #     print row
                self.laid = []
                self.la1 = []
                self.la5 = []
                self.la15 = []
                for i in data_loadaveage:
                    self.laid.append(i[0])
                    self.la1.append(i[2])
                    self.la5.append(i[3])
                    self.la15.append(i[4])
                return self.laid
                return self.la1
                return self.la5
                return self.la15
                time.sleep(5)
            except Exception as e:
                print e
                conn.rollback()
        conn.close()
    def create_image(self):
        pass


