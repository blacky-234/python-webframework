import subprocess
from django.db import connection
from django.http import JsonResponse


POSTGRES_CONTAINER = "djangoframework"
MEMCACHE_CONTAINER = "memcache_container"


class ContainerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 1) Check DB connection
        db_ok = self.check_db()

        if not db_ok:
            self.start_container(POSTGRES_CONTAINER)

        # 2) Check Memcached (optional)
        # if not self.check_memcache():
        #     self.start_container(MEMCACHE_CONTAINER)

        return self.get_response(request)

    def check_db(self):
        try:
            connection.cursor()  # Try DB connection
            return True
        except Exception:
            return False

    def check_memcache(self):
        import socket
        try:
            s = socket.create_connection(("172.17.0.4", 11211), timeout=1)
            s.close()
            return True
        except Exception:
            return False

    def start_container(self, name):
        print(f"➡️ Starting container: {name}")
        subprocess.run(["docker", "start", name])
