# 3D Screenshot to 3D-Model
Quick Python script to transform screenshots of 3D movies into a 3D meshes. See https://shkspr.mobi/blog/2018/04/reconstructing-3d-models-from-the-last-jedi for more details.

## Usage

`python3 screenshot_to_mesh.py screenshot.png`

Will output a 3D mesh in PLY format.

## Demo
From this screenshot:

![Screenshot from the movie Finding Nemo. Two fish are swimming in the ocean.](https://raw.githubusercontent.com/edent/3D-Screenshot-to-3D-Model/master/samples/Finding_Nemo_01.png)

To this mesh:
![The scheenshot is now in 3D. The fishes float away from the background.](https://user-images.githubusercontent.com/837136/38454786-dd26d8ee-3a65-11e8-94c9-a8b65c27df00.png)

From this screenshot:
![Screenshot from the short film Paperman. A man stands in front of a post box.](https://raw.githubusercontent.com/edent/3D-Screenshot-to-3D-Model/master/samples/Paperman_1.png)

To this mesh:
![The scheenshot is now in 3D.](https://user-images.githubusercontent.com/837136/38456341-9e62b2ac-3a7b-11e8-933b-0f9898fbce2b.png)

From this screenshot:
![Screenshot from the movie Resident Evil: Retribution. People are crammed in a corridor.](https://raw.githubusercontent.com/edent/3D-Screenshot-to-3D-Model/master/samples/Resident_Evil_Retribution_1.png)

To this mesh:
![The scheenshot is now in 3D.](https://user-images.githubusercontent.com/837136/38456251-90c490a8-3a7a-11e8-81ee-ae16c780bc4e.png)


## Requirements

The code runs quickly, even on older hardware. It should take less than a minute to generate a mesh, even on a modest machine.

In order to run the software, you will need:

* Python3
* [PyntCloud](https://github.com/daavoo/pyntcloud)
* [Pandas](https://pandas.pydata.org/)
* [NumPy](http://www.numpy.org/)
* [OpenCV](https://pypi.python.org/pypi/opencv-python)
* [OpenCV Contrib](https://pypi.python.org/pypi/opencv-contrib-python)
* [Pillow](https://pypi.python.org/pypi/Pillow/)
* [numba](https://numba.pydata.org/)

## Copyright
This code is BSD. Please [check the LICENSE file for contributors](https://github.com/edent/3D-Screenshot-to-3D-Model/blob/master/LICENSE).

### Screenshots
The screenshots in the `samples` folder fall under the UK's "Fair Dealing" exception.  They are for the purposes of private study, data mining for non-commercial research, and for criticism & review of 3D movies.

* [Doctor Who - The Day of the Doctor](https://www.imdb.com/title/tt2779318/) is © BBC
* [Star Wars - The Last Jedi](https://www.imdb.com/title/tt2527336/) is © LucasFilm Ltd
* [Finding Nemo](https://www.imdb.com/title/tt0266543/) is © Disney / Pixar
* [Dial M For Murder](https://www.imdb.com/title/tt0046912/) is © Warner Bros
* [Creature From The Black Lagoon](https://www.imdb.com/title/tt0046876/) is © Universal Pictures
* [Piranha 3DD](https://www.imdb.com/title/tt1714203/) is © Dimension Films
* [Paperman](https://www.imdb.com/title/tt2388725/) is © Disney
* [Resident Evil: Retribution](https://www.imdb.com/title/tt1855325/) is © Sony Pictures 
* [Planet Dinosaur](https://www.imdb.com/title/tt1998816/) is © Jellyfish Pictures
* [House of Wax](https://www.imdb.com/title/tt0045888/) is © Warner Bros
* [Kiss Me Kate](http://www.imdb.com/title/tt0045963/) is © MGM
* LG content from their 3D demo videos