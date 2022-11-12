import requests
from bs4 import BeautifulSoup

import sqlite3
import pyodbc


def sqlSrv_Connect():
    conn = pyodbc.connect(
        "Driver=SQL Server Native Client 11.0;Server=pedres2;Database=psbi_lab;uid=admin1;pwd=admin1;")
    cursor = conn.cursor()
    cursor.execute("select * from tblLogin")

    cursor.close()
    conn.close()


def deleteOldRecords():
    conn = sqlite3.connect("articlesscrap.db")
    cursor = conn.cursor()
    cursor.execute("delete from articles")

    cursor.close()
    conn.commit()
    conn.close()


def addArticles(var_article_button, var_article_cit, var_article_pmid_heading, var_article_heading_title,
                var_article_author_list, var_article_abstract):
    conn = sqlite3.connect('articlesscrap.db')
    cursor = conn.cursor()

    data_tuple = (var_article_button,
                  var_article_cit,
                  var_article_pmid_heading,
                  var_article_heading_title,
                  var_article_author_list,
                  var_article_abstract)

    qry = '''insert into articles(jrnme, jryr, pmid, title, author, abstract) values(?, ?, ?, ?, ?, ?)'''
    cursor.execute(qry, data_tuple)
    conn.commit()

    cursor.close()
    conn.close()


def scrapArticles_Pg1():
    WEB_URL = "https://pubmed.ncbi.nlm.nih.gov"
    URL = "https://pubmed.ncbi.nlm.nih.gov/?term=%28%22Infant%22%5BMesh%5D+OR+%22Infant%2C+Newborn%22%5BMesh%5D+OR+%22Child%22%5BMesh%5D+OR+%22Child%2C+Preschool%22%5BMesh%5D+OR+infan*+OR+babies+OR+baby+OR+newborn*+OR+neonat*+OR+toddler*+OR+child*%5Btiab%5D%29+AND+%28%22Weaning%22%5BMesh%5D+OR+%22Infant+Nutritional+Physiological+Phenomena%22%5BMesh%5D+OR+%22Feeding+Behavior%22%5BMesh%5D+OR+complementary+feed*%5Btiab%5D+OR+complementary+food*%29+AND+%28introduc*%5Btiab%5D+OR+introduction%5Btiab%5D+OR+initiation%5Btiab%5D+OR+early%5Btiab%5D+OR+late%5Btiab%5D+OR+time%5Btiab%5D+OR+timing%5Btiab%5D%29&sort=pubdate&sort_order=asc&size=200"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    href = soup.find_all('a', attrs={"class", "docsum-title"})

    # sqlSrv_Connect()

    count = 0
    for id in href:
        child_req = requests.get(WEB_URL + href[count].get("href"))
        child_soup = BeautifulSoup(child_req.content, 'html.parser')

        article_main = child_soup.find("main", attrs={"class", "article-details"})
        article_header = article_main.find("header", attrs={"class", "heading"})

        article_button = article_header.find("button", attrs={"class", "journal-actions-trigger trigger"})
        var_article_button = article_button.text.strip()

        article_cit = article_header.find("span", attrs={"class", "cit"})
        var_article_cit = article_cit.text.strip()

        article_heading_title = article_header.find("h1")

        if article_heading_title is not None:
            var_article_heading_title = article_heading_title.text.strip()
        else:
            var_article_heading_title = ""

            article_author_list = article_header.find("div", attrs={"class", "authors-list"})

            if article_author_list is not None:
                var_article_author_list = article_author_list.text.strip().replace(",", " -")
            else:
                var_article_author_list = ""

            article_pmid = article_header.find("ul", attrs={"class", "identifiers"})

            if article_pmid is not None:
                article_pmid_heading = article_pmid.find("span", attrs={"class", "id-label"})
                article_pmid_value = article_pmid.find("strong", attrs={"class", "current-id"})
                var_article_pmid_heading = article_pmid_heading.text.strip() + article_pmid_value.text.strip()
            else:
                var_article_pmid_heading = ""

            article_abstract = child_soup.find("div", attrs={"class", "abstract"})
            article_abstract = article_abstract.find("p")

            if article_abstract is not None:
                for data in article_abstract(['p', 'strong']):
                    # Remove tags
                    data.decompose()
                    ' '.join(article_abstract.stripped_strings)
                    var_article_abstract = ' '.join(article_abstract.stripped_strings)
            else:
                var_article_abstract = ""

            addArticles(var_article_button, var_article_cit, var_article_pmid_heading, var_article_heading_title,
                        var_article_author_list, var_article_abstract)

            count = count + 1


def scrapArticles_Oth_Pg():
    WEB_URL = "https://pubmed.ncbi.nlm.nih.gov"
    pg = 2
    URL = "https://pubmed.ncbi.nlm.nih.gov/?term=(%22Infant%22%5BMesh%5D%20OR%20%22Infant%2C%20Newborn%22%5BMesh%5D%20OR%20%22Child%22%5BMesh%5D%20OR%20%22Child%2C%20Preschool%22%5BMesh%5D%20OR%20infan*%20OR%20babies%20OR%20baby%20OR%20newborn*%20OR%20neonat*%20OR%20toddler*%20OR%20child*%5Btiab%5D)%20AND%20(%22Weaning%22%5BMesh%5D%20OR%20%22Infant%20Nutritional%20Physiological%20Phenomena%22%5BMesh%5D%20OR%20%22Feeding%20Behavior%22%5BMesh%5D%20OR%20complementary%20feed*%5Btiab%5D%20OR%20complementary%20food*)%20AND%20(introduc*%5Btiab%5D%20OR%20introduction%5Btiab%5D%20OR%20initiation%5Btiab%5D%20OR%20early%5Btiab%5D%20OR%20late%5Btiab%5D%20OR%20time%5Btiab%5D%20OR%20timing%5Btiab%5D)&sort=pubdate&sort_order=asc&size=200&page=" + str(
        pg)

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    href = soup.find_all('a', attrs={"class", "docsum-title"})

    while len(href) != 0:

        URL = "https://pubmed.ncbi.nlm.nih.gov/?term=(%22Infant%22%5BMesh%5D%20OR%20%22Infant%2C%20Newborn%22%5BMesh%5D%20OR%20%22Child%22%5BMesh%5D%20OR%20%22Child%2C%20Preschool%22%5BMesh%5D%20OR%20infan*%20OR%20babies%20OR%20baby%20OR%20newborn*%20OR%20neonat*%20OR%20toddler*%20OR%20child*%5Btiab%5D)%20AND%20(%22Weaning%22%5BMesh%5D%20OR%20%22Infant%20Nutritional%20Physiological%20Phenomena%22%5BMesh%5D%20OR%20%22Feeding%20Behavior%22%5BMesh%5D%20OR%20complementary%20feed*%5Btiab%5D%20OR%20complementary%20food*)%20AND%20(introduc*%5Btiab%5D%20OR%20introduction%5Btiab%5D%20OR%20initiation%5Btiab%5D%20OR%20early%5Btiab%5D%20OR%20late%5Btiab%5D%20OR%20time%5Btiab%5D%20OR%20timing%5Btiab%5D)&sort=pubdate&sort_order=asc&size=200&page=" + str(
            pg)

        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        href = soup.find_all('a', attrs={"class", "docsum-title"})

        # sqlSrv_Connect()

        count = 0
        for id in href:
            child_req = requests.get(WEB_URL + href[count].get("href"))
            child_soup = BeautifulSoup(child_req.content, 'html.parser')

            article_main = child_soup.find("main", attrs={"class", "article-details"})
            article_header = article_main.find("header", attrs={"class", "heading"})

            article_button = article_header.find("button", attrs={"class", "journal-actions-trigger trigger"})
            var_article_button = article_button.text.strip()

            article_cit = article_header.find("span", attrs={"class", "cit"})
            var_article_cit = article_cit.text.strip()

            article_heading_title = article_header.find("h1")

            print(article_heading_title.text.strip() + " - " + str(pg) + " - " + href[count].get("href"))

            if article_heading_title is not None:
                var_article_heading_title = article_heading_title.text.strip()
            else:
                var_article_heading_title = ""

                article_author_list = article_header.find("div", attrs={"class", "authors-list"})

                if article_author_list is not None:
                    var_article_author_list = article_author_list.text.strip().replace(",", " -")
                else:
                    var_article_author_list = ""

                article_pmid = article_header.find("ul", attrs={"class", "identifiers"})

                if article_pmid is not None:
                    article_pmid_heading = article_pmid.find("span", attrs={"class", "id-label"})
                    article_pmid_value = article_pmid.find("strong", attrs={"class", "current-id"})
                    var_article_pmid_heading = article_pmid_heading.text.strip() + article_pmid_value.text.strip()
                else:
                    var_article_pmid_heading = ""

                article_abstract = child_soup.find("div", attrs={"class", "abstract"})
                article_abstract = article_abstract.find("p")

                if article_abstract is not None:
                    for data in article_abstract(['p', 'strong']):
                        # Remove tags
                        data.decompose()
                        ' '.join(article_abstract.stripped_strings)
                        var_article_abstract = ' '.join(article_abstract.stripped_strings)
                else:
                    var_article_abstract = ""

                addArticles(var_article_button, var_article_cit, var_article_pmid_heading, var_article_heading_title,
                            var_article_author_list, var_article_abstract)

                count = count + 1
                pg = pg + 1


if __name__ == '__main__':
    deleteOldRecords()
    # scrapArticles_Pg1()
    scrapArticles_Oth_Pg()

    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################

    # arr = []
    # arr = article_abstract.text.strip().split(" ")
    # var_article_abstract = arr[0].strip()

    # for a in range(0, len(arr)):
    #   print(arr[a].strip())

    # article_citation_doi = article_header.find("span", attrs={"class", "citation-doi"})

    # if article_citation_doi != None:
    #   article_citation_doi = article_header.find("span", attrs={"class", "citation-doi"})
    #   article_citation_doi = article_citation_doi.text.strip()
