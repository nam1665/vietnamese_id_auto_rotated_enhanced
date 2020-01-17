import base64
from io import StringIO
from io import BytesIO
import sys
import tempfile

MODEL_BASE = '/opt/models/research'
sys.path.append(MODEL_BASE)
sys.path.append(MODEL_BASE + '/object_detection')
sys.path.append(MODEL_BASE + '/slim')

from flask_wtf.file import FileField
import numpy as np
from PIL import Image
from PIL import ImageDraw
import tensorflow as tf
from object_detection.utils import label_map_util
from wtforms import Form
from wtforms import ValidationError


# @app.before_request
# @requires_auth
# def before_request():
#   pass


PATH_TO_CKPT = './inference_graph/frozen_inference_graph.pb'
PATH_TO_LABELS = './inference_graph/labelmap.pbtxt'

content_types = {'jpg': 'image/jpeg',
                 'jpeg': 'image/jpeg',
                 'png': 'image/png'}
extensions = sorted(content_types.keys())


def is_image():
  def _is_image(form, field):
    if not field.data:
      raise ValidationError()
    elif field.data.filename.split('.')[-1].lower() not in extensions:
      raise ValidationError()

  return _is_image


class PhotoForm(Form):
  input_photo = FileField(
      'File extension should be: %s (case-insensitive)' % ', '.join(extensions),
      validators=[is_image()])


class ObjectDetector(object):

  def __init__(self):
    self.detection_graph = self._build_graph()
    self.sess = tf.Session(graph=self.detection_graph)

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True)
    self.category_index = label_map_util.create_category_index(categories)

  def _build_graph(self):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    return detection_graph

  def _load_image_into_numpy_array(self, image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

  def detect(self, image):
    image_np = self._load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)

    graph = self.detection_graph
    image_tensor = graph.get_tensor_by_name('image_tensor:0')
    boxes = graph.get_tensor_by_name('detection_boxes:0')
    scores = graph.get_tensor_by_name('detection_scores:0')
    classes = graph.get_tensor_by_name('detection_classes:0')
    num_detections = graph.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = self.sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    boxes, scores, classes, num_detections = map(
        np.squeeze, [boxes, scores, classes, num_detections])

    return boxes, scores, classes.astype(int), num_detections


def draw_bounding_box_on_image(image, box, color='red', thickness=4):
  draw = ImageDraw.Draw(image)
  im_width, im_height = image.size
  ymin, xmin, ymax, xmax = box
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
  draw.line([(left, top), (left, bottom), (right, bottom),
             (right, top), (left, top)], width=thickness, fill=color)

  return (left, right, top, bottom)



def encode_image(image):
  # image_buffer = BytesIO()
  # image.save(image_buffer, format='PNG')
  # imgstr = 'data:image/png;base64,{:s}'.format(
  #     base64.b64encode(image_buffer.getvalue()))
  # return imgstr

  buff = BytesIO()
  image.save(buff, format="JPEG")
  imgstr = base64.b64encode(buff.getvalue())
  return imgstr

def detect_objects(image_path):
  image = Image.open(image_path).convert('RGB')
  boxes, scores, classes, num_detections = client.detect(image)
  width, height = image.size
  # image.thumbnail((480, 480), Image.ANTIALIAS)
  coordinate_array = []
  new_images = {}
  data = {}
  for i in range(0, int(num_detections)):
    if scores[i] < 0.8: continue
    cls = classes[i]
    name = ""
    if cls not in new_images.keys():
      new_images[cls] = image.copy()
    coordinate = draw_bounding_box_on_image(new_images[cls], boxes[i],
                               thickness=int(scores[i]))

    if (cls == 1):
      name = "person"
    if (cls == 2):
      name = "text"
    if (cls == 3):
      name = "logo"
    if (cls == 4):
      name = "all"

    data["class"] = name
    data["coordinate"] = coordinate

    coordinate_array.append(data.copy())
  # result = {}
  # result['original'] = encode_image(image.copy())
  #
  # for cls, new_image in new_images.items():
  #   category = client.category_index[cls]['name']
  #   result[category] = encode_image(new_image)
  #   with open(category + ".jpg", "wb") as fh:
  #     fh.write(base64.decodebytes(result[category]))
  return coordinate_array

client = ObjectDetector()
