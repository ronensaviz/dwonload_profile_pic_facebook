from facebook_scraper import get_profile
import requests
import os
import json


profile = get_profile("100090742053033")
# Or if you have a cookies.txt file to authenticate and bypass certain limitations:
# profile = get_profile("zuck", cookies="cookies.txt")
print(profile)
def download_images_from_json(data, save_dir="downloaded_images"):
    """
    Download images from the provided JSON data.

    :param data: JSON data in the form of a Python dictionary.
    :param save_dir: Directory to save the downloaded images. Default is 'downloaded_images'.
    """

    # Create directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Extract image URLs from the JSON data
    image_urls = []
    if "cover_photo" in data:
        image_urls.append(data["cover_photo"])
    if "profile_picture" in data:
        image_urls.append(data["profile_picture"])

    # Download each image
    for url in image_urls:
        response = requests.get(url)
        # Extract image file name from the URL
        image_name = os.path.join(save_dir, url.split("/")[-1].split("?")[0])  # Removing query parameters
        with open(image_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {image_name}")


def extract_metadata(data, output_file="output_metadata.json"):
    """
    Extracts and saves desired metadata from the given data.

    :param data: A dictionary containing the user's data.
    :param output_file: The name of the JSON file where the extracted metadata will be saved.
    """

    # Extract relevant fields
    metadata = {
        "Name": data.get("Name", None),
        "Location": data.get("מקומות מגורים", None),  # Assuming 'מקומות מגורים' is the key for location
        "Gender": None,  # Gender is not provided in the example data
        "Place of study": data.get("השכלה", None),  # Assuming 'השכלה' is the key for place of study
        "Groups they belong to": None,  # Groups data is not provided in the example data
        "Friends": None,  # Friends data is not provided in the example data
        "Profile and cover images as URIs": {
            "profile_picture": data.get("profile_picture", None),
            "cover_photo": data.get("cover_photo", None)
        }
    }

    # Save the extracted metadata to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print(f"Metadata saved to {output_file}")


extract_metadata(profile)
download_images_from_json(profile)
