import requests
from bs4 import BeautifulSoup

# [Description]
# Returns a list of urls formatted as a string
# If payload is specified, page_num value is ignored.
#
# [Inputs]
# page_num : INT -> page id of plants
# payLoad : HTTP Response code -> 1xx, 2xx, ..., 5xx
def get_images_by_page(page_num=None, payload=None):
	if payload is None:
		target = 'https://calscape.org/photos/{0}'.format(page_num)
		payload = requests.get(target)

	soup = BeautifulSoup(payload.text, 'lxml')
	divs = soup.find_all(class_='big_image hide')

	image_urls = ['http:' + url.find('img')['src'] for url in divs]
	
	return image_urls

# [Description]
# Downloads an image located at the specified resource location.
#
# [Inputs]
# url : STRING -> specific resource location
# path : STRING -> location to be saved at
def download_image(url, path):
	with requests.get(url, stream=True) as r:
		with open(path, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)

# [Description]
# Gets name of plant by page num
# If payload is specified, page_num value is ignored.
#
# [!!!WARNINGS!!!] 
# Could possibly could return a blank name!
#
# [Inputs]
# page_num : INT -> page id of plant
def get_name_for_images(page_num=None, payload=None):
	if payload is None:
		target = 'https://calscape.org/photos/{0}'.format(page_num)
		payload = requests.get(target)
	
	soup = BeautifulSoup(payload.text, 'lxml')
	header = soup.find('h2')

	return header.contents[0][14:]

print(len(get_images_by_page(page_num=10)))
print(len(get_images_by_page(payload=requests.get('https://calscape.org/photos/10'))))