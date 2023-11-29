from scipy.spatial import distance as dist
import numpy as np

"""

Takes a dlib-predicted bounding rectangle and converts it to the format:
  (x, y, w, h) 
to make it work with OpenCV

"""
def to_bounding(rect):
  x = rect.left()
  y = rect.top()
  w = rect.right() - x
  h = rect.bottom() - y

  return (x, y, w, h)

def landmarks_to_np(shape, dtype="int"):
  coords = np.zeros((68, 2), dtype=dtype) # List of (x, y) coordinates

  # Convert each facial landmark to a coordiate
  for i in range(0, 68):
    coords[i] = (shape.part(i).x, shape.part(i).y)

  return coords

def eye_aspect_ratio(eye):
  A = dist.euclidean(eye[1], eye[5])
  B = dist.euclidean(eye[2], eye[4])

  C = dist.euclidean(eye[0], eye[3])

  ear = (A + B) / (2.0 * C)

  return ear