import os
from seleniumbase import BaseCase

class FacebookAlbumScraper(BaseCase):
    def test_scrape_facebook_album(self):
        # Define the URL of the Facebook album
        album_url = "https://www.facebook.com/media/set/?set=a.165916470091759&type=3"

        # Specify the path to the chromedriver executable
        chromedriver_path = "/path/to/chromedriver"

        # Load cookies from the 'cookies.txt' file
        self.load_cookies("cookies.txt")

        # Open the album URL with cookies
        self.open(album_url)

        # Check if the request was successful
        if "This content isn't available right now" not in self.get_page_source():
            # Find all image elements using their class (you might need to inspect the page to find the correct class)
            image_elements = self.find_elements("your-image-class")

            # Extract the image URLs from the "src" attribute
            image_urls = [img.get_attribute("src") for img in image_elements]

            # Print the extracted image URLs
            for url in image_urls:
                print(url)
        else:
            print("Failed to fetch the page. Check your cookies or URL.")

    def load_cookies(self, name="cookies.txt"):
        """Loads the page cookies from the specified file path."""
        self.wait_for_ready_state_complete()
        folder = os.path.dirname(name)
        if not folder:
            folder = "."
        abs_folder = os.path.abspath(folder)
        cookies_file_path = os.path.join(abs_folder, os.path.basename(name))
        json_cookies = None
        with open(cookies_file_path, "r") as f:
            for line in f.read().splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    key, value = parts[0], parts[1]
                    self.driver.add_cookie({"name": key, "value": value})

if __name__ == "__main__":
    FacebookAlbumScraper("test_scrape_facebook_album").run()
