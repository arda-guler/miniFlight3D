class basic_airfoil:
    def __init__(self, rel_pos, model, baseCd, baseCl, m,
                 L, t, w):
        self.rel_pos = rel_pos
        self.model = model
        self.baseCd = baseCd # base drag coeff
        self.baseCl = baseCl # base lift coeff
        self.m = m # mass in kg
        self.L = L # chord length in m
        self.t = t # max. thickness in m
        self.w = w # width in m

        self.A_front = w * t
        self.A_top = L * w
        self.A_side = L * t
