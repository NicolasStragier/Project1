class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "Leerling123",
            "db": "smartfridgedb"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor(buffered=True)

    def getDataFromDatabaseloggin(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM logging"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
        return result

    def getDataFromDatabaseusers(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM users"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
        return result



    def setDataToDatabaseGebruikers(self, value1, value2, value3):
        # Query met parameters
        sqlQuery = "INSERT INTO Gebruikers(Naam, Emailadres, Wachtwoord_hash) VALUES ('{param1}', '{param2}', md5('{param3}'))"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=value1, param2=value2, param3=value3)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        # self.__cursor.close()

    def setDataToDatabaseMetingen(self, value, type):
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO Metingen(Datum, Tijd, Waarde_meting, Soort_meting)" \
                   "VALUES (CURRENT_DATE , CURRENT_TIME , '{param1}', '{param2}')"
        sqlCommand = sqlQuery.format(param1=value, param2=type)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        # self.__cursor.close()

    def setDataToDatabaseMetingenMetVerandering(self, value, type, verandering):
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO Metingen(Datum, Tijd, Waarde_meting, Soort_meting, Bijsturen_meting)" \
                   "VALUES (CURRENT_DATE , CURRENT_TIME , '{param1}', '{param2}', '{param3}')"
        sqlCommand = sqlQuery.format(param1=value, param2=type, param3=verandering)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        # self.__cursor.close()

    def truncateTable(self, table):
        self.__cursor = self.__connection.cursor()
        sqlQuery = "truncate table {param1}"
        sqlCommand = sqlQuery.format(param1=table)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        # self.__cursor.close()

    def updateTable(self, unit, reports):
        self.__cursor = self.__connection.cursor()
        sqlQuery = "UPDATE Gebruikers " \
                   "SET Eenheid = '{param1}', Meldingen = '{param2}' " \
                   "WHERE Emailadres = 'update@update.be'"

        sqlCommand = sqlQuery.format(param1=unit, param2=reports)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()

    def insertConfig(self, hum, temp):
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO ConfiguratieId(GebruikerId, Humidity, Temperature)" \
                   "VALUES (16, {param1}, {param2})"
        sqlCommand = sqlQuery.format(param1=hum, param2=temp)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()


