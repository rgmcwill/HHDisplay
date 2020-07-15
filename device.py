class device:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __next__(self):
        print("Name: " + self.name + " | Address: " + self.address)