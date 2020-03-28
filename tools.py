
import requests
import shutil
import wget
import tqdm
import os


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return True
    return False


def download_image_tqdm(pathname, img_url):
    # download the body of response by chunk, not immediately
    response = requests.get(img_url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, img_url.split("/")[-1])
    # read 1024 bytes every time
    buffer_size = 1024
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    del response


def download_image_shutil(pathname, img_url):
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(img_url, stream=True)
    # Open a local file with wb ( write binary ) permission.

    filename = os.path.join(pathname, img_url.split("/")[-1])
    local_file = open(filename, 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp


def download_image_wget(pathname, img_url):
    local_file = wget.download(img_url, out=pathname)
    print("local_file: {}".format(local_file))
