from PIL import Image

from raypy.geometry.plane import Plane
from raypy.geometry.sphere import Sphere
from raypy.materials.emissive import Emissive
from raypy.renderer import Renderer
from raypy.utils.vector3 import vec3, rgb
from raypy.scene import Scene
from raypy.materials.diffuse import Diffuse

def main():

    index_of_refraction = vec3(1.0, 1.0, 1.0)
    scene = Scene(n=index_of_refraction)

    green_diffuse = Diffuse(diff_color=rgb(.12, .45, .15))
    red_diffuse = Diffuse(diff_color=rgb(.65, .05, .05))
    white_diffuse = Diffuse(diff_color=rgb(.73, .73, .73))
    emissive_white = Emissive(color=rgb(15., 15., 15.))

    scene.add(Plane(material=emissive_white, center=vec3(213 + 130 / 2, 554, -227.0 - 105 / 2), width=130.0, height=105.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, 1.0)),
           importance_sampled=True)

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 555 / 2, -555.0), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(1.0, 0, 0.0)))

    scene.add(Plane(material=green_diffuse, center=vec3(-0.0, 555 / 2, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=red_diffuse, center=vec3(555.0, 555 / 2, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(0.0, 1.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 555, -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Plane(material=white_diffuse, center=vec3(555 / 2, 0., -555 / 2), width=555.0, height=555.0,
                 u_axis=vec3(1.0, 0.0, 0), v_axis=vec3(0.0, 0, -1.0)))

    scene.add(Sphere(material=red_diffuse, center=vec3(370.5, 165 / 2, -65 - 185 / 2), radius=165 / 2, shadow=False,
                  max_ray_depth=3))

    scene.add(Sphere(material=green_diffuse, center=vec3(200.5, 165 / 2, -65 - 185), radius=165 / 2, shadow=False,
                  max_ray_depth=3))

    scene.add_camera(screen_width=300,
                     screen_height=300,
                     look_from=vec3(278, 278, 800),
                     look_at=vec3(278, 278, 0),
                     field_of_view=40)

    renderer = Renderer(scene)
    img = renderer.render(500)
    img.save("test.png")

if __name__ == '__main__':
    main()
