from aiohttp import web
from app.app import App
import logging
import json

main = web.Application()

with open('config.json') as file:
    file = json.load(file)

app = App()

main.router.add_route('POST', '/check_data/', app.check_data)

web.run_app(main, host=file['host'], port=file['port'])
