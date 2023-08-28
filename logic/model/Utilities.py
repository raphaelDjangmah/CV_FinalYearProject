import mysql.connector

class Databases:
    def dbConnection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'cvProject'
            )
            return connection
        except Exception as e:
            return False
    
    def queryDb(self, id, entryOrExit=1):
        if(self.dbConnection() == False):
            return "Database connection failed"

        #create a cursor and query db
        connection = self.dbConnection()
        cursor = connection.cursor()
        sql    = f'SELECT * FROM savedItems where STUDENTID={id} and FLAG={entryOrExit}'
        cursor.execute(sql)
        result = cursor.fetchall()

        return result
    
    def saveToDb(self, studentID,  item=None, entryFlag=1):
        if(self.dbConnection() == False):
            return "Database connection failed"

        #create a cursor and query db
        connection = self.dbConnection()
        cursor = connection.cursor()
        sql = 'INSERT INTO savedItems(STUDENTID, FLAG, ITEM1) VALUES(%s, %s, %s)'
        values = (studentID, entryFlag, item)

        try:
            cursor.execute(sql,values)
            connection.commit()
            return True
        except Exception as e:
            print(e)

        return False
    
    def updateDb(self, studentID , itemCount, item, entryFlag = 1):
        if(self.dbConnection() == False):
            return "Database connection failed"

        #create a cursor and query db
        connection = self.dbConnection()
        cursor = connection.cursor()
        sql    = f'UPDATE savedItems SET ITEM{itemCount}=%s where STUDENTID=%s and FLAG={entryFlag}'
        values = (item, studentID)
        
        try:
            cursor.execute(sql,values)
            connection.commit()
            return True
        except Exception as e:
            print(e)

        return False


if __name__ == '__main__':
    dbConnection = Databases()
    print(dbConnection.saveToDb(108877665,"mobile",0))
    # print(dbConnection.updateDb(10998877, 2, 'laptop'))


    