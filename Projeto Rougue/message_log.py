class MessageLog:
    def __init__(self):
        self.messages = []

    def add(self, text):
        self.messages.append(text)