import os
import requests
import json
from lxml import etree


def getDownloadUrls():
    with open('./data.json', 'r') as f:
      movies_info = json.load(f)
      return movies_info['items']



def downloadAndSave(image_path, image_addr):
  headers = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
  }
  image_data = requests.get(image_addr, headers=headers).content
  with open(image_path, "wb+") as f:
    f.write(image_data)


def downloadSource(urls):
    for item in urls:
      url = item['content'][0]['url']
      db_id = item['id']
      title = item['page']
      # 内容
      suffix = url.split(".")[-1]
      image_path = "./pptImages/" + db_id + "_" + str(title) + '.' + suffix
      # 封面
      poster_url = item['content'][0]['poster']
      poster_path = "./pptImages/" + db_id + "_poster_" + str(title) + '.' + poster_url.split('.')[-1]
      downloadAndSave(image_path, url)
      downloadAndSave(poster_path, poster_url)
      with open("./pptImages.txt", "ab+") as f:
        tmp_data = str(image_path) + '|' + str(poster_path) + "\n"
        f.write(tmp_data.encode("utf-8"))
      print('current download:' + image_path)

def main():


    urls = getDownloadUrls()

    if os.path.isfile("./pptImages.txt"):
        os.remove("./pptImages.txt")


    if os.path.exists("./pptImages/"):
      pass
    else:
      os.makedirs("./pptImages/")

    downloadSource(urls)
    
    print('download finish enjoy.')

if __name__ == '__main__':
    main()
