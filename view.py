import sys
from software import Software
from PyQt5 import QtCore, QtGui, QtWidgets


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setText(self.hover)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.setText(self.default)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def setImages(self, default, hover):
        self.default = default
        self.hover = hover
        self.setText(self.default)

    def setToDefault(self):
        self.setText(self.default)


class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)

    def focusInEvent(self, event):
        super(CustomLineEdit, self).focusInEvent(event)
        self.clear()

    def setSuggestion(self, suggestion):
        self.suggestion = suggestion

    def showSuggestion(self):
        self.setText(self.suggestion)


class SoftwareWidget(QtWidgets.QWidget):
    def __init__(self, font, parent=None):
        super(SoftwareWidget, self).__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background = transparent;
            }
        """)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.font = font

        self.font.setBold(True)

        self.team = QtWidgets.QLabel()
        self.team.setFont(self.font)
        self.team.setWordWrap(True)

        self.font.setBold(False)

        self.description = QtWidgets.QLabel()
        self.description.setFont(self.font)
        self.description.setWordWrap(True)
        self.description.setAlignment(QtCore.Qt.AlignJustify)

        self.year = QtWidgets.QLabel()
        self.year.setFont(self.font)
        self.year.setWordWrap(True)

        self.vBoxLayout.addWidget(self.team)
        self.vBoxLayout.addWidget(self.description)
        self.vBoxLayout.addWidget(self.year)
        self.setLayout(self.vBoxLayout)

    def setTeam(self, text):
        self.team.setText(text)

    def setDescription(self, text):
        self.description.setText(text)

    def setYear(self, text):
        self.year.setText(text)


class View:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Software Aggregator Research Assistant")
        self.window.resize(1800, 1000)
        self.window.setStyleSheet("""
            QLabel {
                color: rgb(70, 70, 70);
            }
            QLineEdit {
                border: 1px solid rgb(209, 209, 209);
                color: rgb(70, 70, 70);
            }
            QListWidget {
                border: none;
                color: rgb(70, 70, 70);
                outline: 0;
            }
            QProgressBar {
                border: 20px solid rgb(255, 255, 255);
            }
            QTextEdit {
                border: 1px solid rgb(209, 209, 209);
                color: rgb(70, 70, 70);
            }
            QTextBrowser {
                background-color: transparent;
                border: none;
                color: rgb(70, 70, 70);
                text-align: justify;
            }
        """)

        self.font = self.loadFont()

        self.mainLayout = QtWidgets.QGridLayout(self.window)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget = QtWidgets.QStackedWidget(self.window)

        self.home = QtWidgets.QWidget()
        self.library = QtWidgets.QWidget()
        self.scrape = QtWidgets.QWidget()
        self.info = QtWidgets.QWidget()
        self.addEdit = QtWidgets.QWidget()

        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.library)
        self.stackedWidget.addWidget(self.scrape)
        self.stackedWidget.addWidget(self.info)
        self.stackedWidget.addWidget(self.addEdit)

        self.menuButtons = []

        self.setupHome()
        self.setupLibrary()
        self.setupScrape()
        self.setupInfo()
        self.setupAddEdit()

        self.mainLayout.addWidget(self.stackedWidget)

        self.currentPage = 0
        self.pageHistory = [0]

        self.stackedWidget.setCurrentIndex(0)

        # self.window.show()

    def loadFont(self):
        fontDb = QtGui.QFontDatabase()
        fontId = fontDb.addApplicationFont(
            'fonts/Quicksand/Quicksand-Regular.ttf')
        fontFam = fontDb.applicationFontFamilies(fontId)
        return QtGui.QFont(fontFam[0])

    def createMenuBar(self, page, layout):
        menuBar = QtWidgets.QWidget()
        menuBar.setStyleSheet("background-color: rgb(65, 60, 88)")

        menuBarLayout = QtWidgets.QVBoxLayout()
        menuBarLayout.setSpacing(0)
        menuBarLayout.setContentsMargins(0, 0, 0, 0)

        logo = QtWidgets.QLabel()
        logo.setText(
            "<html><body><p><img src=\"icons/sara-white.png\"></p></body></html>")

        backButton = ClickableLabel()
        backButton.setImages("<html><body><p><img src=\"icons/arrow-left-solid-white-back.png\"></p></body></html>",
                             "<html><body><p><img src=\"icons/arrow-left-solid-white-back-hover.png\"></p></body></html>")
        homeButton = ClickableLabel()
        homeButton.setImages("<html><body><p><img src=\"icons/home-solid-white-home.png\"></p></body></html>",
                             "<html><body><p><img src=\"icons/home-solid-white-home-hover.png\"></p></body></html>")
        libraryButton = ClickableLabel()
        libraryButton.setImages("<html><body><p><img src=\"icons/book-solid-white-library.png\"></p></body></html>",
                                "<html><body><p><img src=\"icons/book-solid-white-library-hover.png\"></p></body></html>")
        scrapeButton = ClickableLabel()
        scrapeButton.setImages("<html><body><p><img src=\"icons/search-solid-white-searchweb.png\"></p></body></html>",
                               "<html><body><p><img src=\"icons/search-solid-white-searchweb-hover.png\"></p></body></html>")
        infoButton = ClickableLabel()
        infoButton.setImages("<html><body><p><img src=\"icons/info-solid-white-information.png\"></p></body></html>",
                             "<html><body><p><img src=\"icons/info-solid-white-information-hover.png\"></p></body></html>")

        buttons = [backButton, homeButton,
                   libraryButton, scrapeButton, infoButton]
        self.menuButtons.append(buttons)

        menuBarLayout.addWidget(logo)
        menuBarLayout.addWidget(backButton)
        menuBarLayout.addWidget(homeButton)
        menuBarLayout.addWidget(libraryButton)
        menuBarLayout.addWidget(scrapeButton)
        menuBarLayout.addWidget(infoButton)
        menuBarLayout.addStretch()

        menuBar.setLayout(menuBarLayout)

        layout.addWidget(menuBar)
        page.setLayout(layout)

    def createTitleBar(self, page, layout, contentLayout, image):
        titleBar = QtWidgets.QWidget()
        titleBar.setStyleSheet("background-color: rgb(255, 255, 255)")

        titleBarLayout = QtWidgets.QHBoxLayout()
        titleBarLayout.setSpacing(0)
        titleBarLayout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel(page)
        title.setText(image)

        titleBarLayout.addWidget(title)

        titleBar.setLayout(titleBarLayout)

        contentLayout.addWidget(titleBar)

    def setupHome(self):
        self.homeLayout = QtWidgets.QHBoxLayout()
        self.homeLayout.setSpacing(0)
        self.homeLayout.setContentsMargins(0, 0, 0, 0)
        self.homeContentLayout = QtWidgets.QVBoxLayout()

        self.createMenuBar(self.home, self.homeLayout)

        self.createTitleBar(self.home, self.homeLayout, self.homeContentLayout,
                            "<html><body><p><img src=\"icons/home-title-white.png\"></p></body></html>")

        self.homeInfoWidget = QtWidgets.QWidget()
        self.homeInfoLayout = QtWidgets.QVBoxLayout()
        self.homeInfoLayout.setContentsMargins(40, 40, 40, 40)
        self.homeButtonsLayout = QtWidgets.QHBoxLayout()
        self.homeButtonsLayout.setSpacing(40)

        self.homeLibraryButton = ClickableLabel(self.home)
        self.homeLibraryButton.setImages("<html><body><p><img src=\"icons/home-library-white.png\"></p></body></html>",
                                         "<html><body><p><img src=\"icons/home-library-hover.png\"></p></body></html>")
        self.homeSearchButton = ClickableLabel(self.home)
        self.homeSearchButton.setImages("<html><body><p><img src=\"icons/home-searchweb-white.png\"></p></body></html>",
                                        "<html><body><p><img src=\"icons/home-searchweb-hover.png\"></p></body></html>")
        self.homeInfoButton = ClickableLabel(self.home)
        self.homeInfoButton.setImages("<html><body><p><img src=\"icons/home-information-white.png\"></p></body></html>",
                                      "<html><body><p><img src=\"icons/home-information-hover.png\"></p></body></html>")

        self.homeButtonsLayout.addWidget(self.homeLibraryButton)
        self.homeButtonsLayout.addWidget(self.homeSearchButton)
        self.homeButtonsLayout.addWidget(self.homeInfoButton)
        self.homeButtonsLayout.addStretch()
        self.homeInfoLayout.addLayout(self.homeButtonsLayout)
        self.homeInfoLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.homeInfoWidget.setLayout(self.homeInfoLayout)
        self.homeContentLayout.addWidget(self.homeInfoWidget)

        self.homeLayout.addLayout(self.homeContentLayout)

    def setupLibrary(self):
        self.libraryLayout = QtWidgets.QHBoxLayout()
        self.libraryLayout.setSpacing(0)
        self.libraryLayout.setContentsMargins(0, 0, 0, 0)
        self.libraryContentLayout = QtWidgets.QVBoxLayout()

        self.createMenuBar(self.library, self.libraryLayout)

        self.createTitleBar(self.library, self.libraryLayout, self.libraryContentLayout,
                            "<html><body><p><img src=\"icons/library-title-white.png\"></p></body></html>")

        self.libraryInfoWidget = QtWidgets.QWidget()
        self.libraryInfoLayout = QtWidgets.QVBoxLayout()
        self.libraryInfoLayout.setSpacing(40)
        self.libraryInfoLayout.setContentsMargins(40, 40, 40, 40)

        self.librarySearchWidget = QtWidgets.QWidget()
        self.librarySearchWidget.setStyleSheet(
            "background-color: rgb(255, 255, 255)")
        self.librarySearchLayout = QtWidgets.QHBoxLayout()
        self.librarySearchLayout.setSpacing(40)
        self.librarySearchLayout.setContentsMargins(40, 40, 40, 40)

        font = self.font
        font.setPointSize(10)
        self.librarySearchInstr = QtWidgets.QLabel()
        self.librarySearchInstr.setFont(font)
        self.librarySearchInstr.setText("What are you looking for?")

        self.librarySearchLine = CustomLineEdit()
        self.librarySearchLine.setFont(font)
        self.librarySearchLine.setSuggestion("Enter a year")

        self.librarySearchLayout.addWidget(self.librarySearchInstr)
        self.librarySearchLayout.addWidget(self.librarySearchLine)

        self.librarySearchWidget.setLayout(self.librarySearchLayout)

        self.libraryResultsList = QtWidgets.QListWidget()
        self.libraryResultsList.setFont(font)
        self.libraryResultsList.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.libraryInfoLayout.addWidget(self.librarySearchWidget)
        self.libraryInfoLayout.addWidget(self.libraryResultsList)

        self.libraryInfoLayout.addItem(QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.libraryInfoWidget.setLayout(self.libraryInfoLayout)
        self.libraryContentLayout.addWidget(self.libraryInfoWidget)

        self.libraryLayout.addLayout(self.libraryContentLayout)

    def setupScrape(self):
        self.scrapeLayout = QtWidgets.QHBoxLayout()
        self.scrapeLayout.setSpacing(0)
        self.scrapeLayout.setContentsMargins(0, 0, 0, 0)
        self.scrapeContentLayout = QtWidgets.QVBoxLayout()

        self.createMenuBar(self.scrape, self.scrapeLayout)

        self.createTitleBar(self.scrape, self.scrapeLayout, self.scrapeContentLayout,
                            "<html><body><p><img src=\"icons/searchweb-title-white.png\"></p></body></html>")

        self.scrapeInfoWidget = QtWidgets.QWidget()
        self.scrapeInfoLayout = QtWidgets.QVBoxLayout()
        self.scrapeInfoLayout.setSpacing(40)
        self.scrapeInfoLayout.setContentsMargins(40, 40, 40, 40)

        self.scrapeSearchWidget = QtWidgets.QWidget()
        self.scrapeSearchWidget.setStyleSheet(
            "background-color: rgb(255, 255, 255)")
        self.scrapeSearchLayout = QtWidgets.QHBoxLayout()
        self.scrapeSearchLayout.setSpacing(40)
        self.scrapeSearchLayout.setContentsMargins(40, 40, 40, 40)

        font = self.font
        font.setPointSize(10)
        self.scrapeSearchInstr = QtWidgets.QLabel()
        self.scrapeSearchInstr.setFont(font)
        self.scrapeSearchInstr.setText("What are you searching for?")

        self.scrapeSearchLine = CustomLineEdit()
        self.scrapeSearchLine.setFont(font)
        self.scrapeSearchLine.setSuggestion("Enter a year")

        self.scrapeSearchLayout.addWidget(self.scrapeSearchInstr)
        self.scrapeSearchLayout.addWidget(self.scrapeSearchLine)

        self.scrapeSearchWidget.setLayout(self.scrapeSearchLayout)

        self.scrapeResultsList = QtWidgets.QListWidget()
        self.scrapeResultsList.setFont(font)
        self.scrapeResultsList.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setTextVisible(False)

        self.scrapeInfoLayout.addWidget(self.scrapeSearchWidget)
        self.scrapeInfoLayout.addWidget(self.scrapeResultsList)
        self.scrapeInfoLayout.addWidget(self.progressBar)

        self.scrapeInfoLayout.addItem(QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.scrapeInfoWidget.setLayout(self.scrapeInfoLayout)

        self.scrapeContentLayout.addWidget(self.scrapeInfoWidget)

        self.scrapeLayout.addLayout(self.scrapeContentLayout)

    def setupInfo(self):
        self.infoLayout = QtWidgets.QHBoxLayout()
        self.infoLayout.setSpacing(0)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoContentLayout = QtWidgets.QVBoxLayout()

        self.createMenuBar(self.info, self.infoLayout)

        self.createTitleBar(self.info, self.infoLayout, self.infoContentLayout,
                            "<html><body><p><img src=\"icons/information-title-white.png\"></p></body></html>")

        self.infoInfoWidget = QtWidgets.QWidget()
        self.infoInfoLayout = QtWidgets.QVBoxLayout()
        self.infoInfoLayout.setSpacing(40)
        self.infoInfoLayout.setContentsMargins(40, 40, 40, 40)

        font = self.font
        font.setPointSize(10)
        self.infoDescription = QtWidgets.QTextBrowser()
        self.infoDescription.setFont(font)
        self.infoDescription.setText(
            "<html><body style=\"margin-right: 40px;\"><h4>What is Sara?</h4><p align=\"justify\">Sara stands for Software Aggregator Research Assistant. It is a bot that gathers software developed by past iGEM teams and puts them into one place.</p>"
            "<br><h4>What's the point?</h4><p align=\"justify\">We created Sara because we noticed that software developed by iGEM teams typically do not get used after development and we think it's because they are not the easiest to find. So we created a bot that can scrape the web for previous iGEM teams' software and store them all into a searchable database.</p>"
            "<br><h4>How do I use Sara?</h4><p align=\"justify\">Sara has two main features: LIBRARY and SEARCH WEB. LIBRARY is where you can find all software that have already been scraped by Sara or inputted by users. SEARCH WEB is where you can use Sara to scrape the web for previous iGEM teams' software.</p>"
            "<br><h4>LIBRARY</h4><p align=\"justify\">Enter a team name, a description of the software you're looking for, or a year on the search bar, and Sara will provide software that may be useful to you.</p>"
            "<br><h4>SEARCH WEB</h4><p align=\"justify\">Enter a year, and Sara will venture into the depths of the web world to search for more iGEM software developed in that year.</p></body></html>")

        self.infoInfoLayout.addWidget(self.infoDescription)

        self.infoInfoLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.infoInfoWidget.setLayout(self.infoInfoLayout)

        self.infoContentLayout.addWidget(self.infoInfoWidget)

        self.infoLayout.addLayout(self.infoContentLayout)

    def setupAddEdit(self):
        self.addEditLayout = QtWidgets.QHBoxLayout()
        self.addEditLayout.setSpacing(0)
        self.addEditLayout.setContentsMargins(0, 0, 0, 0)
        self.addEditContentLayout = QtWidgets.QVBoxLayout()

        self.createMenuBar(self.addEdit, self.addEditLayout)

        self.createTitleBar(self.addEdit, self.addEditLayout, self.addEditContentLayout, "<html><body><p><img src=\"icons/edit-title-white.png\"></p></body></html>")

        self.addEditInfoWidget = QtWidgets.QWidget()
        self.addEditInfoLayout = QtWidgets.QVBoxLayout()
        self.addEditInfoLayout.setSpacing(40)
        self.addEditInfoLayout.setContentsMargins(40, 40, 40, 40)

        self.teamWidget = QtWidgets.QWidget()
        self.teamWidget.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.teamLayout = QtWidgets.QHBoxLayout()
        self.teamLayout.setSpacing(40)
        self.teamLayout.setContentsMargins(40, 40, 40, 40)

        self.descriptionWidget = QtWidgets.QWidget()
        self.descriptionWidget.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.descriptionLayout = QtWidgets.QHBoxLayout()
        self.descriptionLayout.setSpacing(40)
        self.descriptionLayout.setContentsMargins(40, 40, 40, 40)

        self.yearWidget = QtWidgets.QWidget()
        self.yearWidget.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.yearLayout = QtWidgets.QHBoxLayout()
        self.yearLayout.setSpacing(40)
        self.yearLayout.setContentsMargins(40, 40, 40, 40)

        font = self.font
        font.setPointSize(10)

        self.addEditTeamLabel = QtWidgets.QLabel()
        self.addEditTeamLabel.setFont(font)
        self.addEditTeamLabel.setText("Team:")
        self.addEditTeam = QtWidgets.QLineEdit()
        self.addEditTeam.setFont(font)

        self.addEditDescriptionLabel = QtWidgets.QLabel()
        self.addEditDescriptionLabel.setFont(font)
        self.addEditDescriptionLabel.setText("Description:")
        self.addEditDescription = QtWidgets.QTextEdit()
        self.addEditDescription.setFont(font)

        self.addEditYearLabel = QtWidgets.QLabel()
        self.addEditYearLabel.setFont(font)
        self.addEditYearLabel.setText("Year:")
        self.addEditYear = QtWidgets.QLineEdit()
        self.addEditYear.setFont(font)

        self.teamLabelLayout = QtWidgets.QVBoxLayout()
        self.teamLabelLayout.addWidget(self.addEditTeamLabel)
        self.teamLabelLayout.addItem(QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))

        self.descriptionLabelLayout = QtWidgets.QVBoxLayout()
        self.descriptionLabelLayout.addWidget(self.addEditDescriptionLabel)
        self.descriptionLabelLayout.addItem(QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))

        self.yearLabelLayout = QtWidgets.QVBoxLayout()
        self.yearLabelLayout.addWidget(self.addEditYearLabel)
        self.yearLabelLayout.addItem(QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))

        self.teamLayout.addLayout(self.teamLabelLayout)
        self.teamLayout.addWidget(self.addEditTeam)
        self.teamWidget.setLayout(self.teamLayout)

        self.descriptionLayout.addLayout(self.descriptionLabelLayout)
        self.descriptionLayout.addWidget(self.addEditDescription)
        self.descriptionWidget.setLayout(self.descriptionLayout)

        self.yearLayout.addLayout(self.yearLabelLayout)
        self.yearLayout.addWidget(self.addEditYear)
        self.yearWidget.setLayout(self.yearLayout)

        self.addEditButtonsLayout = QtWidgets.QHBoxLayout()
        self.addEditButtonsLayout.setAlignment(QtCore.Qt.AlignHCenter)

        self.editButton = ClickableLabel()
        self.editButton.setImages("<html><body><p><img src=\"icons/edit-default.png\"></p></body></html>",
                                  "<html><body><p><img src=\"icons/edit-hover.png\"></p></body></html>")
        self.confirmButton = ClickableLabel()
        self.confirmButton.setImages("<html><body><p><img src=\"icons/confirm-default.png\"></p></body></html>",
                                     "<html><body><p><img src=\"icons/confirm-hover.png\"></p></body></html>")
        self.cancelButton = ClickableLabel()
        self.cancelButton.setImages("<html><body><p><img src=\"icons/cancel-default.png\"></p></body></html>",
                                    "<html><body><p><img src=\"icons/cancel-hover.png\"></p></body></html>")

        self.addEditButtonsLayout.addWidget(self.editButton)
        self.addEditButtonsLayout.addWidget(self.confirmButton)
        self.addEditButtonsLayout.addWidget(self.cancelButton)

        self.menuButtons[4][1].setVisible(False)
        self.menuButtons[4][2].setVisible(False)
        self.menuButtons[4][3].setVisible(False)
        self.menuButtons[4][4].setVisible(False)

        self.disableAddEdit()

        self.addEditInfoLayout.addWidget(self.teamWidget)
        self.addEditInfoLayout.addWidget(self.descriptionWidget)
        self.addEditInfoLayout.addWidget(self.yearWidget)
        self.addEditInfoLayout.addLayout(self.addEditButtonsLayout)

        self.addEditInfoLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.addEditInfoWidget.setLayout(self.addEditInfoLayout)

        self.addEditContentLayout.addWidget(self.addEditInfoWidget)

        self.addEditLayout.addLayout(self.addEditContentLayout)

    def enableAddEdit(self):
        self.addEditDescription.setEnabled(True)

        self.addEditDescription.setStyleSheet("border: 1px solid rgb(209, 209, 209)")

        self.editButton.setVisible(False)
        self.confirmButton.setVisible(True)
        self.cancelButton.setVisible(True)

    def disableAddEdit(self):
        self.addEditTeam.setEnabled(False)
        self.addEditDescription.setEnabled(False)
        self.addEditYear.setEnabled(False)

        self.addEditTeam.setStyleSheet("border: none")
        self.addEditDescription.setStyleSheet("border: none")
        self.addEditYear.setStyleSheet("border: none")

        self.editButton.setVisible(True)
        self.confirmButton.setVisible(False)
        self.cancelButton.setVisible(False)

    def switchTo(self, index):
        self.window.setFocus()
        if index == 1:
            self.librarySearchLine.showSuggestion()
        if index == 2:
            self.scrapeSearchLine.showSuggestion()
        if index == 4:
            self.disableAddEdit()
        if index != self.currentPage:
            self.stackedWidget.setCurrentIndex(index)
            self.currentPage = index
            self.pageHistory.append(index)

    def goBack(self):
        if len(self.pageHistory) > 1:
            self.stackedWidget.setCurrentIndex(self.pageHistory[-2])
            self.currentPage = self.pageHistory[-2]
            del self.pageHistory[-1]

    def addToList(self, softwareList, software):
        softwareWidget = SoftwareWidget(self.font)

        softwareWidget.setTeam(software.team)
        softwareWidget.setDescription(software.description)
        softwareWidget.setYear(software.year)

        softwareItem = QtWidgets.QListWidgetItem(softwareList)
        softwareItem.setSizeHint(softwareWidget.sizeHint())

        softwareList.addItem(softwareItem)
        softwareList.setItemWidget(softwareItem, softwareWidget)


if __name__ == '__main__':
    view = View()
