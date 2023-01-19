from PIL import Image

from raypy.geometry.plane import Plane
from raypy.geometry.sphere import Sphere
from raypy.geometry.cuboid import Cuboid
from raypy.materials.emissive import Emissive
from raypy.renderer import Renderer
from raypy.utils.vector3 import vec3, rgb
from raypy.scene import Scene
from raypy.materials.diffuse import Diffuse

def main():

    WIDTH = 500
    HEIGHT = 500
    SAMPLES = 500

    index_of_refraction = vec3(1.0, 1.0, 1.0)
    scene = Scene(n=index_of_refraction)

    blue_diffuse = Diffuse(diff_color=rgb(0.27, 0.51, 0.84))
    red_diffuse = Diffuse(diff_color=rgb(0.74, 0.08, 0.08))
    yellow_diffuse = Diffuse(diff_color=rgb(.90, .82, .1))
    white_diffuse = Diffuse(diff_color=rgb(.73, .73, .73))
    emissive_white = Emissive(color=rgb(35.0, 35.0, 35.0))

    scene.add(Plane(material=emissive_white, center=vec3(213 + 130 / 2, 554, -227.0 - 105 / 2), width=130.0, height=105.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, 1.0)),
           importance_sampled=True)

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 555 / 2, -555.0), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(1.0, 0, 0.0)))

    scene.add(Plane(material=red_diffuse, center=vec3(-0.0, 555 / 2, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=blue_diffuse, center=vec3(555.0, 555 / 2, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 555, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 0., -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    size = 180
    # leftCube = Cuboid(material=yellow_diffuse, center=vec3(150, size / 2, -size - 160 / 2), width=size,
    #                   height=size,
    #                   length=size,
    #                   shadow=True)
    # scene.add(leftCube)
    leftSphere = Sphere(center=vec3(150, size / 2, -size - 160 / 2), radius=size / 2, material=yellow_diffuse)
    scene.add(leftSphere)

    rightCube = Cuboid(material=white_diffuse, center=vec3(390, size, -185 - 160 / 2), width=size, height=size*2, length=size)
    rightCube.rotate(theta=55, u=vec3(0,1,0))
    scene.add(rightCube)

    scene.add_camera(screen_width=WIDTH,
                     screen_height=HEIGHT,
                     look_from=vec3(278, 278, 800),
                     look_at=vec3(278, 278, 0),
                     field_of_view=40)

    renderer = Renderer(scene)
    img = renderer.render(SAMPLES)
    img.save(f"results/result_Sphere-{WIDTH}x{HEIGHT}-{SAMPLES}_samples.png")

if __name__ == '__main__':
    main()
