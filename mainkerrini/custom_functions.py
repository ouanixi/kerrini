import uuid
from kerrini.settings import STATIC_URL
import os


media = STATIC_URL + "videos/"


def handle_uploaded_file(file):

    path = str(uuid.uuid1())
    with open(media, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path
