from pictureflow.flow import Broadcast, Combine
from pictureflow.output import DiskOutput
from pictureflow.transform import Rotate, Scale

import cv2
import pictureflow as pf


inpt = pf.Placeholder(out_type=pf.Image)

broadcast = Broadcast(inpt, pf.Constant(2))

branch_a = Rotate(broadcast, rot_angle=pf.Constant(90))
branch_b = Scale(broadcast, scale_factor=pf.Constant(0.1))

graph = Combine(branch_a, branch_b)

graph = DiskOutput(graph, base_path=pf.Constant('data/output/'))

# Load images
# TODO: Disk loader would be _very_ nice for processing datasets
image_1 = pf.Image('image_1', 'jpg', cv2.imread('data/in.jpg'))

# Declare a new session. (A session is basically a runtime context for a
# previously-defined graph)
with pf.Session({inpt: [image_1]}) as sess:
    output = sess.run_sync(graph)
