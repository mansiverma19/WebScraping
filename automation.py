# web scraping using requests beautiful soup and html5lib
# step 1- all requirements
import shutil
import requests
from bs4 import BeautifulSoup
import random
import os

# step 2- get the html file from server
url = "https://www.bedtimeshortstories.com/"
r = requests.get(url)
html_content = r.content

# step 3- parse the html file
soup = BeautifulSoup(html_content, 'html.parser')

# step 4- tree traversal
title = soup.title

para = soup.find('p')
# print(para)
# print(soup.find_all("p", class_="menu-item"))

all_links = set()
table = soup.find('div', attrs={'class': 'menu-sidebar-all-categories-container'})
link = set()
for i in table.find_all('a'):
    if i.has_attr('href'):
        link.add(i.attrs['href'])
# print(link)
n_list = list(link)
n = int(len(link))
req_link = n_list[random.randint(0, n-1)]
print(req_link)

# entering new link
next_url = req_link
r1 = requests.get(next_url)
next_html_content = r1.content
soup1 = BeautifulSoup(next_html_content, 'html.parser')
# print(soup1.prettify())

table1 = soup1.find('h2', attrs={'class': 'title'})
link1 = set()
for i in table1.find_all('a'):
    if i.has_attr('href'):
        link1.add(i.attrs['href'])
print(link1)
slink = list(link1)
req_link1 = slink[0]
print(req_link1)

# file which contain links
with open("file_links.txt", 'w') as f:
    f.write(req_link1)
story_url = req_link1
s = requests.get(story_url)
story_html_content = s.content
soup2 = BeautifulSoup(story_html_content, 'html.parser')
# print(soup2.prettify())

# creating a folder
folder_list = ['Story and Image', 'ALL TITLE']
path = "D:/WEB_SCRAPING"
if not os.path.exists(path):
    for folder in folder_list:
        os.makedirs(os.path.join(path, folder))

# story paragraph
story_text = soup2.find('div', attrs={'class': 'single-content'})
st = []
for i in story_text.find_all('h4'):
    st.append(i.get_text('h4'))
print(st)

# getting the story title
title = soup2.find('div', attrs={'class': 'post-content'})
for i in title.find_all('h2'):
    s_title = i.get_text('h2')
print(s_title)

# gets the image link
img_link = soup2.find('div', attrs={'class': 'wp-caption aligncenter'})
img_url = []
for i in img_link.find_all('a'):
    if i.has_attr('href'):
        img_url.append(i.attrs['href'])
print(img_url)

# creating text file
path1 = "D:/WEB_SCRAPING/Story and Image"
completeName = os.path.join(path1, s_title+".txt")
with open(completeName, "w") as file1:
    file1.write(str(st))

# image downloading
response = requests.get(str(img_url[0]), stream=True)   
file = open(path1+s_title+".png", "wb")
response.row_decode_content = True
shutil.copyfileobj(response.raw, file)
del response
file.close()