import platform

system = platform.system()

if system == "Linux":
    DEBUG = False
elif system == "Windows":
    DEBUG = True

DATABASES = {
    "debug": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "*",
        "database": "mysql",
        "use_unicode": True,
        "charset": "utf8mb4",
        "autocommit": True,
    },
    "product": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "*",
        "database": "mysql",
        "use_unicode": True,
        "charset": "utf8mb4",
        "autocommit": True,
    }
}