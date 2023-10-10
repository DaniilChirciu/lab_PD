import os
import requests
from bs4 import BeautifulSoup

# функция для создания папок
def create_folder(classes):
    for class_name in classes:
        folder_name = f"dataset/{class_name}"
        os.makedirs(folder_name, exist_ok = True)

# функция для загрузки изображений
def download_img(query, class_name, num_images = 5):
    base_url = "https://yandex.ru/images/search"
    params = {"text": query, "type": "photo", "img_url": "true"}

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img", class_="serp-item__thumb")

    for i, img_tag in enumerate(img_tags[:num_images]):
        img_url = img_tag["src"]

        if not img_url.startswith("http"):
            img_url = "https:" + img_url

        img_data = requests.get(img_url).content
        filename = f"dataset/{class_name}/{str(i).zfill(4)}.jpg"

        with open(filename, "wb") as f:
            f.write(img_data)

# основная функция
def main():
    classes = ["rose", "tulip"]

    create_folder(classes)

    for class_name in classes:
        query = class_name.replace("_", " ")
        download_img(query, class_name, num_images = 5)

if __name__ == "__main__":
    main()