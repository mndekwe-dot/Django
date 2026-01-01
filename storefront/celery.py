import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

# Create Celery app instance
app = Celery('storefront')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()  # Call on the instance 'app', not the class 'Celery'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')