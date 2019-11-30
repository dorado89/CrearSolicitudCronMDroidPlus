from time import sleep
import datetime
import Settings
import json
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from SQSConnection import SQSConnection


def execute_test(script,urlapk):
    subprocess.run(['git', 'clone', script])
    sleep(60)
    #outputsrc = subprocess.call(['find','.','src'])
    #java -jar MDroidPlus-1.0.0.jar ./libs4ast/ ./calendula/Calendula/src/ es.usc.citius.servando.calendula ./output/calendula . false
    output = subprocess.call(['java' ,'-jar' ,'MDroidPlus-1.0.0.jar' ,'./libs4ast/', './calendula/Calendula/src/', 'es.usc.citius.servando.calendula', './output/calendula', '.' ,'false'])
    # s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)
    # msg = MIMEMultipart()
    # message = output
    #
    # msg['From'] = MY_ADDRESS
    # msg['To'] = email
    # msg['Subject'] = "This is TEST"
    #
    # msg.attach(MIMEText(message, 'plain'))
    #
    # s.send_message(msg)
    # del msg
    # s.quit()
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
                listapruebas = msg["pruebas"]
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
