# PictureFlow

PictureFlow is an image processing library that aims to simplify the way we think about modifying images. It depends on [OpenCV](http://opencv.org/) for most image manipulation tasks, altough we have plans to support more backends in the future. We currently only support Python 3.6+, but efforts to make the project compatible with 2.7+ and < 3.6 are very welcome!



## Installation

### Via `pip`

```shell
$ pip install pictureflow
```



### Manually

```shell
$ git clone git@github.com:mentum/pictureflow.git
$ cd pictureflow
$ python setup.py install
```



## Example

```python
from pictureflow.output import DiskOutput
from pictureflow.transform import ColorMask, Convert, Rotate, Scale

import cv2
import pictureflow as pf

# Define some placeholders that will form the root of our transformation graph
imgs = pf.Placeholder(out_type=pf.Image)
angle = pf.Placeholder(out_type=int)

# This branch will reduce the image to 20% of its original size, convert it to RGB & write it to the 'output/' directory
branch_a = Scale(imgs, scale_factor=pf.Constant(0.2))
branch_a = Convert(branch_a, src=pf.Constant('bgr'), dest=pf.Constant('rgb'))
branch_a = DiskOutput(branch_a, base_path=pf.Constant('output/'))

# This branch will rotate the image by variable angles (fed with the session context),
# will filter-out the red color, and will write it to the 'other/' directory.
branch_b = Rotate(imgs, rot_angle=angle)
branch_b = ColorMask(branch_b, color_mask=pf.Constant([None, None, 0]))
branch_b = DiskOutput(branch_b, base_path=pf.Constant('other/'))

# Load images
image_1 = pf.Image('image_1', 'jpg', cv2.imread('pic.jpg'))
image_2 = pf.Image('image_2', 'jpg', cv2.imread('pic2.jpg'))

# Declare a new session. (A session is basically a runtime context for a
# previously-defined graph)
with pf.Session({imgs: [image_1, image_2], angle: [90, 180]}) as sess:
    output = sess.run_sync(branch_a)

    for item in sess.run(branch_b):
        print(item.id)
```



## Requirements

* Python 3.6