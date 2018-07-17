from model import Model
from view import View
from software import Software
from scraper import Scraper
from PyQt5 import QtCore, QtGui, QtWidgets


class ScrapeThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(Software)

    def __init__(self, year):
        QtCore.QThread.__init__(self)
        self.year = year
        self.scraper = Scraper(self.progress, self.result)

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
            buttons[0].clicked.connect(lambda: self.prepareBack())
            buttons[1].clicked.connect(lambda: self.view.switchTo(0))
            buttons[2].clicked.connect(lambda: self.openLibrary())
            buttons[3].clicked.connect(lambda: self.view.switchTo(2))
            buttons[4].clicked.connect(lambda: self.view.switchTo(3))

        self.view.homeLibraryButton.clicked.connect(lambda: self.openLibrary())
        self.view.homeSearchButton.clicked.connect(lambda: self.view.switchTo(2))
        self.view.homeInfoButton.clicked.connect(lambda: self.view.switchTo(3))

        self.view.librarySearchLine.returnPressed.connect(self.startSearching)
        self.view.scrapeSearchLine.returnPressed.connect(self.prepareScrape)

        self.view.libraryResultsList.currentItemChanged.connect(self.viewSoftware)

        self.view.editButton.clicked.connect(lambda: self.edit())
        self.view.confirmButton.clicked.connect(lambda: self.confirmEdit())
        self.view.cancelButton.clicked.connect(lambda: self.cancelEdit())

        self.view.window.show()

    def edit(self):
        self.view.enableAddEdit()

    def confirmEdit(self):
        self.view.disableAddEdit()
        software = Software(self.view.addEditTeam.text(), self.view.addEditDescription.toPlainText(), str(self.view.addEditYear.text()))
        self.model.replace(software)
    
    def cancelEdit(self):
        self.view.disableAddEdit()
        self.view.addEditDescription.setText(self.view.libraryResultsList.itemWidget(self.view.libraryResultsList.currentItem()).description.text())

    def prepareBack(self):
        self.startSearching()
        self.view.goBack()

    def viewSoftware(self):
        selectedWidget = self.view.libraryResultsList.itemWidget(self.view.libraryResultsList.currentItem())
        if selectedWidget != None:
            self.view.addEditTeam.setText(selectedWidget.team.text())
            self.view.addEditDescription.setText(selectedWidget.description.text())
            self.view.addEditYear.setText(selectedWidget.year.text())
            self.view.switchTo(4)

    def openLibrary(self):
        self.listAll()
        self.view.switchTo(1)

    def listAll(self):
        self.view.libraryResultsList.clear()
        softwareList = self.model.getAll()
        for i in softwareList:
            software = Software(i[0], i[1], str(i[2]))
            self.view.addToList(self.view.libraryResultsList, software)

    def startSearching(self):
        self.view.libraryResultsList.clear()
        if len(self.view.librarySearchLine.text()) == 0 or self.view.librarySearchLine.text() == "Enter a year":
            self.listAll()
        else:
            year = int(self.view.librarySearchLine.text())
            softwareList = self.model.getAllFromYear(year)
            for i in softwareList:
                software = Software(i[0], i[1], str(i[2]))
                self.view.addToList(self.view.libraryResultsList, software)

    def prepareScrape(self):
        year = int(self.view.scrapeSearchLine.text())

        if self.model.checkYear(year):
            overwriteMessage = QtWidgets.QMessageBox()
            choice = overwriteMessage.question(self.view.window, "Sara", "Software from this year can already be found in the Library. Clicking \"Yes\" will overwrite these.", overwriteMessage.Yes | overwriteMessage.No)

            if choice == overwriteMessage.Yes:
                self.startScraping(year)
            else:
                self.view.scrapeSearchLine.setText(str(year))

        else:
            scrapeMessage = QtWidgets.QMessageBox()
            choice = scrapeMessage.question(self.view.window, "Sara", "Sara will now search the web for software from this year. Do you want to continue?", scrapeMessage.Yes | scrapeMessage.No)

            if choice == scrapeMessage.Yes:
                self.startScraping(year)
            else:
                self.view.scrapeSearchLine.setText(str(year))

    def startScraping(self, year):
        self.view.scrapeResultsList.clear()
        self.scrapeThread = ScrapeThread(year)

        self.view.progressBar.setValue(0)
        self.scrapeThread.progress.connect(self.updateProgressBar)

        self.scrapeThread.result.connect(self.addToDatabase)
        self.scrapeThread.finished.connect(lambda: self.showResults(year))
        self.scrapeThread.start()

    def updateProgressBar(self, val):
        self.view.progressBar.setValue(self.view.progressBar.value() + val)

    def addToDatabase(self, software):
        self.model.replace(software)

    def showResults(self, year):
        self.view.progressBar.setValue(100)
        softwareList = self.model.getAllFromYear(year)
        for i in softwareList:
            software = Software(i[0], i[1], str(i[2]))
            self.view.addToList(self.view.scrapeResultsList, software)
        finishMessage = QtWidgets.QMessageBox()
        finishMessage.question(self.view.window, "Sara", "Sara is finished searching.", finishMessage.Ok)
