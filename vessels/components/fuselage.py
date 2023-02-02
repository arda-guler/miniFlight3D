import math
PI = math.pi

class cylindrical_fuselage:
    def __init__(self, rel_pos, model, D, L, m):
        self.rel_pos = rel_pos # relative position wrt. vessel's center
        self.model = model
        self.D = D # outer diameter in meters
        self.L = L # length in meters
        self.m = m # mass in kg
        
        self.I_long = 0.5 * m * (D/2)**2 # axial (longitudional) moment of inertia
        self.I_trans = (1/12) * m * (3*(D/2)**2 + L**2) # transverse moment of inertia about center
        
        self.A_front = PI * (D**2)/4 # frontal area
        self.A_side = L * D # side area
