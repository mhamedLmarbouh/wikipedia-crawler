import requests
from bs4 import BeautifulSoup
from urllib import parse
import argparse
from validator import url as validate_url
from webpage_gen import write_pages

articls = list()


def main():
    global articls
    parser = setup_parser()
    parsed = parser.parse_args()
    
    start_url, target_url= urls(parsed.start,parsed.target)
    maxp=parsed.maxp
    crawl_wikipidia(start_url,target_url,maxp)
    write_pages(articls)
    print('Done!')

def urls(start,target):
    if validate_url(start) and validate_url(target) and 'wikipedia' in start and 'wikipedia' in target
        start_url = urlparse(start).path[1:]
        target_url = urlparse(target).path[1:]
        return start_url,target_url
    else:
        print('invalide urls')
        exit()


def crawl_wikipidia(url, target_url,maxp):
    global articls
    wikipidia_base = 'https://en.wikipedia.org/'
    url = parse.urljoin(wikipidia_base, url)
    counter=1
    
    while continue_to_crawle(url) and len(articls)!=maxp:
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
    
    print("Done")


def continue_to_crawle(url):
    """
    this function decides if we should continue to crawle or not
    """
    global articls
    ctc=True
    if url == target_url:
        print('Success :\n\ttarget page \'{}\' reached after crawling ({}) pages\n\tall visited urls are in pages.html'.format(target_url, len(articls)))
        articls.append(['target',target_url])
        ctc= False
    for articl in articls:
        if url == articl[1]:
            print('Error: Page Visited twice :\n\turl {} was already visited'.format(url))
            ctc= False
            break
    else:
        ctc= True
    
    return ctc


def get_first_url(soup):
    """
    this function fetchs the 1st url in a wikipidia page 
    """
    global wikipidia_base
    try:
        content=soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p')
        for sp in soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p').find_all('span'):
            sp.decompose()
        for sp in soup.find(id='mw-content-text').find(class_='mw-parser-output').find('p').find_all('sup'):
            sp.decompose()
        url=content.a.get('href')
        return parse.urljoin(wikipidia_base, url)
    except AttributeError:
        print('Dead-end page reached before getting to target page')
        print('\tall visited urls are in pages.html')
        write_pages()
        exit(-1)



def setup_parser():
    """
    this methose setup the argparser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start',
        required=True,
        help='wikipidia page url to start with',
        type=str
    )
    parser.add_argument(
        '--target',
        required=True,
        help='wikipidia page url to stop at',
        type=str
    )
    parser.add_argument(
        '--maxp',
        required=False,
        help='maximum of visited pages to stop at if target not reached\ndefault is 100\n enter -1 for no limits',
        type=int,
        default=100
    )
    return parser


if __name__ == "__main__":
    main()

