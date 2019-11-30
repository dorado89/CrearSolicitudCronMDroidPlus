from time import sleep
import datetime
import Settings
import json
import subprocess
from SQSConnection import SQSConnection


def execute_test(script,urlapk):
    subprocess.run(['git', 'clone', script])
    output = subprocess.call(['java','-jar','MDroidPlus-1.0.0.jar','./lib4ast/','./'+script.rsplit('/',1)[-1]],urlapk,'./'+urlapk,'./','false')
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
                listapruebas = msg[0]["fields"]["pruebas"]
                script=""
                urlapk=""
                for prueba in listapruebas:
                    script=prueba["script"]
                    urlapk=prueba["url_apk"]
                # sqs_connection.delete()
                execute_test(script,urlapk)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        process()
        st = str(datetime.datetime.now())
        print(st + ' : alive')
        sleep(Settings.SLEEP_TIME)
