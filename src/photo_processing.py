import requests
import time
import psycopg2

class photo_processing:
    def __init__(self, HOST, NAME_USER, PASSWORD, DATABASE, CONNECT, path, url):
        self.host = HOST
        self.name_user = NAME_USER
        self.password = PASSWORD
        self.database = DATABASE
        self.connect = CONNECT
        self.path_to_images = path
        self.url = url

    def save_photo(self):
        connection = psycopg2.connect(host=self.host, user=self.name_user, password=self.password, database=self.database)
        connection.autocommit = True
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                with

        except Exception as e:
            print(f"Ошибка: {e}")