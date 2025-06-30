from model.Model import Model

class Controller():

    def __init__(self, model: Model):
        self.model = model


    def acquire_leaders(self):
        leaders, leader_dict = self.model.acquire_leaders()
        return leaders, leader_dict


    def add_colors(self, primary, secondary):
        return self.model.add_colors(primary, secondary)


    def assign_alt3(self, leader, path, p_title, s_title):
        self.model.assign_alt3(leader, path, p_title, s_title)


    def reset_files(self, leader_dict):
        self.model.reset_files(leader_dict)
