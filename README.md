# Cloud-Image-Processing-System
## Overview
This system allows users to upload images through a web-based graphical user interface (GUI), processes the images using a distributed architecture on Microsoft Azure, and returns the processed images along with the identifier of the Virtual Machine (VM) that processed each image.

## Architecture
1. **User Server**
    - **`gui.py`**: A Flask server that renders the GUI and handles image upload requests.
2. **Azure Load Balancer**
    - Distributes incoming image processing requests to one of the three VMs.
3. **Virtual Machines (VMs)**
    - **`inter.py`**: A small server running on each VM that receives image processing requests from the Load Balancer.
    - **`worker_thread.py`**: Processes the images using worker threads on each VM.

## Components

### User Server
- **`gui.py`**:
    - Renders the GUI for users to upload images.
    - Forwards image upload requests to the Azure Load Balancer.
    - Displays processed images and the VM identifier that processed them.

### Virtual Machines (VMs)
- **`inter.py`**:
    - Listens for image processing requests from the Load Balancer.
    - Interfaces with `worker_thread.py` to process images.
    - Sends processed images and VM identifiers back to the User Server.

- **`worker_thread.py`**:
    - Utilizes worker threads to process images concurrently.
    - Contains the logic and algorithms for image processing.

## Setup and Deployment

### Prerequisites
- Microsoft Azure account.
- SSH keys for VM access.
- Python and required libraries
 ## [Report](https://drive.google.com/file/d/1SQbLaUtPxo1kSRA5dUp3MmumH69D_QIF/view?usp=sharing)
 ## [Video](https://drive.google.com/file/d/1oo0HFmXl2moJbayZ8VlJPpC01bpS-nnc/view?usp=sharing)
