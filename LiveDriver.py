from Views import LiveView as LV
from Controllers import LiveController as LC
from Models import LiveModel as LM


if __name__ == '__main__':
    model = LM.LiveModel()
    view = LV.LiveView()
    controller = LC.LiveController(model, view)





