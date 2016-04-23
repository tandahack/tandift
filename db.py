import sqlite3
import os.path
import sys
import logging
import traceback

class Application:
    def __init__(self):

        self.conn = sqlite3.connect('tandift.db')
        self.c = self.conn.cursor()

        self.execSQL("ATTACH DATABASE 'MarkTime.db' as upload;")
        self.execSQL("BEGIN;")
        for table in self.getTables():

            cols = self.getColumns(table)
            if len(cols)>1:
                k = cols[1]
                self.mergeTables(table, "upload."+table, key=k)

        deletes = []
        for row in self.c.execute("SELECT * FROM changelog"):
            print(row)
            if row[3] == "DEL":
                    deletes.append("DELETE FROM '"+row[1]+"' WHERE _id="+row[2])
        for sql in deletes:
            self.c.execute(sql)
            logger.info(sql)
            print(sql)
        self.c.execute("DELETE FROM changelog")


        self.execSQL("END;")
        self.execSQL("DETACH upload;" )
        self.conn.commit()
        self.conn.close()

        os.remove("MarkTime.db")
        self.updateStatus("finished")


    def addUser(self, user, pass, salt):
        cols = self.getColumns(tableA)
        del cols[0]
        if key == "":
            key = cols[0]
        print(cols*2)
        print(key)
        sql = "INSERT INTO "+tableA+" ("+",".join(cols)+") SELECT "+",".join(cols)+" FROM "+tableB+" WHERE "+key+" NOT IN (SELECT "+key+" FROM "+tableA+")"
        self.execSQL(sql)
        self.conn.commit()

    def mergeTables(self, tableA, tableB, key="", keys=[]):
        print("Merging tables.")
        cols = self.getColumns(tableA)
        del cols[0]
        if key == "":
            key = cols[0]

        sql = "INSERT INTO "+tableA+" ("+",".join(cols)+") SELECT "+",".join(cols)+" FROM "+tableB+" WHERE "+key+" NOT IN (SELECT "+key+" FROM "+tableA+")"
        self.execSQL(sql)
        self.conn.commit()

    def copyTable(self, tableName, newTableName):
        c = self.c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName))
        c = self.c.execute(c.fetchone()[0].replace(tableName, newTableName, 1))
        self.execSQL("INSERT INTO {} SELECT * FROM {};".format(newTableName, tableName))
        self.conn.commit()
        #self.c.execute()

    def renameTable(self, oldName, newName):
        self.copyTable(oldName, newName)
        self.execSQL("DROP TABLE {}".format(oldName))

    def getColumns(self, table):
        t = []
        for row in self.c.execute("PRAGMA table_info("+table+");"):
            t.append(row[1])
        return t

    def getTables(self):
        t = []
        for row in self.c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            t.append(row[0])
        return t

    def execSQL(self, sql):
        try:
            for row in self.c.execute(sql):
                print row
        except sqlite3.OperationalError  as e:
            print(e)

    def setFlag(self, flag):
        pass

def my_handler(exctype, value, tb):
    logger.exception("""
    Type: {}
    Value: {}
    Traceback: {}
    """.format(exctype, value, traceback.extract_tb(tb)))
    self.updateStatus("error")

if __name__ == "__main__":
    logging.basicConfig(filename='python.log',level=logging.DEBUG)
    logger = logging.getLogger('mylogger')
    sys.excepthook = my_handler

    app = Application()