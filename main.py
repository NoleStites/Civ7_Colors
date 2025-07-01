from model.Model import Model
from view.View import View
from controller.Controller import Controller

class App():

    def __init__(self):
        
        os = "Windows"
        
        match os:
            case "Windows":
                path = "C:\\Program Files (x86)\\Steam\steamapps\\common\\Sid Meier's Civilization VII\\"
                sub_path = "Base\\modules\\base-standard\\data\\colors\\"
            case _:
                path = "C:\\Program Files (x86)\\Steam\steamapps\\common\\Sid Meier's Civilization VII\\"
                sub_path = "Base\\modules\\base-standard\\data\\colors\\"
        
        model = Model(path, sub_path)
        controller = Controller(model)
        view = View(controller)


if __name__ == "__main__":
    app = App()

