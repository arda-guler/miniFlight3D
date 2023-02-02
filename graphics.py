import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import pywavefront

from math_utils import *
from ui import *
from vector3 import *

def calcTransparentColor(background_color, main_color, alpha=0.5):
    delta_r = background_color[0] - main_color[0]
    delta_g = background_color[1] - main_color[1]
    delta_b = background_color[2] - main_color[2]

    return [main_color[0] + delta_r * (1-alpha), main_color[1] + delta_g * (1-alpha), main_color[2] + delta_b * (1-alpha)]

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(100,0,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,100,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,100)
    glEnd()

def drawPoints(points):

    for p in points:
        glColor(p.color[0], p.color[1], p.color[2])
        
        glPushMatrix()
        glTranslatef(p.pos.x, p.pos.y, p.pos.z)

        glBegin(GL_POINTS)
        glVertex3f(0, 0, 0)
        glEnd()

        glPopMatrix()

def drawPoint2D(x, y, color, camera):
    glPushMatrix()

    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])

    glBegin(GL_POINTS)

    x1 = x * 100
    y1 = y * 100

    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)

    x1 = x1 * 100
    y1 = y1 * 100
    x2 = x2 * 100
    y2 = y2 * 100
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

def drawForces(forces):
    
    for f in forces:
        glPushMatrix()

        scaler = 0.2
        start_position = f.point.pos
        end_position = f.point.pos + f.force
        f_vector = f.force * scaler
        
        f_dir = f_vector.normalized()
        arrowhead_start = f.force * scaler * 0.8

        if not f_dir.cross(vec3(1,0,0)) == vec3(0,0,0):
            arrowhead_vector1 = f_dir.cross(vec3(1,0,0))
        else:
            arrowhead_vector1 = f_dir.cross(vec3(0,1,0))

        arrowhead_vector2 = arrowhead_vector1.cross(f_dir)

        arrowhead_vector1 = arrowhead_vector1 * f.force.mag() * scaler * 0.1
        arrowhead_vector2 = arrowhead_vector2 * f.force.mag() * scaler * 0.1
            
        arrowhead_pt1 = arrowhead_start + arrowhead_vector1
        arrowhead_pt2 = arrowhead_start - arrowhead_vector1

        arrowhead_pt3 = arrowhead_start + arrowhead_vector2
        arrowhead_pt4 = arrowhead_start - arrowhead_vector2
        
        glTranslate(start_position.x, start_position.y, start_position.z)
        glColor(1,0,1)

        glBegin(GL_LINES)

        glVertex3f(0,0,0)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glEnd()

        glPopMatrix()

def drawVector(vessel, rel_pos, vector):
    
    glPushMatrix()

    scaler = 0.2
    start_position = vessel.pos + rel_pos
    end_position = vessel.pos + vector
    f_vector = vector * scaler
    
    f_dir = f_vector.normalized()
    arrowhead_start = vector * scaler * 0.8

    if not f_dir.cross(vec3(1,0,0)) == vec3(0,0,0):
        arrowhead_vector1 = f_dir.cross(vec3(1,0,0))
    else:
        arrowhead_vector1 = f_dir.cross(vec3(0,1,0))

    arrowhead_vector2 = arrowhead_vector1.cross(f_dir)

    arrowhead_vector1 = arrowhead_vector1 * vector.mag() * scaler * 0.1
    arrowhead_vector2 = arrowhead_vector2 * vector.mag() * scaler * 0.1
        
    arrowhead_pt1 = arrowhead_start + arrowhead_vector1
    arrowhead_pt2 = arrowhead_start - arrowhead_vector1

    arrowhead_pt3 = arrowhead_start + arrowhead_vector2
    arrowhead_pt4 = arrowhead_start - arrowhead_vector2
    
    glTranslate(start_position.x, start_position.y, start_position.z)
    glColor(1,0,1)

    glBegin(GL_LINES)

    glVertex3f(0,0,0)
    glVertex3f(f_vector.x, f_vector.y, f_vector.z)

    glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
    glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

    glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
    glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

    glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
    glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

    glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
    glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

    glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
    glVertex3f(f_vector.x, f_vector.y, f_vector.z)

    glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
    glVertex3f(f_vector.x, f_vector.y, f_vector.z)

    glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)
    glVertex3f(f_vector.x, f_vector.y, f_vector.z)

    glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)
    glVertex3f(f_vector.x, f_vector.y, f_vector.z)

    glEnd()

    glPopMatrix()

def drawCursors(cursors, camera):

    for cursor in cursors:
        if cursor.visible:
            glPushMatrix()

            glTranslate(cursor.pos.x,
                        cursor.pos.y,
                        cursor.pos.z)
            
            glColor(cursor.color[0], cursor.color[1], cursor.color[2])

            glBegin(GL_LINES)

            glVertex3f(2,0,0)
            glVertex3f(-2,0,0)

            glVertex3f(0,2,0)
            glVertex3f(0,-2,0)

            glVertex3f(0,0,2)
            glVertex3f(0,0,-2)

            glEnd()
            
            glPopMatrix()

def drawModelLocalMatrix(model, color, line=True, poly=False):
        
    glColor(color[0], color[1], color[2])

    if poly and line:
        for mesh in model.mesh_list:
            glColor(color[0]-0.1, color[1]-0.1, color[2]-0.1)
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

            glColor(color[0], color[1], color[2])
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()
            
    elif poly:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

    elif line:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

def drawModelGeneric(model, pos, rot, scale, color, line=True, poly=True):
    
    glPushMatrix()
    
    glTranslatef(pos[0], pos[1], pos[2])

    if rot:
        glRotatef(rot[0], rot[1], rot[2], rot[3])

    if scale:
        glScalef(scale[0], scale[1], scale[2])
        
    glColor(color[0], color[1], color[2])

    if poly and line:
        for mesh in model.mesh_list:
            glColor(color[0]-0.1, color[1]-0.1, color[2]-0.1)
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

            glColor(color[0], color[1], color[2])
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()
            
    elif poly:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

    elif line:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

    glPopMatrix()

def drawVessels(vessels):
    
    for v in vessels:
        # vessel matrix
        glPushMatrix()
        glTranslatef(v.pos.x, v.pos.y, v.pos.z)
        
##        for c in v.components:
##            # component matrix
##            glPushMatrix()
##            cmodel = c.model
##            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
##            glRotatef(90, 1, 0, 0)
##            # glScalef(scale[0], scale[1], scale[2])
##            drawModelLocalMatrix(c.model, (1,1,1))
##
##            # componenet matrix
##            glPopMatrix()

        for c in v.fuselages:
            # component matrix
            glPushMatrix()
            cmodel = c.model
            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
            glRotatef(90, 1, 0, 0)
            # glScalef(scale[0], scale[1], scale[2])
            drawModelLocalMatrix(c.model, (1,1,1))

            # componenet matrix
            glPopMatrix()

        for c in v.tanks:
            # component matrix
            glPushMatrix()
            cmodel = c.model
            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
            glRotatef(90, 1, 0, 0)
            # glScalef(scale[0], scale[1], scale[2])
            drawModelLocalMatrix(c.model, (1,1,0))

            # componenet matrix
            glPopMatrix()

        for c in v.engines:
            # component matrix
            glPushMatrix()
            cmodel = c.model
            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
            glRotatef(90, 1, 0, 0)
            # glScalef(scale[0], scale[1], scale[2])
            drawModelLocalMatrix(c.model, (1,0,1))

            # componenet matrix
            glPopMatrix()

        for c in v.wings:
            # component matrix
            glPushMatrix()
            cmodel = c.model
            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
            glRotatef(90, 1, 0, 0)
            # glScalef(scale[0], scale[1], scale[2])
            drawModelLocalMatrix(c.model, (0,1,1))

            # componenet matrix
            glPopMatrix()

        for c in v.control_surfaces:
            # component matrix
            glPushMatrix()
            cmodel = c.model
            glTranslatef(c.rel_pos.x, c.rel_pos.y, c.rel_pos.z)
            glRotatef(90, 1, 0, 0)
            # glScalef(scale[0], scale[1], scale[2])
            drawModelLocalMatrix(c.model, (1,0,0))

            # componenet matrix
            glPopMatrix()

        # vessel matrix
        glPopMatrix()

def drawVesselInfo(v, cam):
    render_AN("VEL: " + str(round(v.vel.mag(), 1)), (1,0,0), [-9,6], cam)
    render_AN("MASS: " + str(round(v.mass, 1)), (1,0,0), [-9,5], cam)

def drawScene(cam, vessels):
    #comblist.sort(key=lambda x: mag([-x.pos.x - cam.pos.x, -x.pos.y - cam.pos.y, -x.pos.z - cam.pos.z]), reverse=True)
    drawVessels(vessels)
    drawVesselInfo(vessels[0], cam)
    drawVector(vessels[0], vec3(), vessels[0].vel)
    drawOrigin()

