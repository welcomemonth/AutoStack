# import threading

# class Singleton():
#     """
#     Singleton metaclass for ensuring only one instance of a class.
#     """

#     _instances = {}
#     _lock = threading.Lock()  # 添加锁以保证线程安全

#     def __call__(cls, *args, **kwargs):
#         """Call method for the singleton metaclass."""
#         with cls._lock:
#             if cls not in cls._instances:
#                 cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


# 装饰器确保类是单例模式
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
