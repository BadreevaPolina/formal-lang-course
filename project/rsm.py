class RSM:
    def __init__(self, start_symbol=None, boxes=None):
        self.start_symbol = start_symbol
        self.boxes = boxes

    def rsm_from_ecfg(self, ecfg):
        boxes = {key: value.to_epsilon_nfa() for key, value in ecfg.productions.items()}
        self.start_symbol = ecfg.start_symbol
        self.boxes = boxes
        return self

    def minimize(self):
        for key, nfa in self.boxes.items():
            self.boxes[key] = nfa.minimize()
        return self
