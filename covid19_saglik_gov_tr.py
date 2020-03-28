
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
import os


def create_folder(folder_path):
    print(os.path.exists(folder_path))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return True
    return False


def download_image(pathname, img_url):
    response = requests.get(img_url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, img_url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    buffer_size = 1024
    progress = tqdm(response.iter_content(buffer_size),
                    f"Downloading {filename}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


if __name__ == '__main__':

    created_time = datetime.now()
    date = str(created_time).split(" ")[0]

    main_folder_path = os.path.join(os.getcwd(), "images", date)
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
            #download_image(main_folder_path, img_download_url)

