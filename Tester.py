import mido


input = mido.open_input("Traktor Kontrol F1 - 1 Input")

while True:

    for msg in input.iter_pending():
        print(msg)