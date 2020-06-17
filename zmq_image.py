import numpy as np
import zmq
import base64
import json
from json import JSONEncoder
import io
from skimage.feature import blob_dog


from PIL import Image

def set_up_host():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    return socket




def send_to_client(socket):
    request = socket.recv()
    if request:
        print("Received request")
        img = None
        err = None
        out_str="Image error,not a valid image"
        try:
            buf = Image.open(io.BytesIO(request)).convert('LA')
            img = np.array(buf)

        except Exception as e: 
            print("Image file not understood!")
            err = e
        if img is not None:
            err="All is okay"
            pass
            out_dict = {"error" : err, "output" : img.shape}

       
            out_str = json.dumps(out_dict,cls=NumpyArrayEncoder) 
        
        socket.send_json(out_str)
        print("send respond")

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

if __name__ == "__main__":
    socket = set_up_host()
    while True:
        try:
            send_to_client(socket)
        except KeyboardInterrupt:
            break
