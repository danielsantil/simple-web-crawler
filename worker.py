from xmlrpc import client
from threading import Thread
from selenium import webdriver
from bs4 import BeautifulSoup

server = client.ServerProxy('http://localhost:9080/server')

def get_work():
    work = server.GetWork()
    if work == 'Empty':
        print('Chill!')
        exit(0)

    params = work.split('|')
    url = params[0]
    search = params[1]
    max_depth = int(params[2])
    current_depth = int(params[3])
    print(f'Working with: {work}')

    site_html = parse_html(url)
    text_nodes = get_text_elements(site_html)
    matches = filter_nodes(text_nodes, search)

    for m in matches:
        write_file(m)

def parse_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path = './chromedriver', chrome_options = options)
    driver.get(url)
    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    return html

def get_text_elements(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags_list = ['p', 'div', 'title', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'span', 'pre', 'li']

    elements = soup.find_all(tags_list)
    return elements

def filter_nodes(text_nodes, search):
    matches = []
    for node in text_nodes:
        if search in node.get_text():
            matches.append(' '.join(node.get_text().splitlines()))
    return matches

def write_file(result):
    with open('results.txt', 'a') as f:
        f.write(f'{result}\n\n---------------\n\n')


thread_get_work = Thread(target = get_work)
thread_get_work.start()