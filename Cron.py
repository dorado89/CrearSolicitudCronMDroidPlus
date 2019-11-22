from time import sleep
import datetime
import Settings
import json
import subprocess
from SQSConnection import SQSConnection
from threading import Thread


def execute_test(script):
    txt = script
    output = subprocess.call(['git', 'clone', txt])
    output = subprocess.call(['java','-jar','MDroidPlus-1.0.0.jar'])
    if output < 0:
        print('error en ejecución de prueba')

def process():
    try:
        sqs_connection = SQSConnection(Settings.AWS_QUEUE_URL_OUT_MDROIDPLUS)

        with sqs_connection:
            sqs_connection.receive()
            if sqs_connection.message is not '':
                message_body = sqs_connection.message.get('Body')
                msg = json.loads(message_body)
                #Aqui va la conversion del json
                script = msg['descripcion']
                sqs_connection.delete()
                execute_test(script)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        Thread(target=process).start()
        st = str(datetime.datetime.now())
        print(st + ' : alive')
        sleep(Settings.SLEEP_TIME)
