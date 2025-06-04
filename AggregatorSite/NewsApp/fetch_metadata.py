from django.utils import timezone

class SingletonMeta(type):
    """
    A Singleton metaclass that ensures a class has only one instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class FetchMetadata(metaclass=SingletonMeta):
    def __init__(self):
        self.last_loaded = timezone.now()
    def set_time(self):
        self.last_loaded = timezone.now()
    def return_time(self):
        return self.last_loaded
