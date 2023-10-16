from facebook_scraper import get_profile
import requests
import os
import json
import csv


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


def extract_metadata(data, output_file):
    metadata = {
        "Name": data.get("Name", None),
        "Location": next((place['text'] for place in data.get("Places lived", []) if place['type'] == 'Current city'), None),
        "Gender": "Male" if "Male" in data.get("Basic info\nEdit", "") else ("Female" if "Female" in data.get("Basic info\nEdit", "") else None),
        "Place of study": [edu.split("\n")[0] for edu in data.get("Education", "").split("More options") if "Class of" in edu],
        "Groups they belong to": [],  # Not provided in example data
        "Friends": [],  # Not provided in example data
        "Profile and cover images as URIs": {
            # Not provided in example data, placeholders added
            "profile_picture": None,
            "cover_photo": None
        }
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print(f"Metadata saved to {output_file}")


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

        profile = get_profile(uid,cookies="www.facebook.com_cookies.txt")
        print(profile)
        metadata_file = os.path.join(profile_dir, "metadata.json")
        extract_metadata(profile, metadata_file)
        download_images_from_json(profile, profile_dir)
    except Exception as e:
        print(f"An error occurred while processing user ID {uid}: {e}")

print("Processing completed.")
