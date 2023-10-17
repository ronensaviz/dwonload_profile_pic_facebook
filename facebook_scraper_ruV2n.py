import logging

from facebook_scraper import get_profile, get_photos, get_friends
import requests
import os
import csv
import json
import re
from requests_html import HTMLSession

def get_profile_picture(user_id):
    """
    Retrieves the profile picture URL for the provided Facebook user ID.

    :param user_id: The user's Facebook ID.
    :return: The URL of the profile picture or None if not found.
    """
    # Define the URL for the user's profile
    profile_url = f"https://www.facebook.com/profile.php?id={user_id}"

    # Create an HTML Session
    session = HTMLSession()

    # Send a GET request to the profile URL
    response = session.get(profile_url)

    # Ensure the request was successful
    if response.status_code == 200:
        # Find the profile picture element
        profile_picture_elem = response.html.find("i.profpic", first=True)
        if profile_picture_elem:
            style_attr = profile_picture_elem.attrs.get("style")
            match = re.search(r"url\('(.+)'\)", style_attr)
            if match:
                profile_picture_url = match.groups()[0]  # Assuming the URL doesn't need decoding
                return profile_picture_url

    return None  # Return None if no profile picture is found or request failed



def download_images_from_json(data, save_dir):
    image_urls = []
    if "cover_photo" in data:
        image_urls.append(data["cover_photo"])
    if "profile_picture" in data:
        image_urls.append(data["profile_picture"])

    for url in image_urls:
        response = requests.get(url)
        image_name = os.path.join(save_dir, "images", url.split("/")[-1].split("?")[0])
        if not os.path.exists(os.path.dirname(image_name)):
            os.makedirs(os.path.dirname(image_name))
        with open(image_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {image_name}")


def extract_metadata(data, friends,photos, output_file):
    """Extract metadata from profile data and save to a JSON file."""
    metadata = {
        "Name": data.get("Name"),
        "Location": next((item["text"] for item in data.get("Places lived", []) if item["type"] == "Current city"),
                         None),
        "Gender": data.get("Basic info", "").split("\n")[0] if 'Gender' in data.get("Basic info", "") else None,
        "Place of study": list(data.get("Education", {}).values()),
        "Groups they belong to": [],
        "Friends": [friend['id'] for friend in friends],
        "Profile and cover images as URIs": {
            "profile_picture": data.get("profile_picture"),
            "cover_photo": data.get("cover_photo")
        },
        "Photos": [photo['url'] for photo in photos]
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    logging.info(f"Metadata saved to {output_file}")


def get_userids_from_csv(filename):
    userids = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            userids.append(row['userid'])
    return userids


def main():
    base_dir = "profiles_data"
    os.makedirs(base_dir, exist_ok=True)
    userids = get_userids_from_csv('/Users/ronen_saviz/PycharmProjects/dwonload_profile_pic_facebook/input.csv')

    for uid in userids:
        profile_dir = os.path.join(base_dir, uid)
        os.makedirs(profile_dir, exist_ok=True)

        try:
            profile = get_profile(uid, cookies="cookies.txt")
            print(profile)
        except Exception as e:
            logging.error(f"An error occurred while getting profile for user ID {uid}: {e}")
            profile = {}

        # try:
        #     friends = list(get_friends(uid, cookies="cookies.txt"))
        #     print(friends)
        # except Exception as e:
        #     logging.error(f"An error occurred while getting friends for user ID {uid}: {e}")
        #     friends = []

        # try:
        #     photos_gen = get_photos(uid, cookies="cookies.txt")
        #     for photo in photos_gen:
        #         print(photo['url'])
        # except Exception as e:
        #     logging.error(f"An error occurred while getting photos for user ID {uid}: {e}")
        #     photos = []
        profile_picture = get_profile_picture(uid)
        print(profile_picture)
        photos = []
        friends = []
        metadata_file = os.path.join(profile_dir, "metadata.json")
        extract_metadata(profile, friends, photos, metadata_file)

    logging.info("Processing completed.")

if __name__ == "__main__":
    main()