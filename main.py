from pyrogram import Client, errors
import time
import datetime
from random import randint, uniform
import cv2
import numpy as np
from flask import Flask

app = Flask(__name__)


api_id = 26541817
api_hash = "192aa1d108342022bee4cb45e6a6be7e"
image_dir = 'C:/Users/Computer/PycharmProjects/pythonProject1/gen'
num_images = 100
ADDITIONAL_WAIT_TIME = 100



def generate_images(num_images, size=300, random_range=(220, 255)):
    image_paths = []
    for i in range(num_images):
        random_int = randint(random_range[0], random_range[1])
        img = np.random.randint(random_int, size=(size, size, 3), dtype=np.uint8)
        image_path = f'C:/Users/Computer/PycharmProjects/pythonProject1/gen/image-{i}.png'
        cv2.imwrite(image_path, img)
        image_paths.append(image_path)
        print(f"Image {i} generated and saved.")
    return image_paths



image_paths = generate_images(num_images)


def set_profile_photo_with_retry(app, image_path, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            app.set_profile_photo(photo=image_path)
            print("Profile photo updated successfully.")
            return True
        except errors.FloodWait as e:
            wait_seconds = e.value + ADDITIONAL_WAIT_TIME
            print(f"FloodWait detected (attempt {retries + 1}). Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
            retries += 1
        except Exception as e:
            print(f"An error occurred during photo update: {e}")
            return False
    print("Maximum retries reached for profile photo update. Skipping.")
    return False


@app.route("/")
def main():
    with Client("my_account", api_id, api_hash) as app:
        while True:
            time.sleep(3)
            time_sleep = uniform(124, 194)
            current_time = datetime.datetime.now().time()
            print("Start cycle...")

            random_ava = randint(0, num_images - 1)
            image_path = image_paths[random_ava]

            if set_profile_photo_with_retry(app, image_path):
                print("Task completed successfully")
            else:
                print("Failed to update profile photo")

            print(f"Wait {time_sleep:.2f} seconds. Time: {current_time}")
            time.sleep(time_sleep)

    return "Bot is running", 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
