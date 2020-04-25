# moonDistance
Downloads the 1122 images from the distance folder at NASA
Added scaling to 1920x1080

[![video](https://img.youtube.com/vi/D48lmI_Sb28/0.jpg)](https://youtu.be/D48lmI_Sb28)

# moonOrbit
Downloads the 999 images from the orbit folder
Added scaling to 1920x1080

[![video](https://img.youtube.com/vi/xIVGC1HEWyU/0.jpg)](https://youtu.be/xIVGC1HEWyU)

# himawari
Downloads the 2500 lates images from himawari sattellite. This code is uglier since some pictures are missing,
and ffmpeg crashes if images are missing
Added scaling to 1920x1080

[![video](https://img.youtube.com/vi/IstgFh7EE6Y/0.jpg)](https://www.youtube.com/watch?v=IstgFh7EE6Y)

# moonPhase
Downloads 8762 photos of the moon from a NASA website and uses them to create a fluid animation (click):

[![video](https://img.youtube.com/vi/0tjY13kYnZs/0.jpg)](https://youtu.be/0tjY13kYnZs)

See [here for an introduction/tutorial](https://nicholasfarrow.com/Creating-a-Moon-Animation-Using-NASA-Images-and-Python/).

Added scaling to 1366x768
# Usage
```
python moonphase.py
```

```
optional arguments:
  -h, --help            show this help message and exit
  -t THINNING, --thinning THINNING
                        Frequency of images to download, e.g. every 10th image
  -f, --ffmpeg          Use ffmpeg to create video
```

If you are creating a gif via imageio then creating a `.gif` of 8761 images could take a long time and create a >100Mb file. Try using a smaller number of images with the `-t` flag:

Eg. use every 20th image:
```
python moonphase.py -t 20
```

If you are on a unix OS and have ffmpeg installed then you can compile an `.mp4` instead of a `.gif`:
```
python moonphase.py -f
```
