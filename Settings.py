import os

AWS_ACCESS_KEY_ID_SQS = os.environ.get('AWS_ACCESS_KEY_ID_SQS')
AWS_SECRET_ACCESS_KEY_SQS = os.environ.get('AWS_SECRET_ACCESS_KEY_SQS')
AWS_REGION_SQS = os.environ.get('AWS_REGION_SQS')
AWS_QUEUE_URL_IN = os.environ.get('AWS_QUEUE_URL_IN')
AWS_QUEUE_URL_OUT_MDROIDPLUS = os.environ.get('AWS_QUEUE_URL_OUT_MDROIDPLUS')
SLEEP_TIME = 5