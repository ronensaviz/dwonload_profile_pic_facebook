import logging

from facebook_scraper import get_profile, get_photos, get_friends
import requests
import os
import json
import csv




def download_photos(user_id, save_dir, cookies_path=None):
    """
    Download photos of a specified Facebook user.

    :param user_id: Facebook username or user ID.
    :param save_dir: Directory where photos will be saved.
    :param cookies_path: Path to cookies file (optional).
    """
    photos_dir = os.path.join(save_dir, "photos")  # Create a new 'photos' directory inside save_dir
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)

    # Fetch photos using the get_photos function
    photos = get_photos(user_id, cookies=cookies_path)

    # Download each photo
    for photo in photos:
        try:
            response = requests.get(photo['url'])
            image_name = os.path.join(photos_dir, photo['url'].split("/")[-1].split("?")[0])  # Save inside photos_dir
            with open(image_name, 'wb') as file:
                file.write(response.content)
            logging.info(f"Downloaded {photo['url']} to {image_name}")
        except Exception as e:
            logging.error(f"An error occurred while downloading {photo['url']}: {e}")

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


def extract_metadata(data, friends, output_file):
    """Extract metadata from profile data and save to a JSON file."""
    metadata = {
        "Name": data.get("Name"),
        "Location": next((item["text"] for item in data.get("Places lived", []) if item["type"] == "Current city"), None),
        "Gender": data.get("Basic info", "").split("\n")[0] if 'Gender' in data.get("Basic info", "") else None,
        "Place of study": list(data.get("Education", {}).values()),
        "Groups they belong to": [],
        "Friends": [friend['id'] for friend in friends],
        "Profile and cover images as URIs": {
            "profile_picture": data.get("profile_picture"),
            "cover_photo": data.get("cover_photo")
        }
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


base_dir = "profiles_data"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

userids = get_userids_from_csv('/Users/ronen_saviz/PycharmProjects/dwonload_profile_pic_facebook/input.csv')

for uid in userids:
    try:
        profile_dir = os.path.join(base_dir, uid)
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)

        try:
            profile = get_profile(uid, cookies="cookies.txt")
            print(profile)
        except Exception as e:
            logging.warning(f"An error occurred while getting profile for user ID {uid}: {e}")
            profile = {}

        # try:
        #     friends = list(get_friends(uid, cookies="cookies.txt"))
        # except Exception as e:
        #     logging.warning(f"An error occurred while getting friends for user ID {uid}: {e}")
        #     friends = []

        #
        # metadata_file = os.path.join(profile_dir, "metadata.json")
        # extract_metadata(profile,friends, metadata_file)
        # download_images_from_json(profile, profile_dir)
    except Exception as e:
        print(f"An error occurred while processing user ID {uid}: {e}")

print("Processing completed.")