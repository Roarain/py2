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
                self.curr = []
                for i in data_loadaveage:
                    self.laid.append(i[0])
                    self.la1.append(i[2])
                    self.la5.append(i[3])
                    self.la15.append(i[4])
                return self.laid
                return self.la1
                return self.la5
                return self.la15
                return self.curr
                time.sleep(5)
            except Exception as e:
                print e
                conn.rollback()
        conn.close()
    def create_image(self):
        from pychartdir import *

        # The data for the line chart
        data0 = self.la1
        data1 = self.la5
        data2 = self.la15
        start_time = list(self.curr[0])
        # The labels for the line chart
        # labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
        #     "16", "17", "18", "19", "20", "21", "22", "23", "24"]
        # labels = ["2017-5-7 0:33:50","2017-5-7 0:33:55","2017-5-7 0:34","2017-5-7 0:34:5","2017-5-7 0:34:10","2017-5-7 0:34:15","2017-5-7 0:34:20","2017-5-7 0:34:25","2017-5-7 0:34:30","2017-5-7 0:34:35","2017-5-7 0:34:40","2017-5-7 0:34:45","2017-5-7 0:34:50","2017-5-7 0:34:55","2017-5-7 0:35","2017-5-7 0:35:5","2017-5-7 0:35:10","2017-5-7 0:35:15","2017-5-7 0:35:20","2017-5-7 0:35:25","2017-5-7 0:35:30","2017-5-7 0:35:35","2017-5-7 0:35:40","2017-5-7 0:35:45","2017-5-7 0:35:50","2017-5-7 0:35:56","2017-5-7 0:36:1","2017-5-7 0:36:6","2017-5-7 0:36:11","2017-5-7 0:36:16","2017-5-7 0:36:21","2017-5-7 0:36:26","2017-5-7 0:36:31","2017-5-7 0:36:36","2017-5-7 0:36:41","2017-5-7 0:36:46","2017-5-7 0:36:51","2017-5-7 0:36:56","2017-5-7 0:37:1","2017-5-7 0:37:6","2017-5-7 0:37:11","2017-5-7 0:37:16","2017-5-7 0:37:21","2017-5-7 0:37:26","2017-5-7 0:37:31","2017-5-7 0:37:36","2017-5-7 0:37:41","2017-5-7 0:37:46","2017-5-7 0:37:51","2017-5-7 0:37:54"]
        # labels = ["2017-5-7 0:33:50",'','',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"2017-5-7 0:37:54"]
        labels = start_time
        # Create an XYChart object of size 600 x 300 pixels, with a light blue (EEEEFF) background, black
        # border, 1 pxiel 3D border effect and rounded corners
        c = XYChart(600, 300, 0xeeeeff, 0x000000, 1)
        c.setRoundedFrame()

        # Set the plotarea at (55, 58) and of size 520 x 195 pixels, with white background. Turn on both
        # horizontal and vertical grid lines with light grey color (0xcccccc)
        c.setPlotArea(55, 58, 520, 195, 0xffffff, -1, -1, 0xcccccc, 0xcccccc)

        # Add a legend box at (50, 30) (top of the chart) with horizontal layout. Use 9pt Arial Bold font.
        # Set the background and border color to Transparent.
        c.addLegend(50, 30, 0, "arialbd.ttf", 9).setBackground(Transparent)

        # Add a title box to the chart using 15pt Times Bold Italic font, on a light blue (CCCCFF)
        # background with glass effect. white (0xffffff) on a dark red (0x800000) background, with a 1 pixel
        # 3D border.
        c.addTitle("Application Server Throughput", "timesbi.ttf", 15).setBackground(0xccccff, 0x000000,
                                                                                     glassEffect())

        # Add a title to the y axis
        c.yAxis().setTitle("MBytes per hour")

        # Set the labels on the x axis.
        c.xAxis().setLabels(labels)

        # Display 1 out of 3 labels on the x-axis.
        c.xAxis().setLabelStep(3)

        # Add a title to the x axis
        c.xAxis().setTitle("Load Average")

        # Add a line layer to the chart
        layer = c.addLineLayer2()

        # Set the default line width to 2 pixels
        layer.setLineWidth(2)

        # Add the three data sets to the line layer. For demo purpose, we use a dash line color for the last
        # line
        layer.addDataSet(data0, 0xff0000, "loadaverage 1 minute")
        layer.addDataSet(data1, 0x008800, "loadaverage 5 minute")
        layer.addDataSet(data2, c.dashLineColor(0x3333ff, DashLine), "loadaverage 15 minute")

        # Output the chart
        c.makeChart("testimage.png")


