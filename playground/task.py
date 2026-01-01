from time import sleep
from celery import shared_task

@shared_task
def notify_customer(message):
    print("sending notification to customer...")
    print(message)
    sleep(2)
    print("notification sent successfully!")