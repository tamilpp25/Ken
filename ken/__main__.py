import asyncio
import json
import time
from quart import Quart, request
import traceback
from loguru import logger

from utils.functions import Models
import serial

app = Quart(__name__)
arduino = serial.Serial(port='COM5',  baudrate=9600, timeout=.1)

logger.info('Staring Serial LOOP...')

async def startLoop():
    while True:
        arduino.write('aaa'.encode())
        data = arduino.readline().decode()

        if len(data) < 5:
            continue

        data = json.loads(data)
        logger.info(data)

        
        # test = {
        #     'temp': 'mid',
        #     'noise': 'low',
        #     'distance': 'low',
        #     'ldr': 'low',
        #     'pir': 'low',
        # }

        output = await Models.prescribe(data)
        logger.debug(output)

@app.post("/serial")
async def test():
    try:
        
        query = request.args.get('query')

        arduino.write(query.encode())
        time.sleep(0.05)

        return {
            'code': 0,
            'msg': "OK",
            'data': arduino.readline().decode()
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }


@app.post("/prescribe")
async def prescribe():
    try:
        
        data = await request.json

        output = await Models.prescribe(data)

        return {
            'code': 0,
            'data': output
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }


@app.post("/question")
async def question():
    try:

        data = await request.data
        output = await Models.question(data, [request.args.get('q')])

        return {
            'code': 0,
            'data': output
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }
    


@app.get('/')
async def index():
    return {'code': 0}


if __name__ == "__main__":
    logger.debug(f'Binding backend server to 0.0.0.0:5000')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startLoop())
    # app.run(host='0.0.0.0', port=5000)