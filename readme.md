# Miura

## TODO

-   [x] Make phi an abstract class with the ability to compute
    -   phi
    -   phi_x
    -   phi_y
    -   normal
-   [ ] Have face_normal() use phi_x and phi_y
-   [ ] Adjust domain cell generation + inputs
    -   The circumference of the hyperboloid / number of desired cells is the max width of a cell. How to do this generally
    -   Maybe include it in gen_domain
-   [ ] Reposition object orientation so that it is where the Miura center is
    -   MiuraBuilder + MiuraTransformer classes?

## Left off at

got the debug_vector function working. now debug what the dx, dy vectors are doing everywhere

---

## Development Environment Setup

1. Install the [Blender Development extension by Jacques Lucke](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)

2. Open the command palette with `ctrl+shift+P` and search `blender`

3. Run ` Blender: New Addon` and then `Blender: Start`

    - if there is a privilege-related error and Blender crashes, run
      `"C:\PATH_TO_BLENDER\Blender Foundation\Blender 2.93\2.93\python\bin\python.EXE" -m pip install --upgrade --force-reinstall debugpy click flask`, and then try again.

4. To easily enable intellisense, run `pip install fake-bpy-module-2.93`

## Links

https://hal-enpc.archives-ouvertes.fr/hal-01978795/document

nurbs for polynomial meshes

https://docs.blender.org/manual/en/latest/animation/constraints/transform/limit_distance.html
try constraining edges
