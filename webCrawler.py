import requests
from bs4 import BeautifulSoup
import urllib
import time
import sys


start_url = "wiki/Python_(programming_language)"
target_url = "https://en.wikipedia.org/wiki/Philosophy"
wikipidia_base = "https://en.wikipedia.org/"
articls = []


def crawl_wikipidia(url):
    url = urllib.parse.urljoin(wikipidia_base, url)
    counter=1
    while continue_to_crawle(url):
        print(counter,url)
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            title=soup.title.text
            articls.append([title,url])
            url = get_first_url(soup)
        else:
            print('Error {} while trying to access page {}'.format(html.status_code,url))
            exit(-1)
        counter+=1
        #time.sleep(1) 
    print("Done")


def continue_to_crawle(url):
    if len(articls)==100:
        write_pages()
        exit(-1)
    elif url == target_url:
        print('Success :\n\ttarget page \'{}\' reached after crawling ({}) pages\n\tall visited urls are in pages.html'.format(target_url, len(articls)))
        articls.append(['target',target_url])
        write_pages()
        return False
    for articl in articls:
        if url == articl[1]:
            print('Error: Page Visited twice :\n\turl {} was already visited'.format(url))
            write_pages()
            return False
    else:
        return True


def get_first_url(soup):
    try:
        content=soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p')
        for sp in soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p').find_all('span'):
            sp.decompose()
        for sp in soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p').find_all('sup'):
            sp.decompose()
        url=content.a.get('href')
        return urllib.parse.urljoin(wikipidia_base, url)
    except AttributeError:
        print('Dead-end page reached before getting to target page')
        print('\tall visited urls are in pages.html')
        write_pages()
        exit(-1)


def write_pages():
    with open('pages.html', 'w') as output:
        html_begin = '''
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <title>Visited pages</title>
            </head>
            <body>
            <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Page</th>
                </tr>
            </thead>
            <tbody>'''
        html_end = '''</tbody></table></body></html>'''
        tb_contet=fill_table()
        print(html_begin+tb_contet+html_end,file=output,end='')
        #output.write(html_begin+tb_contet+html_end)

def fill_table():
    print('fill_table')
    content=''
    for counter,articl in enumerate (articls):
        content+='<tr><th scope="row">{0}</th><td><a href="{2}">{1}</a></td></tr>'.format(counter,articl[0],articl[1])
    return content



crawl_wikipidia(start_url)

