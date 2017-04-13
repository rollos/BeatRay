import mido


class LiveModel():

    def __init__(self):
        print(mido.get_input_names())

        #self.midi_clock =

    def set_midi_input(self, input):
        self.midi_input = input

        self.run_clock()

    def run_clock(self):
        while(True):
            for message in self.midi_input:
                print(message)

                if message.type == 'clock':
                    self.run_frame()
                



    def run_frame(self):
        print("frame")

