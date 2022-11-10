from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

stone_texture = load_texture('block_stone.png')
wood_texture = load_texture('block_planks.png')
sky_texture = load_texture('sky.jpeg')

block_pick = 1


def update():
    global block_pick
    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)

            if key == 'right mouse down':
                if block_pick == 1:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture='grass')

                if block_pick == 2:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=stone_texture)

                if block_pick == 3:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=wood_texture)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True,
        )


for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()

sky = Sky()

app.run()
