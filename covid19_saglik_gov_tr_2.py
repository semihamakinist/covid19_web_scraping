
from bs4 import BeautifulSoup

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
import json
import os


def tuple2dict(tup):
    di = {}
    for k, v in tup:
        di[k] = v
    return di


if __name__ == '__main__':
    url = 'https://covid19.saglik.gov.tr/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(id="bg-logo")
    elems_list = []

    json_file_path = os.path.join(os.getcwd(), 'datas', 'data.json')
    datas = []
    try:
        with open(json_file_path, 'r') as json_file:
            datas = json.load(json_file)
    except Exception as e:
        print("Error: {}".format(e))

    rs = results[0]
    tarih = rs.find("p", class_="p1").text + "-" + rs.find("p", class_="p2").text + "-" + rs.find("p", class_="p3").text

    li_elems_toplam = rs.find_all("li", attrs={"class": "d-flex justify-content-between baslik-k"})
    li_elems_acik = rs.find_all("li", attrs={"class": "d-flex justify-content-between baslik-k-2 bg-acik"})
    li_elems_koyu = rs.find_all("li", attrs={"class": "d-flex justify-content-between baslik-k-2 bg-koyu"})

    li_elems = li_elems_toplam + li_elems_acik + li_elems_koyu
    for li_elem in li_elems:
        li_span_elems = li_elem.find_all("span")
        elems_list.append((li_span_elems[0].text.replace("\r\n", " ").replace("  ", ""),
                           li_span_elems[1].text.replace("\r\n", " ").replace("  ", "")))

    # elems_list.append(("tarih", tarih))
    elems_list.append(("title", rs.find("div", class_='baslik-tablo').text.replace("\n", "")))
    elems_dict = {tarih: tuple2dict(elems_list)}
    print()
    with open(json_file_path, 'w') as outfile:
        outfile.write(json.dumps(elems_dict, sort_keys=True,
                                 ensure_ascii=True, indent=4))

    # canvas = results[1].find(id="canvas")
