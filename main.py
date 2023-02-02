import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import keyboard
import glfw
import time
import random
import math

from camera import *
from graphics import *
from vector3 import *
from matrix3x3 import *
from AGX1 import *
from vessels import components

def get_os_type():
    return os.name

def clear_cmd_terminal(os_name):
    if os_name == "nt":
        os.system("cls")
    else:
        os.system("clear")

vp_size_changed = False
def resize_cb(window, w, h):
    global vp_size_changed
    vp_size_changed = True

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def main():
    global vp_size_changed

    # init graphics
    print("Initializing GLFW...")
    glfw.init()
    
    print("Setting up graphics...")
    window_x = 1280
    window_y = 720
    mwin = glfw.create_window(window_x, window_y, "miniFlight3D", None, None)
    glfw.set_window_pos(mwin, 50, 50)
    glfw.make_context_current(mwin)
    glfw.set_window_size_callback(mwin, resize_cb)

    gluPerspective(70, window_x/window_y, 0.05, 1000)
    glEnable(GL_CULL_FACE)
    glEnable(GL_POINT_SMOOTH)
    glClearColor(0,0,0,1)

    os_name = str(get_os_type())

    main_cam = camera("main_cam", vec3(0,0,0), [[1,0,0],[0,1,0],[0,0,1]], True)
    main_cam.move(vec3(2,10,-10))
    main_cam.rotate(vec3(45, 0, 0))

    # keyboard controls
    cam_strafe_speed = 0.1
    cam_rotate_speed = 0.1
    cam_pitch_down = "W"
    cam_pitch_up = "S"
    cam_yaw_left = "A"
    cam_yaw_right = "D"
    cam_roll_ccw = "Q"
    cam_roll_cw = "E"
    cam_strafe_up = "U"
    cam_strafe_down = "O"
    cam_strafe_right = "L"
    cam_strafe_left = "J"
    cam_strafe_forward = "I"
    cam_strafe_backward = "K"

    # create test plane
    plane = create_AGX_1()
    plane.engines[0].thrust = 10000
    plane.vel = vec3(0, 1, 0)
    vessels = [plane]

    # init physical stuff
    gravity = vec3(0, 0, -9.8)
    #gravity = vec3()
    dt = 1e-3

    while not glfw.window_should_close(mwin):
        glfw.poll_events()

        if vp_size_changed:
            vp_size_changed = False
            w, h = glfw.get_framebuffer_size(mwin)
            glViewport(0, 0, w, h)

        # camera movement
        main_cam.rotate(vec3(lst=[(keyboard.is_pressed(cam_pitch_down) - keyboard.is_pressed(cam_pitch_up)) * cam_rotate_speed,
                                  (keyboard.is_pressed(cam_yaw_left) - keyboard.is_pressed(cam_yaw_right)) * cam_rotate_speed,
                                  (keyboard.is_pressed(cam_roll_ccw) - keyboard.is_pressed(cam_roll_cw)) * cam_rotate_speed]))

        main_cam.move(vec3(lst=[(keyboard.is_pressed(cam_strafe_left) - keyboard.is_pressed(cam_strafe_right)) * cam_strafe_speed,
                                (keyboard.is_pressed(cam_strafe_down) - keyboard.is_pressed(cam_strafe_up)) * cam_strafe_speed,
                                (keyboard.is_pressed(cam_strafe_forward) - keyboard.is_pressed(cam_strafe_backward)) * cam_strafe_speed]))

        # PHYSICS HAPPEN HERE
        
        for v in vessels:
            # apply gravity
            v.vel += gravity * dt

            for ve in v.engines:
                # apply engine linear thrust
                if ve.thrust > ve.max_thrust:
                    ve.thrust = ve.max_thrust
                    
                if ve.is_intake_enough(ve.air_intake.dot(v.vel) + ve.idle_compressor_intake):
                    v.vel += (ve.rel_axis * ve.thrust / v.mass) * dt
                    
                for idx_tank in range(len(ve.tanks)):
                    tank = ve.tanks[idx_tank]
                    mass_flow = ve.mass_flows[idx_tank] * ve.get_throttle() * dt

                    if tank.fluid_mass > 0:
                        tank.fluid_mass -= mass_flow
                        tank.m -= mass_flow
                    elif tank.fluid_mass < 0:
                        tank.fluid_mass = 0

            for vw in v.wings:
                aoa = math.acos(v.vel.normalized().dot(v.orient.vy()))
                cl = vw.baseCl * math.sin(aoa)
                airflow_vec = -v.vel
                lift_dir = airflow_vec.cross(v.orient.vx())
                lift_dir = lift_dir - v.orient.vy() * v.orient.vy().dot(lift_dir)
                lift_mag = 0.5 * cl * v.vel.mag()**2 * vw.A_top * 1 # change 1 with air density
                lift_vec = lift_dir * lift_mag / v.mass
                v.vel += lift_vec * dt

                drag_dir = airflow_vec
                drag_mag = (abs(airflow_vec.normalized().dot(v.orient.vx()) * vw.A_side) + abs(airflow_vec.normalized().dot(v.orient.vy()) * vw.A_front) + abs(airflow_vec.normalized().dot(v.orient.vz()) * vw.A_top)) * vw.baseCd * 0.5 * airflow_vec.mag()**2
                drag_vec = drag_dir * drag_mag / v.mass
                v.vel += drag_vec * dt

        for v in vessels:
            v.pos += v.vel * dt
            v.update_mass()
            
        # END PHYSICS

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawScene(main_cam, vessels)
        glfw.swap_buffers(mwin)

main()
