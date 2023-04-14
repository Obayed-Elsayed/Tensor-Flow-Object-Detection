from easygui import *

import serial
import os
import tensorflow as tf
import cv2 
import numpy as np
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from google.protobuf import text_format
from matplotlib import pyplot as plt
# my_ssd_mobnet_tuned
# my_lite_640_ssd
CUSTOM_MODEL_NAME = 'my_ssd_mobnet_tuned' 
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'
check_pt = 'ckpt-21'
PORT = 'COM6'
BAUD = 460800

# https://www.geeksforgeeks.org/python-easygui-enter-box/

#
paths = {
    'SCRIPTS_PATH': os.path.join('Tensorflow','scripts'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace','models'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, check_pt), 
 }

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

# /-----------------UI---------------/
# camera_cap = input("Please type the camera number you wish to use, 0 is first cam: \n")
# print(f"Here are the file paths that are being used: \nFor model path: {files['PIPELINE_CONFIG']}\nFor check point path: {paths['CHECKPOINT_PATH']}")
# change_path = input("would you like to change any of the paths above? yb for both, yc for check point yp for model, n for no \n")
response = ["ya","yl","yc","yp","n", "yport"]
# while (change_path not in response):
#     change_path = input("would you like to change any of the paths above? ya for all, yl for label map, yc for check point yp for model, n for no \n")


# message to be displayed
text = "Please type the camera number you wish to use, 0 is first cam"
title = "PC Interactor"
# default text
d_text = ""
  
# creating a enter box
camera_cap = enterbox(text, title, d_text)
  
# title for the message box
title = "Message Box"
  
# creating a message
message = f"you chose : {camera_cap} for cam. Here are the file paths that are being used: \nFor model path: {files['PIPELINE_CONFIG']}\nFor check point path: {paths['CHECKPOINT_PATH']} \nfor label map : {files['LABELMAP']}" 
msg = msgbox(message, title)
# change_path = enterbox(message, title, d_text)

change_message = "would you like to change any of the paths above? ya for all, yl for label map, yc for check point yp for model,yport for pornt change, n for no"
change_path = enterbox(change_message, title, d_text)
while (change_path not in response):
    change_path = enterbox(change_message, title, d_text)
    # change_path = input("would you like to change any of the paths above? ya for all, yl for label map, yc for check point yp for model, n for no \n")


# creating a message box
# msg = msgbox(message, title)

# response functions can be better with dict mapping to response [TODO if time allows]
if(change_path == "n"):
    pass
elif(change_path == "ya"):
    msgbox("pipline / model \n")
    files['PIPELINE_CONFIG'] = fileopenbox()

    msgbox("Labelmap: \n")
    files['LABELMAP'] = fileopenbox()

    msgbox("check point path Directory: \n")
    paths['CHECKPOINT_PATH'] = diropenbox()
    num = enterbox(f"checkpoint number? ","","")
    paths['CHECKPOINT_PATH'] = os.path.join(paths['CHECKPOINT_PATH'], f'ckpt-{num}')

    PORT = enterbox("Enter Port Num: ", title, d_text)
    BAUD = int(enterbox("Enter Baud rate: ", title, d_text))
elif(change_path == "yc"):
    msgbox("check point path Directory: \n")
    paths['CHECKPOINT_PATH'] = diropenbox()
    num = enterbox(f"checkpoint number? ","","")
    paths['CHECKPOINT_PATH'] = os.path.join(paths['CHECKPOINT_PATH'], f'ckpt-{num}')

elif(change_path == "yp"):
    msgbox("pipline / model \n")
    files['PIPELINE_CONFIG'] = fileopenbox()

elif(change_path == "yl"):
    msgbox("label map path: \n")
    files['LABELMAP'] = fileopenbox()
elif(change_path == "yport"):
    PORT = enterbox("Enter Port Num: ", title, d_text)
    BAUD = int(enterbox("Enter Baud rate: ", title, d_text))


program_settings = {'cam':camera_cap, 'label_map':files['LABELMAP'], 'model':files['PIPELINE_CONFIG'],"check point":paths['CHECKPOINT_PATH']}



msgbox(f"Here are the settings you chose: {camera_cap}, label map: {files['LABELMAP']}, model: {files['PIPELINE_CONFIG']}, check point {paths['CHECKPOINT_PATH']}, Port: {PORT} at {BAUD}")
# msgbox(f"Here are the settings you chose: {program_settings}")
def more_certain_detection(q) -> int:
    count_tuples = [[-1,0],[0,0],[1,0],[2,0]]

    for item in q:
        count_tuples[item+1][1] +=1
    count_tuples.sort(key=lambda a: a[1])
    # if the difference in count between -1 and any other isnt too big then we return the other
    if(count_tuples[-1][0] == -1 and (count_tuples[-1][1] - count_tuples[-2][1]) <=1):
        return count_tuples[-2][0]

    return count_tuples[-1][0]

try:
    serial_1 = serial.Serial(port=PORT, baudrate=BAUD,bytesize=8, timeout=0)
    # num = 45

    # to_send = str(num).encode('UTF-8')
    # serial_1.write(to_send)
    # i = 0
    # while(True):
    #     buffer = serial_1.read()
    #     serial_1.write(to_send)
    #     print(i,buffer)
    #     i+=1
except Exception as e:
    print(f"An error: {e} has occurred while opening coms")


def main():
    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
    # Load pipeline config and build a detection model
    configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    # Restore checkpoint (latest model)
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(paths['CHECKPOINT_PATH']).expect_partial()
    # ckpt.restore(paths['CHECKPOINT_PATH'])

    @tf.function
    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        return detections


    cap = cv2.VideoCapture(int(camera_cap))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    det_queue = [-1,-1,-1,-1,-1,-1,-1]
    q_counter = 0
    while cap.isOpened(): 
        ret, frame = cap.read()
        image_np = np.array(frame)
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
        
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,
                    min_score_thresh=.62 ,
                    agnostic_mode=False)

        if(q_counter%7 ==0):
            q_counter = 0
        
        if(detections['detection_scores'][0] >0.65):
            det_queue[q_counter] = detections['detection_classes'][0]
        else:
            det_queue[q_counter] = -1

        q_counter+=1
        
        # SEND UART SIGNAL
        # decision = more_certain_detection(det_queue)
        # print(f" Sending {decision}")
        # try:
        #     serial_1.write(str(decision).encode('UTF-8'))
        # except Exception as e:
        #     print("error while sending: {e}")

        # print(detections['detection_classes'][0])
        # print(detections['detection_scores'][0])
        cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

main()