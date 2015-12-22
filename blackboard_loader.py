
import urllib.request
import urllib.parse
import bs4
from mimetypes import guess_extension
from documents import pdfFile

################################################
# Functions
################################################


def login_bb(user_id, user_passwd):
    authentication_url = 'https://blackboard.aber.ac.uk/webapps/login/'
    payload = {
        'op': 'login',
        'user_id': user_id,
        'password': user_passwd
    }
    data = urllib.parse.urlencode(payload)
    binary_data = data.encode('UTF-8')
    req = urllib.request.Request(authentication_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = resp.read()


def download_pdf(file_to_get):

    source = urllib.request.urlopen(file_to_get.get_url())
    extension = guess_extension(source.info()['Content-Type'])
    app_name = "default.pdf"

    if extension:
        app_name = file_to_get.get_name()
        file = open(app_name, 'wb')
        file.write(source.read())
        file.close()
    else:
        file = open('test.pdf', 'wb')
        file.write(source.read())
        file.close()

    #print("I think it worked")


#This will print the links which have "pdf" specified in the naming
def get_links(url):
    site = urllib.request.urlopen(url)
    html = site.read()

    # parse the html
    soup = bs4.BeautifulSoup(html, 'html.parser')

    data = soup.find_all(id='content')

    #container for the docs
    documents = []


    for div in data:
        links = div.find_all('a')
        for a in links:
            if'pdf' in a.text:
                temp_doc = pdfFile()
                temp_doc.set_name(a.text)
                temp_doc.set_url('https://blackboard.aber.ac.uk' + a['href'])
                documents.append(temp_doc)

    return documents
