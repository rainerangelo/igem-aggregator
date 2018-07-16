import requests
from bs4 import BeautifulSoup
from software import Software


class Scraper():
    def __init__(self, result):
        self.result = result

    def scrape(self, year):
        teamWikisPageSource = requests.get(
            'http://igem.org/Team_Wikis?year=' + str(year)).text
        teamWikisPageSoup = BeautifulSoup(teamWikisPageSource, 'lxml')
        teamWikisPageContent = teamWikisPageSoup.find('div', id='content_Page')
        links = self.getLinks(teamWikisPageContent)
        linksWithContent = self.getLinksWithContent(links)
        self.getLinkDescriptions(linksWithContent, year)

    def getLinks(self, teamWikisPageContent):
        links = []
        for link in teamWikisPageContent.findAll('a'):
            links.append(link['href'] + "/Software")
        return links

    def getLinksWithContent(self, links):
        linksWithContent = []
        for i in range(0, len(links), 1):
            wikiSource = requests.get(links[i]).text
            if "There is currently no text in this page." in wikiSource or "In order to be considered for the" in \
                    wikiSource or "you must fill this page." in wikiSource or "This page is used by the judges to " \
                    "evaluate your team for the" in wikiSource or "Regardless of the topic, iGEM projects often create " \
                    "or adapt computational tools to move the project forward." in wikiSource:
                pass
            else:
                linksWithContent.append(links[i])
        return linksWithContent

    def getLinkDescriptions(self, linksWithContent, year):
        for i in range(0, len(linksWithContent), 1):
            description = ""
            wikiWithContentSource = requests.get(linksWithContent[i]).text
            wikiWithContentSoup = BeautifulSoup(wikiWithContentSource, 'lxml')
            wikiWithContentContent = wikiWithContentSoup.find(
                'div', id='bodyContent')
            paragraphs = []
            for paragraph in wikiWithContentContent.findAll('p'):
                temp = "".join(line.strip()
                               for line in paragraph.text.split("\n"))
                if "<style" in str(paragraph) or "</style>" in str(paragraph) or "<script" in str(paragraph) or \
                        "</script>" in str(paragraph) or len(temp) == 0:
                    pass
                else:
                    paragraphs.append("".join(line.strip()
                                              for line in paragraph.text.split("\n")))
            j = 0
            while len(description) < 500 and j < len(paragraphs):
                k = 0
                while len(description) < 500 and k < len(paragraphs[j]):
                    description += paragraphs[j][k]
                    k += 1
                j += 1
                description += " "
            description += "..."
            software = Software(linksWithContent[i].split(
                "/")[3].split(":")[1], description, year)
            self.result.emit(software)
