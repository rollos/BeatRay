import mido

class LiveView():
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message, value):
        for observer in self.observers:
            observer.notify(message, value)

    def get_midi_input(self):
        return mido.open_input('Traktor Virtual Output')