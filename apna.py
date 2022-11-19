import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # URL = "https://www.geeksforgeeks.org/data-structures/"

    WEB_URL = "https://pubmed.ncbi.nlm.nih.gov"

    URL = "https://pubmed.ncbi.nlm.nih.gov/?term=%28%22Infant%22%5BMesh%5D+OR+%22Infant%2C+Newborn%22%5BMesh%5D+OR+%22Child%22%5BMesh%5D+OR+%22Child%2C+Preschool%22%5BMesh%5D+OR+infan*+OR+babies+OR+baby+OR+newborn*+OR+neonat*+OR+toddler*+OR+child*%5Btiab%5D%29+AND+%28%22Weaning%22%5BMesh%5D+OR+%22Infant+Nutritional+Physiological+Phenomena%22%5BMesh%5D+OR+%22Feeding+Behavior%22%5BMesh%5D+OR+complementary+feed*%5Btiab%5D+OR+complementary+food*%29+AND+%28introduc*%5Btiab%5D+OR+introduction%5Btiab%5D+OR+initiation%5Btiab%5D+OR+early%5Btiab%5D+OR+late%5Btiab%5D+OR+time%5Btiab%5D+OR+timing%5Btiab%5D%29&sort=pubdate&sort_order=asc&size=200"

    r = requests.get(URL)

    # soup = BeautifulSoup(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

    soup = BeautifulSoup(r.content, 'html.parser')

