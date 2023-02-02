class turbojet:
    def __init__(self, rel_pos, model, rel_axis, m, thrust, max_thrust,
                 tanks, mass_flows, air_intake, max_intake_requirement,
                 idle_compressor_intake):
        self.rel_pos = rel_pos
        self.model = model
        self.rel_axis = rel_axis # the axis in which thrust is generated
        self.m = m # mass in kg
        self.thrust = thrust # thrust in Newtons
        self.max_thrust = max_thrust # max thrust in Newtons
        self.tanks = tanks # the tanks from which the engine drains fuel
        self.mass_flows = mass_flows # the rates at which the engine consumes fuel from tanks
        self.air_intake = air_intake # the normal of air intake. vector magnitude determines intake area
        self.max_intake_requirement = max_intake_requirement # air intake requirement for max. throttle in kg/s
        self.idle_compressor_intake = idle_compressor_intake # the air sucked in by compressor when the plane has zero air velocity

    def get_throttle(self):
        return self.thrust / self.max_thrust

    def get_intake_requirement(self):
        return self.get_throttle() * self.max_intake_requirement

    def is_intake_enough(self, intake):
        # get if there is enough air intake
        # otherwise, the engine will flame-out
        return bool(intake > self.get_intake_requirement())
