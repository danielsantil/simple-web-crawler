from xmlrpc import client
from threading import Thread
from selenium import webdriver
from bs4 import BeautifulSoup

def launch_worker():
    thread_get_work = Thread(target = get_work)
    thread_get_work.start()

def get_work():
    work = ''
    try:
        server = client.ServerProxy('http://localhost:9080/server')
        work = server.GetWork()
    except:
        print('Error occurred trying to get work. Is server up?')
        exit(0)

    if work == 'Empty':
        print('Chill!')
        exit(0)
    params = work.split('|')
    root_url = params[0]
    search = params[1]
    max_depth = int(params[2])
    current_depth = int(params[3])
    print(f'Working with: {work}')

    site_html = parse_html(root_url)
    text_nodes = get_text_elements(site_html)
    matches = filter_nodes(text_nodes, search)

    print(f'Found {len(matches)} ocurrences')
    write_thread = Thread(target = write_file, args = (matches, 'results.txt'))
    write_thread.start()

    if current_depth < max_depth:
        find_in_depth_thread = Thread(target = find_in_depth, args = (site_html, root_url, max_depth, current_depth))
        find_in_depth_thread.start()

def parse_html(root_url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path = './chromedriver', chrome_options = options)
    driver.get(root_url)
    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    return html

def get_text_elements(html):
    tags_list = ['p', 'div', 'title', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'span', 'pre', 'li']
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(tags_list)
    return elements

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    hrefs = []
    for tag in a_tags:
        href = tag.get('href')
        if is_href_valid(href):
            hrefs.append(href)
    return hrefs

def filter_nodes(text_nodes, search):
    matches = []
    for node in text_nodes:
        if search in node.get_text():
            matches.append(' '.join(node.get_text().splitlines()))
    return matches

def write_file(result_list, file_name):
    with open(file_name, 'a') as f:
        for result in result_list:
            f.write(f'{result}\n\n---------------\n\n')

def is_href_valid(href):
    if href and href != '/' and href != '#':
        return href.startswith(('/', 'http'))
    return False

def filter_links(links, root_url):
    links = list(set(links))
    return [(root_url + href) if href.startswith('/') else href for href in links]

def find_in_depth(site_html, root_url, max_depth, current_depth):
    links = get_links(site_html)
    links = filter_links(links, root_url)
    current_depth = current_depth + 1
    for link in links:
        server = client.ServerProxy('http://localhost:9080/server')
        server.PutWork(link, 'PUCMM', max_depth, current_depth)
        launch_worker()

launch_worker()