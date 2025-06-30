from model.Model import Model
from view.View import View
from controller.Controller import Controller

class App():

    def __init__(self):
        model = Model()
        controller = Controller(model)
        view = View(controller)


if __name__ == "__main__":
    app = App()

