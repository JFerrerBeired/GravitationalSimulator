# GRAVITATIONAL SIMULATOR

## What is this?
This is a personal project that I'm developing in python with pygame support to get used to them (being my first project in such platform). My objective is to learn as much as I can while developing something fun and interesting and to develop some basic tools that I can reuse in future projects.

It will be an interactive sandbox-like environment that simulates the gravitational attraction of the objects.

## How to use
- Click and drag to set the radius of the object (mass is proportional to its cubic power) then you can choose the initial velocity (right-clicking sets it to zero).

- Press space to delete all objects (they are deleted automatically when too far away).

- Most of the parameters can be changed in the *constants.py* file

## Task List
- ~~A Draw mode that allows you to initialize the position, size (mass) and velocity of the objects.~~

- ~~First-order simulation algorithm.~~

- Calculating collisions.

- Different reference frames.
	- Center of mass
	- Fixed in a particular object

- Dinamic screen.
	- Scrollable so you can move to other locations
	- Zoomable, recalculating the radii of the objects but conserving its mass

- Past trajectories are shown in the background.

- Development of some GUI that allows.
    - Interactive buttons
    - Scroll bars
    - Dropdown menus
    - Maybe more?

- Different objects possible (stars, planets, comets...) with different simulation properties and graphical differences to try as many interesting tools with pygame as possible. Maybe some blur to the stars and a particle generation for the comet tail.

- Statistics of the temporal evolution of important quantities (total angular momentum, total energy, number of bodies, distance or relative angule between two objects...)

- Option to show the gravitational potential as a colour map in the background and/or contour lines of equal potential.

- Higher-order simulation algorithms (Runge-Kutta) for better accuracy.

## Some other random ideas

- Predefined starting scenarios that show interesting or cool chaotic behaviour.

- If the energy of a collision is enough it can "break" the planet and generate a new one.

- Add an atmosphere thickness parameter that slows down other objects if they get in contact with it.
