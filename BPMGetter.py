import mido
from threading import Timer
import time


def read_input_clock(input):
    clock_time = 0

    for message in input:
        current_beat_time = time.clock()
        if message.type == 'clock':
            tick()
            # clock_time += 1
            # if (clock_time == 23):  # There is 24 ticks per beat in MIDI
            #     clock_time = 0
            #
            # if (clock_time == 0):
            #     tick()


def tick(scene=None):
    scene.run_frame()
   # print('tick')


def BPMtrigger(bpm, scene,runtime):
    seconds_per_beat = (float(60) / bpm / 24)

    for x in range(runtime):
        if x%24 == 0:
            print("Beat")
        tick(scene)
        time.sleep(seconds_per_beat)


def main():
     print(mido.get_input_names())
    # input = mido.open_input('Traktor Virtual Output')


    # read_input_clock(input)



if __name__ == "__main()__":
    main()