
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
import os

from tools import create_folder, download_image_shutil, download_image_tqdm, download_image_wget



if __name__ == '__main__':

    created_time = datetime.now()
    date = str(created_time).split(" ")[0]

    main_folder_path = os.path.join(os.getcwd(), "images", "covid19_saglik_gov_tr", date)
    create_folder(main_folder_path)

    url = 'https://covid19.saglik.gov.tr/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all("a")

    for rs in results:
        job_elems = rs.find("img", class_='img-fluid')

        if job_elems:
            a_hrf = rs.attrs['href']
            img_url = job_elems.attrs.get("src")
            img_download_url = urljoin(a_hrf, img_url)

            print("img_download_url: {}".format(img_download_url))
            try:
                # download_image_tqdm(main_folder_path, img_download_url)
                # download_image_shutil(main_folder_path, img_download_url)
                download_image_wget(main_folder_path, img_download_url)
            except Exception as e:
                print("Error: {}".format(e))
