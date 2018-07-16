from model import Model
from view import View
from software import Software
from scraper import Scraper
from PyQt5 import QtCore, QtWidgets


class ScrapeThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(Software)

    def __init__(self, year):
        QtCore.QThread.__init__(self)
        self.year = year
        self.scraper = Scraper(self.result)

    def __del__(self):
        self.wait()

    def getData(self):
        self.scraper.scrape(self.year)

    def run(self):
        self.getData()
        self.finished.emit()


class Controller:
    def __init__(self, model, view, parent=None):
        self.model = model
        self.view = view

        for buttons in self.view.menuButtons:
            buttons[0].clicked.connect(lambda: self.view.goBack())
            buttons[1].clicked.connect(lambda: self.view.switchTo(0))
            buttons[2].clicked.connect(lambda: self.listAll())
            buttons[3].clicked.connect(lambda: self.view.switchTo(2))
            buttons[4].clicked.connect(lambda: self.view.switchTo(3))

        self.view.homeLibraryButton.clicked.connect(
            lambda: self.listAll())
        self.view.homeSearchButton.clicked.connect(
            lambda: self.view.switchTo(2))
        self.view.homeInfoButton.clicked.connect(lambda: self.view.switchTo(3))

        self.view.librarySearchLine.returnPressed.connect(self.startSearching)
        self.view.scrapeSearchLine.returnPressed.connect(self.startScraping)

        self.view.window.show()

    def listAll(self):
        self.view.libraryResultsList.clear()
        softwareList = self.model.getAll()
        for i in softwareList:
            software = Software(i[0], i[1], str(i[2]))
            self.view.addToList(self.view.libraryResultsList, software)
        self.view.switchTo(1)

    def startSearching(self):
        self.view.libraryResultsList.clear()
        if len(self.view.librarySearchLine.text()) == 0:
            self.listAll()
        else:
            year = int(self.view.librarySearchLine.text())
            softwareList = self.model.getAllFromYear(year)
            for i in softwareList:
                software = Software(i[0], i[1], str(i[2]))
                self.view.addToList(self.view.libraryResultsList, software)

    def startScraping(self):
        self.view.scrapeResultsList.clear()
        year = int(self.view.scrapeSearchLine.text())
        self.scrapeThread = ScrapeThread(year)
        self.scrapeThread.result.connect(self.addToDatabase)
        self.scrapeThread.finished.connect(lambda: self.showResults(year))
        self.scrapeThread.start()

    def addToDatabase(self, software):
        self.model.replace(software)

    def showResults(self, year):
        softwareList = self.model.getAllFromYear(year)
        for i in softwareList:
            software = Software(i[0], i[1], str(i[2]))
            self.view.addToList(self.view.scrapeResultsList, software)
