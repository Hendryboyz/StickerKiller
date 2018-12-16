import requests
import sys
import re
import os
from PIL import Image
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) == 1:
        print("ERROR : Sticker not found")
        return
    
    sticker_id = sys.argv[1]
    sticker_url = 'https://store.line.me/stickershop/product/' + sticker_id + '/zh-Hant'
    firefox_headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'store.line.me',
        'TE': 'Trailers',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    }
    r = requests.get(sticker_url, headers = firefox_headers)
    
    store_path = create_storage_directory(sticker_id)
    soup = BeautifulSoup(r.text, 'html.parser')

    images_span = soup.find_all("span", attrs={"class": "mdCMN09Image"})
    image_index = 1
    for image in images_span:
        match = re.search(r"https:.*\.png", image['style'], re.M)
        download_image(match.group(0), 'image' + str(image_index), store_path)
        image_index += 1

def create_storage_directory(directory_name):
    directory_path = "./" + directory_name
    if (os.path.isdir(directory_path)):
        remove_directory(directory_path)
    os.mkdir(directory_path)
    return directory_path
        

def remove_directory(directory_path):
    for file in os.listdir(directory_path): 
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(directory_path)

def download_image(image_url, image_index, store_path):
    file_path = os.path.join(store_path, image_index + '.png')
    print(file_path)

    with open(file_path, 'wb') as handle:
        response = requests.get(image_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    print(image_url + ' - OK')

if __name__ == '__main__':
    main()
