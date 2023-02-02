class fuel_tank:
    def __init__(self, rel_pos, model, dry_mass, fluid_mass):
        self.rel_pos = rel_pos # relative positin wrt. vessel's center
        self.model = model
        self.dry_mass = dry_mass # dry mass in kg
        self.fluid_mass = fluid_mass # current contained fluid mass in kg

        self.m = dry_mass + fluid_mass # total mass in kg
