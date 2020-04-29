from django.apps import AppConfig

def get_current_app_name(file):
    return path.dirname(file).replace('\\', '/').split('/')[-1]

class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = "core_api"
    
