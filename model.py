import operator
import sqlite3
from software import Software


class Model:
    def __init__(self, parent=None):
        self.connection = sqlite3.connect('software.db')

        # self.createTable()

        # self.dropTable()

    def createTable(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE software (
            team text,
            description text,
            year integer
        )""")
        cursor.execute(
            "CREATE UNIQUE INDEX team_and_year ON software (team, year)")
        self.connection.commit()
        print("Created table: software")

    def dropTable(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS software")
        self.connection.commit()
        print("Dropped table: software")

    def checkYear(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM software WHERE year = :year LIMIT 1", {'year': year})
        softwareList = cursor.fetchall()
        if len(softwareList) == 1:
            return True
        return False

    def getAll(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM software")
        softwareList = cursor.fetchall()
        softwareList = sorted(softwareList, key=operator.itemgetter(2, 0))
        return softwareList

    def getAllFromYear(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM software WHERE year = :year", {'year': year})
        softwareList = cursor.fetchall()
        softwareList = sorted(softwareList, key=operator.itemgetter(2, 0))
        return softwareList

    def replace(self, software):
        cursor = self.connection.cursor()
        cursor.execute("REPLACE INTO software VALUES (:team, :description, :year)",
                       {'team': software.team, 'description': software.description, 'year': software.year})
        self.connection.commit()


if __name__ == '__main__':
    model = Model()
    # model.createTable()
    # model.dropTable()
