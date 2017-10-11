from pictureflow.output import DiskOutput
from pictureflow.transform import FitToSize, ObjectDetector, PathMask

import cv2
import pictureflow as pf


imgs = pf.Placeholder(out_type=pf.Image)
# branch_a = PathMask(imgs, pf.Constant(np.array([(400, 600), (600, 800), (600, 800), (400, 800), (400, 600)])))
branch_a = ObjectDetector(imgs, pf.Constant(100), pf.Constant(60))
# branch_a = FitToSize(branch_a, pf.Constant(60))
branch_a = DiskOutput(branch_a, base_path=pf.Constant('data/output/'))

# Load images
# TODO: Disk loader would be _very_ nice for processing datasets
image_1 = pf.Image('image_1', 'jpg', cv2.imread('data/img.jpg'))
image_2 = pf.Image('image_2', 'png', cv2.imread('data/img.png'))

# Declare a new session. (A session is basically a runtime context for a
# previously-defined graph)
with pf.Session({imgs: [image_1, image_2]}) as sess:
    output = sess.run_sync(branch_a)
