import pygmsh

def main(width, length, height):
    with pygmsh.occ.Geometry() as geom:
        sketch = geom.add_rectangle(
            [0.0, 0.0, 0.0],  # lower-left corner
            width,
            length
        )
        geom.extrude(sketch, [0.0, 0.0, height])
        mesh = geom.generate_mesh()

    return mesh

if __name__ == '__main__':
    # box 1
    mesh = main(width=20, length=100, height=10.0)
    mesh.write('box1.stl')
    # box 2
    mesh = main(width=40, length=40, height=10.0)
    mesh.write('box2.stl')
    # box 3
    mesh = main(width=100, length=60, height=10.0)
    mesh.write('box3.stl')
    # -----