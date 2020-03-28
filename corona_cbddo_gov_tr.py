from bs4 import BeautifulSoup
from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
import os

from tools import create_folder, download_image_wget


if __name__ == '__main__':

    created_time = datetime.now()
    date = str(created_time).split(" ")[0]

    main_folder_path = os.path.join(os.getcwd(), "datas", "corona_cbddo_gov_tr", date)
    create_folder(main_folder_path)