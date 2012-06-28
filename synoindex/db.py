import os
import sqlite3
import threading


VERSION=001
FIRSTRUN=1

db_lock = threading.Lock()


def checkDB():
    if FIRSTRUN==1:
        conn = sqlite3.connect('SynoDLNAtrakt.db')
        curs = conn.cursor()
        curs.execute("""CREATE TABLE watch (id INTEGER PRIMARY KEY,
            folder TEXT, 
            abitrate NUMERIC, 
            vbitrate NUMERIC, 
            acodec TEXT, 
            vcodec TEXT, 
            achannels NUMERIC, 
            width NUMERIC, 
            height NUMERIC,
            allaudio NUMERIC,
            germanfirst NUMERIC,
            subtitles NUMERIC,
            moveit NUMERIC,
            moveto NUMERIC,
            deleteit NUMERIC,
            addmeta NUMERIC
            appletv NUMERIC, appletvaddon NUMERIC)""")
        curs.execute("""CREATE TABLE files (id INTEGER PRIMARY KEY, 
            folder TEXT, 
            filename TEXT, 
            title TEXT,
            acodec TEXT,
            vcodec TEXT,
            abitrate NUMERIC,
            vbitrate NUMERIC,
            achannels NUMERIC,
            atracks NUMERIC,
            subtitles NUMERIC,
            series NUMERIC)""")
        curs.execute("""CREATE TABLE metadata (id INTEGER PRIMARY KEY, 
            fileid NUMERIC,
            folder TEXT, 
            filename TEXT, 
            title TEXT,
            season NUMERIC,
            episode NUMERIC,
            plot NUMERIC,
            year NUMERIC)""")
        curs.execute("""CREATE TABLE pyencoder (version NUMERIC)""")
        curs.execute("INSERT INTO pyencoder (version) VALUES (1)")
        conn.commit()

# http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# myDB = db.DBConnection()
# myDB.action("INSERT INTO history (action, date, showid, season, episode, quality, resource, provider) VALUES (?,?,?,?,?,?,?,?)",
#                 [action, logDate, showid, season, episode, quality, resource, provider])
class DBConnection:
    def __init__(self, filename="SynoDLNAtrakt.db", suffix=None, row_type="dict"):

        self.filename = filename
        self.connection = sqlite3.connect(filename)
        if row_type == "dict":
            self.connection.row_factory = self._dict_factory
        else:
            self.connection.row_factory = sqlite3.Row

    def action(self, query, args=None):
        with db_lock:
    
            if query == None:
                return
    
            sqlResult = None
            attempt = 0
    
            while attempt < 5:
                try:
                    if args == None:
                        #logger.log(self.filename+": "+query, logger.DEBUG)
                        print query
                        sqlResult = self.connection.execute(query)
                    else:
                        #logger.log(self.filename+": "+query+" with args "+str(args), logger.DEBUG)
                        print query, args
                        sqlResult = self.connection.execute(query, args)
                    self.connection.commit()
                    # get out of the connection attempt loop since we were successful
                    break
                except sqlite3.OperationalError, e:
                    if "unable to open database file" in e.message or "database is locked" in e.message:
                        #logger.log(u"DB error: "+ex(e), logger.WARNING)
                        print "error(e)"
                        attempt += 1
                        time.sleep(1)
                    else:
                        #logger.log(u"DB error: "+ex(e), logger.ERROR)
                        print "error(e)"
                        raise
                except sqlite3.DatabaseError, e:
                    #logger.log(u"Fatal error executing query: " + ex(e), logger.ERROR)
                    print "error(e)"
                    raise
    
            return sqlResult
    
    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    
    def select(self, query, args=None):
        sqlResults = self.action(query, args).fetchall()
        if sqlResults == None:
            return []
        return sqlResults


    #update oder insert in tabel
    #myDB.upsert("watch",{'abitrate': '44800','acodec':'ac3'},{'id': '2'})

    def upsert(self, tableName, valueDict, keyDict):

        changesBefore = self.connection.total_changes

        genParams = lambda myDict : [x + " = ?" for x in myDict.keys()]

        query = "UPDATE "+tableName+" SET " + ", ".join(genParams(valueDict)) + " WHERE " + " AND ".join(genParams(keyDict))

        self.action(query, valueDict.values() + keyDict.values())

        if self.connection.total_changes == changesBefore:
            query = "INSERT INTO "+tableName+" (" + ", ".join(valueDict.keys() + keyDict.keys()) + ")" + \
                     " VALUES (" + ", ".join(["?"] * len(valueDict.keys() + keyDict.keys())) + ")"
            self.action(query, valueDict.values() + keyDict.values())
