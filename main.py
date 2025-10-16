import platform
from pathlib import Path
from model.Model import Model
from view.View import View
from controller.Controller import Controller

class App():

    def __init__(self):
        
        os = platform.system()
        
        # path = "C:\\Program Files (x86)\\Steam\steamapps\\common\\Sid Meier's Civilization VII\\"
        # sub_path = "Base\\modules\\base-standard\\data\\colors\\"
        
        if (os == "Windows"):
            path = Path("C:/Program Files (x86)/Steam/steamapps/common/Sid Meier's Civilization VII/")
            sub_path = Path("Base/modules/base-standard/data/colors/")
        else: # MacOS or Linux
            path = Path.home() / "Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VII/"
            sub_path = Path("Base/modules/base-standard/data/colors/")

        
        model = Model(path, sub_path)
        controller = Controller(model)
        view = View(controller)


if __name__ == "__main__":
    app = App()

