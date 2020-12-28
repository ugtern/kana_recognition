from aiohttp import web
from PIL import Image
import base64
import io
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
import json


class App:
    def __init__(self):
        self.class_list = pd.read_csv('./data/k49_classmap.csv')

        self.restored_model = tf.keras.models.load_model('kana_model.hdf5')
        self.restored_model.compile(optimizer=self.restored_model.optimizer,
                               loss='sparse_categorical_crossentropy',
                               metrics=['accuracy'])

    async def check_data(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))
        print('body')
        print(body)

        print("body.get('canvasData')")
        print(body.get('canvasData'))

        img_base64 = body.get('canvasData')

        print('img_base64')
        print(img_base64)

        np.save('img.npz', img_base64)

        image_b64 = img_base64.split(',')[1]
        base64_decoded = base64.b64decode(image_b64)

        image = Image.open(io.BytesIO(base64_decoded))
        image_np = np.array(image)

        image = cv2.cvtColor(image_np[:, :, 1:4], cv2.COLOR_BGR2GRAY)

        dsize = 28, 28
        output = cv2.resize(image, dsize)

        image = output[None, ..., None]

        predict = self.restored_model.predict(image).argmax()
        answer = self.class_list[self.class_list.index == predict].char.tolist()[0]

        print(answer)
        print(type(answer))

        return web.json_response(status=200, data={'answer': answer}, headers={
            'Access-Control-Allow-Origin': req.headers['Origin']
        })
