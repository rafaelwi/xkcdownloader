# xkcdownloader_functions.py
# github: rafaelwi

# Imports
from requests.exceptions import RequestException
from requests import get
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request
import random
import sys


"""Gets the page source of a requested website
Args:
    url: The URL of the page that the source will be taken from
Returns: 
    the source code of the URL passed in
"""
def get_page(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
            log_message('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


"""Checks if the response from the URL is good

Args:
    resp: Respond from website of connection status

Returns: 
    true if a successful connection has been made and false otherwise
"""
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)


"""Prints out the message passed in. Used for debugging

Args:
    m: A message

Returns: 
    the message
"""
def log_message(m):
    print (m)


"""Gets the url and verifies that it is valid

Args:
    args: List of arguements from the command line

Returns: 
    the URL entered
"""
def get_raw_url(args):
    # Check number of args passed in
    # If there is only one argument passed in, download a random
    if len(args) == 1:
        # Get the latest xkcd value
        latest = get_latest()

        # Randomly generate a number
        random_comic = random.randint(1, int(latest))
        raw_url = "https://xkcd.com/" + str(random_comic) + "/"
        log_message ("Got URL: random comic");


    # If there are two arguements
    elif len(args) == 2:
        raw_url = args[1]

        # Verify that the URL is valid
        if (raw_url.split('/')[2] != "xkcd.com") |  (not (raw_url.split('/')[3]).isdecimal()):
            log_message ("Error: URL is formatted incorrectly")
            sys.exit()

        log_message ("Got URL: " + raw_url)
    # Otherwise, if there are more than 2 args, exit
    else:
        log_message ("Usage: python3 main.py <xkcd url>")
        sys.exit()

    return raw_url


"""Gets the image URL from the page of the URL passed in

Args:
    raw_url: URL of page that will be searched

Returns: 
    the URL of the image
"""
def get_img_url(raw_url):
    # Get the page and place into BeautifulSoup object
    raw_html = get_page(raw_url)
    bs4_html = BeautifulSoup(raw_html, 'html.parser')
    log_message("Got page from URL <" + raw_url + ">")

    # Get only the text from bs4_html
    bs4_text = bs4_html.get_text()
    img_url_location = bs4_text.index('Image URL') # 'Image URL is what we are searching for in the text
    bs4_text = bs4_text[img_url_location:]
    bs4_text_list = bs4_text.splitlines()

    # Get line that has the image URL and return it
    img_url_line = bs4_text_list[0]
    img_url = img_url_line.split(' ')[4]

    return img_url


"""Downloads the image located at img_url

Args:
    raw_url: Used for determining filename
    img_url: URL of image to be downloaded

Returns: 
    no value; saves the image that is located at the URL passed in by img_url
"""
def download_img(raw_url, img_url):
    # Create filename
    filename = "imgs/" + raw_url.split('/')[3] + ".png"

    # Download the image
    urllib.request.urlretrieve(img_url, filename)
    log_message ("Saved image from URL <" + raw_url + "> as " + filename)


"""Gets the number of the latest xkcd comic

Returns: 
    the number of the latest xkcd comic
"""
def get_latest():
    # Get the page and place into BeautifulSoup object
    raw_html = get_page("https://xkcd.com/")
    bs4_html = BeautifulSoup(raw_html, 'html.parser')

    # Get only the text from bs4_html
    bs4_text = bs4_html.get_text()
    latest_url_location = bs4_text.index('Permanent')
    bs4_text = bs4_text[latest_url_location:]
    bs4_text_list = bs4_text.splitlines()

    # Get the line that has the image URL and return it
    latest_url_line = bs4_text_list[0]
    latest_value = latest_url_line.split('/')[3]


    # Return the value
    return latest_value

"""Validates that the URL passed from the command line is valid

Args:
    url: URL of the page that contains the xkcd comic

Returns:
    nothing if the comic is valid or exits otherwise
"""
def validate_url (url):
    # Get the latest value for the comic
    latest_comic = get_latest()

    # Get the number from the URL
    comic_value = url.split('/')[3]

    if ((int(comic_value) > int(latest_comic)) | (int(comic_value) <= 0)):
        log_message("Error: Ending execution due to comic not being in valid range")
        sys.exit()
    else:
        return