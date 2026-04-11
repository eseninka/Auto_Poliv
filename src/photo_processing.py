import requests
import psycopg2
from torchvision import datasets, transforms
import torch
from PIL import Image
import io
from class_dataset import all_class

class photo_processing:
    def __init__(self, HOST, NAME_USER, PASSWORD, DATABASE, CONNECT, url, uuid, model, device):
        self.host = HOST
        self.name_user = NAME_USER
        self.password = PASSWORD
        self.database = DATABASE
        self.connect = CONNECT
        self.url = url
        self.uuid = uuid
        self.model = model
        self.device = device

    def save_photo(self):
        connection = psycopg2.connect(host=self.host, user=self.name_user, password=self.password,
                                      database=self.database)
        connection.autocommit = True
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                with connection.cursor() as cursor:
                    cursor.execute('select cam_id from cam where uuid=%s', (self.uuid,))
                    fet = cursor.fetchone()
                    id_cam = fet[0] if fet else 0
                    if id_cam == 0:
                        cursor.execute('insert into cam(uuid) values (%s)', (self.uuid,))
                    cursor.execute('select cam_id from cam where uuid=%s', (self.uuid,))
                    id_cam = cursor.fetchone()[0]
                    cursor.execute('insert into images(image_data, cam_id) values (%s, %s)', (psycopg2.Binary(response.content), id_cam))
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
        try:
            with connection.cursor() as cursor:
                cursor.execute('select cam_id from cam where uuid=%s', (self.uuid,))
                id_cam = cursor.fetchone()[0]
                cursor.execute('select image_data from images where cam_id=%s order by image_id desc', (id_cam,))
                data = cursor.fetchone()[0]
            img = Image.open(io.BytesIO(data)).convert('RGB')
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            img_tensor = preprocess(img).unsqueeze(0).to(self.device)
            with torch.no_grad():  # Отключаем расчет градиентов (экономим память)
                output = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                conf, pred_idx = torch.max(probabilities, dim=1)
                confidence = conf.item() * 100
                label = all_class[pred_idx]
            return (label, confidence)

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            if connection:
                connection.close()
                print('info: коннект закрыт')
