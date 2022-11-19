# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.


#     https://mytools.gatewayedi.com/LogOn



if __name__ == '__main__':
    # URL = "https://www.geeksforgeeks.org/data-structures/"

    WEB_URL = "https://pubmed.ncbi.nlm.nih.gov"

    URL = "https://pubmed.ncbi.nlm.nih.gov/?term=%28%22Infant%22%5BMesh%5D+OR+%22Infant%2C+Newborn%22%5BMesh%5D+OR+%22Child%22%5BMesh%5D+OR+%22Child%2C+Preschool%22%5BMesh%5D+OR+infan*+OR+babies+OR+baby+OR+newborn*+OR+neonat*+OR+toddler*+OR+child*%5Btiab%5D%29+AND+%28%22Weaning%22%5BMesh%5D+OR+%22Infant+Nutritional+Physiological+Phenomena%22%5BMesh%5D+OR+%22Feeding+Behavior%22%5BMesh%5D+OR+complementary+feed*%5Btiab%5D+OR+complementary+food*%29+AND+%28introduc*%5Btiab%5D+OR+introduction%5Btiab%5D+OR+initiation%5Btiab%5D+OR+early%5Btiab%5D+OR+late%5Btiab%5D+OR+time%5Btiab%5D+OR+timing%5Btiab%5D%29&sort=pubdate&sort_order=asc&size=200"

    r = requests.get(URL)

    # soup = BeautifulSoup(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

    soup = BeautifulSoup(r.content, 'html.parser')

    arr_datas = []  # a list to store quotes
    # get all tags
    # tbl = {tag.name for tag in soup.find_all()}

    # iterate all tags

    articles = soup.find_all('article')

    for article in articles:
        # find all element of tag
        # row = article.find_all("a")
        # row1 = row.find_all("a", attrs={"class", "docsum-title"}).get("href")
        # arr_data = {}
        # arr_data['url'] = row.href

        # print(article.find_all("a", attrs={"class", "docsum-title"}))

        input_tag = article.find("a", attrs={"class", "docsum-title"})

        # print(WEB_URL + input_tag["href"])

        child_journal = requests.get(WEB_URL + input_tag["href"])
        child_soup = BeautifulSoup(child_journal.content, 'html.parser')

        btn_nme = child_soup.find("header", attrs={"class", "heading"})
        journal_name = btn_nme.find("button")
        journal_no = btn_nme.find("span", attrs={"class", "cit"})

        JOURNAL_YR_NO = journal_name.text + journal_no.text

        JOURNAL_HEADING = child_soup.find("h1", attrs={"class", "heading-title"})

        author = child_soup.find("div", attrs={"class", "authors-list"})

        for lst_author in author:
            lst = author.find("a", attrs={"class", "full-name"})

            print(lst.get("data-ga-label"))

        print(JOURNAL_YR_NO.strip(""))
        print(JOURNAL_HEADING.text.strip(""))
        print(author)
        exit(0)

'''
for href in article.find_all("a", attrs={"class", "docsum-title"}):
    val1 = href.find_all("a")

    arr_data = {}
    arr_data["href"] = href.href
    arr_datas.append(arr_data)            

    print(val1)
    
    '''

''' for row in soup.find("a", attrs={"class", "docsum-title"}):
    arr_data = {}
# arr_data['url'] = row.href
# arr_datas.append(arr_data)
print(row.text)

'''

# url_article = requests.get(WEB_URL + s)

# exit(0)

# if len(i['class']) != 0: class_list.add(" ".join(i['class']))

# print(class_list)

# for row in table.findAll("div", "class"): quote = {}
# quote['theme'] = row.
# quote['url'] = row.a['href']
# quote['img'] = row.img['src']
# quote['lines'] = row.img['alt'].split(" #")[0]
# quote['author'] = row.img['alt'].split(" #")[1]
# quotes.append(quote)
