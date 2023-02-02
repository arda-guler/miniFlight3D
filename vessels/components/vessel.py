class vessel:
    def __init__(self, name, components, fuselages, tanks, engines,
                 wings, control_surfaces, pos, vel, orient):
        self.name = name
        self.components = components
        self.fuselages = fuselages
        self.tanks = tanks
        self.engines = engines
        self.wings = wings
        self.control_surfaces = control_surfaces
        self.pos = pos
        self.vel = vel
        self.orient = orient

        self.dry_mass = self.calc_dry_mass()
        self.fluid_mass = self.calc_fluid_mass()
        self.mass = self.dry_mass + self.fluid_mass

        self.I_x = self.calc_moment_of_inertia_x()
        self.I_y = self.calc_moment_of_inertia_y()
        self.I_z = self.calc_moment_of_inertia_z()

    def calc_fluid_mass(self):
        result = 0
        for i in self.tanks:
            result += i.fluid_mass

        return result

    def calc_dry_mass(self):
        result = 0
        for i in self.fuselages:
            result += i.m

        for i in self.tanks:
            result += i.dry_mass

        for i in self.engines:
            result += i.m

        for i in self.wings:
            result += i.m

        return result

    def update_mass(self):
        self.mass = self.dry_mass + self.calc_fluid_mass()

    # y is the axial axis
    # moment of inertia about y opposes roll
    def calc_moment_of_inertia_y(self): 
        result = 0
        for i in self.fuselages:
            result += i.m * (i.rel_pos.x**2 + i.rel_pos.z**2)**0.5 + i.I_long

        for i in self.tanks:
            result += i.m * (i.rel_pos.x**2 + i.rel_pos.z**2)**0.5

        for i in self.engines:
            result += i.m * (i.rel_pos.x**2 + i.rel_pos.z**2)**0.5

        for i in self.wings:
            result += i.m * (i.rel_pos.x**2 + i.rel_pos.z**2)**0.5

        return result

    # x is the wingspan-aligned axis positive to starboard side
    # moment of inertia about x opposes pitch
    def calc_moment_of_inertia_x(self): 
        result = 0
        for i in self.fuselages:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.z**2)**0.5 + i.I_trans

        for i in self.tanks:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.z**2)**0.5

        for i in self.engines:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.z**2)**0.5

        for i in self.wings:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.z**2)**0.5

        return result

    # z is the upwards axis
    # moment of inertia about z opposes yaw
    def calc_moment_of_inertia_z(self): 
        result = 0
        for i in self.fuselages:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.x**2)**0.5 + i.I_trans

        for i in self.tanks:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.x**2)**0.5

        for i in self.engines:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.x**2)**0.5

        for i in self.wings:
            result += i.m * (i.rel_pos.y**2 + i.rel_pos.x**2)**0.5

        return result
