import threading
import queue
import cv2  # OpenCV for image processing
from mpi4py import MPI  # MPI for distributed computing
import numpy as np
import matplotlib.pyplot as plt

class WorkerThread(threading.Thread):
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.result = None  # Variable to store processed result

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break

            image, operation = task
            result = self.process_image(image, operation)
            self.comm.send(result, dest=0)

    def process_image(self, image, operation):
        # Load the image
        # img = cv2.imread(image, cv2.IMREAD_COLOR )

        # Perform the specified operation
        if operation == 'edge_detection':
            result = cv2.Canny(image, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(image)  # Add more operations as needed...
        
        return result




def processImage (image,op):
    task_queue = queue.Queue()

    # Instantiate WorkerThread
    worker_thread = WorkerThread(task_queue)

    # Add image processing task to the queue
    image_path = image
    operation =op  # Specify the desired operation
    task_queue.put((image_path, operation))

    # Start WorkerThread
    worker_thread.start()


    if MPI.COMM_WORLD.Get_rank() == 0:  # Only master node receives result
        processed_result = MPI.COMM_WORLD.recv(source=0)
        return processed_result
    else:
        return None