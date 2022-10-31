from raypy.camera import Camera
from raypy.utils.vector3 import rgb, vec3


class Scene():
    def __init__(self, ambient_color=rgb(0.01, 0.01, 0.01), n=vec3(1.0,1.0,1.0)):
        self.camera = None
        self.scene_primitives = []
        self.collider_list = []
        self.shadowed_collider_list = []
        self.Light_list = []
        self.importance_sampled_list = []
        self.ambient_color = ambient_color
        self.n = n

    def add_camera(self, look_from, look_at, **kwargs):
        self.camera = Camera(look_from, look_at, **kwargs)

    def add(self,primitive, importance_sampled=False):
        self.scene_primitives += [primitive]
        self.collider_list += primitive.collider_list

        if importance_sampled:
            self.importance_sampled_list += [primitive]
        if primitive.shadow:
            self.shadowed_collider_list += primitive.collider_list
