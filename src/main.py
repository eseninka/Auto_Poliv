import os
from dotenv import load_dotenv
import torch
from photo_processing import photo_processing

load_dotenv()

HOST = os.getenv("HOST")
NAME_USER = os.getenv("NAME_USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
CONNECT = os.getenv("CONNECT")
URL = os.getenv("URL")
UUID = os.getenv("UUID")

model = torch.load('full_model.pth')
model.eval()

photo_processing(HOST=HOST, NAME_USER=NAME_USER, PASSWORD=PASSWORD, DATABASE=DATABASE, CONNECT=CONNECT, url=URL, uuid=UUID, model=model)




