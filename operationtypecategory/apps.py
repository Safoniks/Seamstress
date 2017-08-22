from django.apps import AppConfig


class OperationtypecategoryConfig(AppConfig):
    name = 'operationtypecategory'

    def ready(self):
        import operationtypecategory.signals.category_signals
