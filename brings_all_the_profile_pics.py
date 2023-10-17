import json
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

def download_image(image_url, download_folder):
    local_filename = image_url.split('/')[-1].split("?")[0]  # Extract the filename from the URL
    local_filepath = Path(download_folder) / local_filename
    with requests.get(image_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filepath

def parse_netscape_cookie_file(file_path):
    cookies = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip() != '':
                fields = line.strip().split('\t')
                cookie = {
                    'name': fields[5],
                    'value': fields[6],
                    'domain': fields[0],
                    'path': fields[2],
                    'expires': int(fields[4]),
                    'httpOnly': False,
                    'secure': fields[3] == 'TRUE'
                }
                cookies.append(cookie)
    return cookies


def run(playwright, cookies):
    browser = playwright.chromium.launch(headless=False)  # Set headless=True for headless mode
    context = browser.new_context()

    # Add cookies to the context
    if cookies:
        context.add_cookies(cookies)

    # Navigate to the specific URL
    page = context.new_page()
    page.goto("https://www.facebook.com/media/set/?set=a.153286598029132&type=3", wait_until="networkidle")  # Wait for network idle

    # Wait for the specific image elements to be available in the DOM
    # This ensures that the images and their content are loaded
    page.wait_for_selector("img.x1rg5ohu.x5yr21d.xl1xv1r.xh8yej3", state="attached")  # Adjust the selector if needed

    # Find all image elements with the specific class and extract their src attributes
    image_elements = page.query_selector_all("css=img.x1rg5ohu.x5yr21d.xl1xv1r.xh8yej3")  # This selects all <img> elements with the specified classes
    image_urls = [image_element.get_attribute("src") for image_element in image_elements]

    # Print or process the image URLs as needed
    for url in image_urls:
        print(url)

    # Close the browser
    browser.close()




# Run the script
with sync_playwright() as playwright:
    file_path = '/Users/ronen_saviz/PycharmProjects/dwonload_profile_pic_facebook/cookies.txt'
    cookies = parse_netscape_cookie_file(file_path)  # Parse the cookies
    run(playwright, cookies)  # Pass the cookies to the run function
