import pywavefront
import sys

from vessels.components.vessel import *
from vessels.components.fuselage import *
from vessels.components.turbojet import *
from vessels.components.wing import *
from vessels.components.tank import *

from vector3 import *
from matrix3x3 import *

def create_AGX_1():
    model_fuselage = pywavefront.Wavefront("vessels/models/AGX_fuselage.obj", collect_faces=True)
    model_turbojet = pywavefront.Wavefront("vessels/models/AGX_engine.obj", collect_faces=True)
    model_mainwing = pywavefront.Wavefront("vessels/models/AGX_mainwing.obj", collect_faces=True)
    model_aftwing = pywavefront.Wavefront("vessels/models/AGX_aftwing.obj", collect_faces=True)
    model_tailfin = pywavefront.Wavefront("vessels/models/AGX_tailfin.obj", collect_faces=True)
    model_fueltank = pywavefront.Wavefront("vessels/models/AGX_tank.obj", collect_faces=True)

    # fuselage
    # 1.5m diam
    # 12m length
    # 2 tons mass
    main_body = cylindrical_fuselage(vec3(), model_fuselage, 1.5, 12, 2000)

    # main wings
    # 100 kg
    # starboard main wing
    wing_starboard = basic_airfoil(vec3(3, 1, 0), model_mainwing, 0.1, 0.5, 100, 3, 0.2, 5)
    # port main wing
    wing_port = basic_airfoil(vec3(-3, 1, 0), model_mainwing, 0.1, 0.5, 100, 3, 0.2, 5)

    # aft wings
    wing_starboard_aft = basic_airfoil(vec3(2, -4, 0), model_aftwing, 0.1, 0.5, 30, 2, 0.2, 3)
    wing_port_aft = basic_airfoil(vec3(-2, -4, 0), model_aftwing, 0.1, 0.5, 30, 2, 0.2, 3)

    # tail fin
    wing_tailfin = basic_airfoil(vec3(0, -4, 1), model_tailfin, 0.1, 0, 20, 2, 0.2, 2)

    # fuel tanks
    # 50 kg dry mass
    # 300 kg fuel each
    tank_starboard = fuel_tank(vec3(1, 1, 0), model_fueltank, 50, 300)
    tank_port = fuel_tank(vec3(-1, 1, 0), model_fueltank, 50, 300)

    # engine
    # 400 kg
    # 10 kN thrust max
    # 0.5 kg/s fuel consumption max
    main_engine = turbojet(vec3(0, -5, 0), model_turbojet, vec3(0,1,0), 400, 10e3, 10e3, [], [0.5, 0.5], vec3(0,1.766,0), 1, 0.5)

    comps = [main_body, main_engine, wing_starboard, wing_port, wing_starboard_aft, wing_port_aft,
             wing_tailfin, tank_starboard, tank_port]

    fsl = [main_body]

    tnk = [tank_starboard, tank_port]

    eng = [main_engine]

    wng = [wing_starboard, wing_port, wing_starboard_aft, wing_port_aft, wing_tailfin]

    css = []

    ipos = vec3(0, 0, 0)

    ivel = vec3(0, 0, 0)

    iorient = matrix3x3()

    AGX = vessel("AGX-1", comps, fsl, tnk, eng, wng, css, ipos, ivel, iorient)

    # connect tanks to engine
    AGX.engines[0].tanks.append(AGX.tanks[0])
    AGX.engines[0].tanks.append(AGX.tanks[1])
    return AGX
