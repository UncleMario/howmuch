import json
import os
import time
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError

def download_picture(query, path='howmuch/media/downloads'):
  """Download full size images from Google image search.

  Don't print or republish images without permission.
  I used this to train a learning algorithm.
  """
  images = []

  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + '&start=%d'

  BASE_PATH = os.path.join(path, query)

  if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

  start = 0 # Google's start query string parameter for pagination.
  while start < 1: # Google will only return a max of 56 results.
    r = requests.get(BASE_URL % start)
    for image_info in json.loads(r.text)['responseData']['results']:
      url = image_info['unescapedUrl']
      try:
        image_r = requests.get(url)
      except ConnectionError, e:
        print 'could not download %s' % url
        continue

      # Remove file-system path characters from name.
      title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '')

      file = open(os.path.join(BASE_PATH, '%s.jpg') % title, 'w')
      try:
        Image.open(StringIO(image_r.content)).save(file, 'JPEG')
      except IOError, e:
        # Throw away some gifs...blegh.
        print 'could not save %s' % url
        continue
      finally:
        images.append(file)

    start += 1 # 4 images per page.

    # Be nice to Google and they'll be nice back :)
    time.sleep(1.5)

  return images

