import roslibpy

class ROSHandler:
    def __init__(self, host, port):
        self.client = roslibpy.Ros(host=host, port=port)

    def connect(self):
        self.client.run()

    def disconnect(self):
        self.client.terminate()
