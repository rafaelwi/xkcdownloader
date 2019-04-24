# xkcd comic scraper
# github: rafaelwi

# Imports
import sys
import functs as xkcd

"""
    Main Program
"""
# Get raw URL
raw_url = xkcd.get_raw_url(sys.argv)

# Get image URL
img_url = xkcd.get_img_url(raw_url)

# Download image
xkcd.download_img(raw_url, img_url)