from tflite_runtime.interpreter import Interpreter
import azure.functions as func
import time
import cv2
import numpy as np
import base64

interpreter = Interpreter("Azure-TFlite/model.tflite")
interpreter.allocate_tensors()

input_size = 192

KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}
KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def movenet(input_image):
  # TF Lite format expects tensor type of uint8.
  input_image = np.array(input_image, dtype="uint8")
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
  interpreter.set_tensor(input_details[0]['index'], input_image)
  # Invoke inference.
  interpreter.invoke()
  # Get the model prediction.
  keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
  return keypoints_with_scores

def keypoints_and_edges_for_display(keypoints_with_scores, height, width, keypoint_threshold=0.11):
  keypoints_all = []
  keypoint_edges_all = []
  edge_colors = []
  num_instances, _, _, _ = keypoints_with_scores.shape
  for idx in range(num_instances):
    kpts_x = keypoints_with_scores[0, idx, :, 1]
    kpts_y = keypoints_with_scores[0, idx, :, 0]
    kpts_scores = keypoints_with_scores[0, idx, :, 2]
    kpts_absolute_xy = np.stack(
        [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
    kpts_above_thresh_absolute = kpts_absolute_xy[
        kpts_scores > keypoint_threshold, :]
    keypoints_all.append(kpts_above_thresh_absolute)

    for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
      if (kpts_scores[edge_pair[0]] > keypoint_threshold and
          kpts_scores[edge_pair[1]] > keypoint_threshold):
        x_start = kpts_absolute_xy[edge_pair[0], 0]
        y_start = kpts_absolute_xy[edge_pair[0], 1]
        x_end = kpts_absolute_xy[edge_pair[1], 0]
        y_end = kpts_absolute_xy[edge_pair[1], 1]
        line_seg = np.array([[x_start, y_start], [x_end, y_end]])
        keypoint_edges_all.append(line_seg)
        edge_colors.append(color)
  if keypoints_all:
    keypoints_xy = np.concatenate(keypoints_all, axis=0)
  else:
    keypoints_xy = np.zeros((0, 17, 2))

  if keypoint_edges_all:
    edges_xy = np.stack(keypoint_edges_all, axis=0)
  else:
    edges_xy = np.zeros((0, 2, 2))
  return keypoints_xy, edges_xy, edge_colors
def main(req: func.HttpRequest) -> func.HttpResponse:
    image = req.get_body()  # raw data with base64 encoding
    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    y, x, _ = img.shape
    color = (0, 255, 0)

    tf_img = cv2.resize(img, (192,192))
    tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2RGB)
    tf_img = np.asarray(tf_img)
    tf_img = np.expand_dims(tf_img,axis=0)

    # Run model inference.
    outputs = movenet(tf_img)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints = outputs

    (keypoint_locs, keypoint_edges, edge_colors) = keypoints_and_edges_for_display(keypoints,img.shape[0],img.shape[1])

    for xy in keypoint_edges:
        [x1,y1] = xy[0]
        [x2,y2] = xy[1]
        [x1,y1] = [int(x1),int(y1)]
        [x2,y2] = [int(x2),int(y2)]
        img = cv2.line(img, (x1,y1), (x2,y2), color, 2)

    # iterate through keypoints
    for k in keypoints[0,0,:,:]:
        if k[2] > .3:
            yc = int(k[0] * y)
            xc = int(k[1] * x)
            img = cv2.circle(img, (xc, yc), 2, (0, 255, 0), 10)

    tf_img = cv2.resize(img, (x,y))

    # Shows image
    retval, buffer = cv2.imencode('.jpg', tf_img)
    jpg_as_text = base64.b64encode(buffer)
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <img src="data:image/jpg;base64,{jpg_as_text.decode()}" alt="Red dot" />
        </div>
    </body>
    </html>
    """
    return func.HttpResponse(jpg_as_text.decode())
    #return func.HttpResponse(html)