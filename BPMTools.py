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


def ticks_to_beat(ticks):
    return ticks/24

def beats_to_tick(beats):
    return beats*24

def beats_to_bar(beats):
    return beats/4

def bars_to_beats(bars):
    return bars*4

def ticks_to_bars(ticks):
    return beats_to_bar(ticks_to_beat(ticks))

def bars_to_ticks(bars):
    return beats_to_tick(bars_to_beats(bars))

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