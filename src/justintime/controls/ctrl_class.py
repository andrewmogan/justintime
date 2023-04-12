class ctrl:
    def __init__(self, name, id, div, engine):
        self.name = name
        self.id = id
        self.div = div
        self.ctrls =[]
        self.engine = engine
        self.display = {"display":"block"}

    def change_display(self, display):
        self.display = display


    def add_ctrl(self, ctrl):
        if isinstance(ctrl, list):
            self.ctrls.extend(ctrl)
        elif isinstance(ctrl, str):
            self.ctrls.append(ctrl)
