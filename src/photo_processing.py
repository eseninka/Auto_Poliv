import requests
import psycopg2
from torchvision import datasets, transforms
import torch
from PIL import Image

class photo_processing:
    def __init__(self, HOST, NAME_USER, PASSWORD, DATABASE, CONNECT, url, uuid, model):
        self.host = HOST
        self.name_user = NAME_USER
        self.password = PASSWORD
        self.database = DATABASE
        self.connect = CONNECT
        self.url = url
        self.uuid = uuid
        self.model = model

    def save_photo(self):
        connection = psycopg2.connect(host=self.host, user=self.name_user, password=self.password,
                                      database=self.database)
        connection.autocommit = True
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                with connection.cursor() as cursor:
                    cursor.execute('select cam_id from cam where uuid=%s', (self.uuid,))
                    fet = cursor.fetchone()
                    id_cam = fet if fet else 0
                    if id_cam == 0:
                        cursor.execute('insert into cam(uuid) values (%s)', (self.uuid,))
                    cursor.execute('insert into images(image_data, cam_id) values (%s, %s)', (response.content, id_cam))
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            if connection:
                connection.close()
                print('info: коннект закрыт')

    def analiz_image(self):
        connection = psycopg2.connect(host=self.host, user=self.name_user, password=self.password,
                                      database=self.database)
        connection.autocommit = True
        dir = r"C:\Users\kisti\Downloads\archive (1)\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train"

        try:
            with connection.cursor() as cursor:
                cursor.execute('select cam_id from cam where uuid=%s', (self.uuid,))
                id_cam = cursor.fetchone()
                cursor.execute('select image_data from cam where id_cam=%s order by image_id desc', (str(id_cam),))
                data = cursor.fetchone()

            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            dataset = datasets.ImageFolder(dir, transform=preprocess)
            img_tensor = preprocess(data).unsqueeze(0)
            with torch.no_grad():  # Отключаем расчет градиентов (экономим память)
                output = self.model(img_tensor)
                pred_idx = torch.argmax(output, dim=1).item()
            label = dataset.classes[pred_idx.item()]
            return label

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            if connection:
                connection.close()
                print('info: коннект закрыт')
