import docker

class ContainerChecking:

    def __init__(self):
        self.client = docker.from_env()
        self.container_name = "djangoframework"

    def __call__(self):
        if self.container_checking(self.container_name):
            print("✅ Container is running")
        else:
            self.conatainer_start(self.container_name)
            print("✅ Container is starting")

    def container_checking(self, name):
        try:
            container = self.client.containers.get(name)
            return container.status == "running"
        except docker.errors.NotFound:
            return False

    def conatainer_start(self, name):
        container = self.client.containers.get(name)
        container.start()

def main():
    checker = ContainerChecking()
    checker()


if __name__ == "__main__":
    main()
