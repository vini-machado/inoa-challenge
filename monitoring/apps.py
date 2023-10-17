from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
import sys

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self) -> None:
        if 'runserver' in sys.argv:
            from .views import Monitoring
            scheduler = BackgroundScheduler()
            m = Monitoring()

            m.execute(scheduler)