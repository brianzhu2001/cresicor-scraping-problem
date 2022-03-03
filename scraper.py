from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import urlparse, urljoin

from os import makedirs

def __main__(url, directory):
	# fetch webpage
	response = request.urlopen(url)
	webpage = response.read().decode('UTF-8')

	# get all link urls ending in .pdf
	soup = BeautifulSoup(webpage, 'html.parser')
	pdf_urls = [tag.get('href') for tag in soup.find_all('a') if tag.get('href')[-4:] == '.pdf']

	# resolve relative urls
	pdf_urls = [urljoin(url, link) for link in pdf_urls]

	makedirs(directory, exist_ok=True)
	for pdf_url in pdf_urls:
		response_ = request.urlopen(pdf_url)
		path = urlparse(pdf_url).path
		with open(directory + path[(path.rfind('/')+1):], 'wb') as file:
			_ = file.write(response_.read())

url = 'https://cms.math.ca/competitions/cmo/'
directory = './Math Problems/'

__main__(url, directory)