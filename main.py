from psutil import cpu_times
from viewerGL import ViewerGL
import glutils
import glfw
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text, ObjectPhyx
import numpy as np
import OpenGL.GL as GL
import pyrr
import time


def main():

    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y   = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id  = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    #cette partie en commentaire n'est plus utile, on la garde pour s'aider du code fourni
    """#Stegosaurus
    m                    = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr                   = Transformation3D()
    tr.translation.y     = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z     = -5
    tr.rotation_center.z = 0.2
    texture              = glutils.load_texture('stegosaurus.jpg')
    vitesse              = pyrr.Vector3()
    o                    = ObjectPhyx(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr, vitesse)
    viewer.add_object(o)"""


    #Notre personnage : une sphère
    nb_points = 50
    m = Mesh()
    u = np.linspace(-np.pi, np.pi, nb_points)
    v = np.linspace(-np.pi/2, np.pi/2, nb_points)
    r = 0.65
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))[0]
    p0, p1, p2, p3 = [x, y, z], [x, y, z], [x, y, z], [x, y, z]
    n, c           = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]

    p = []
    for i in range(len(u)):
        for j in range(len(v)):
            x = r * np.outer(np.cos(u[i]), np.sin(v[j]))
            y = r * np.outer(np.sin(u[i]), np.sin(v[j]))
            z = r * np.outer(np.ones(np.size(u[i])), np.cos(v[j]))[0]
            pc = [x, y, z, x/r, y/r, z/r, 1,1,1, 0,0] #on crée les points qui définissent la sphère
            p.append(pc)
    m.vertices = np.array(p, np.float32)
    print(m.vertices)

    t = [] #on initialise le tableau contenant les points des triangles au sein de la sphère
    for i in range(len(u)-1):
        for j in range(len(v)-1):
            tc0 = [i+j*nb_points, i+1+j*nb_points, i+(j+1)*nb_points] #on crée le premier triangle adjacent au point cible
            tc1 = [i+1+(j+1)*nb_points, i+1+j*nb_points, i+(j+1)*nb_points] #on crée le second triangle adjacent au point cible
            t.append(tc0)
            t.append(tc1)
    m.faces = np.array(t, np.uint32)
    print(m.faces)
    #Définitions nécessaires pour l'utilisation de Object3D
    tr                   = Transformation3D()
    tr.translation.y     = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z     = -5
    tr.rotation_center.z = 0.2
    vitesse              = pyrr.Vector3()
    texture              = glutils.load_texture('rouge.jpg') #la texture est obligatoire pour la classe Object3D
    o                    = ObjectPhyx(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr, vitesse)
    viewer.add_object(o)
    

    #Sol (piste bleue)
    m = Mesh()
    p0, p1, p2, p3 = [-7, 0, -10], [7, 0, -10], [7, 0, 2000], [-7, 0, 2000]
    n, c           = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1] 
    m.vertices     = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces        = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture        = glutils.load_texture('fondbleu.jpg')
    o              = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    # m.vertices     = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    # m.faces        = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture        = glutils.load_texture('grass.jpg')
    o              = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #Ajout d'un 1er obstacle : cube jaune
    m                    = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.7, 0.7, 0.7, 0.5]))
    tr                   = Transformation3D()
    tr.translation.y     = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z     = -5
    tr.rotation_center.z = 0.2
    texture              = glutils.load_texture('jaune.jpg')
    o                    = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    #Ajout d'un 2e obstacle : cube orange
    m                    = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.7, 0.7, 0.7 , 0.5]))
    tr                   = Transformation3D()
    tr.translation.y     = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z     = -5
    tr.rotation_center.z = 0.2
    texture              = glutils.load_texture('orange.png')
    o                    = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    #Ajout d'un 3e obstacle : cube orange
    m                    = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.7, 0.7, 0.7 , 0.5]))
    tr                   = Transformation3D()
    tr.translation.y     = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z     = -5
    tr.rotation_center.z = 0.2
    texture              = glutils.load_texture('vert.png')
    o                    = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)


    vao     = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o       = Text('runball', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float16), vao, 2, programGUI_id, texture)
    viewer.add_object(o)


    viewer.run()



if __name__ == '__main__':
    main()