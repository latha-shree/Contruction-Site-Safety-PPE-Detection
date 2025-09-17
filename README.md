👷 Construction Site Safety PPE Detection

This project focuses on ensuring workplace safety by automatically detecting Personal Protective Equipment (PPE) such as helmets, safety vests, and gloves on construction sites using Artificial Intelligence and Computer Vision.

The system leverages Deep Learning models (YOLOv4/YOLOv5) along with OpenCV to perform real-time object detection. A Tkinter-based GUI is also provided for easy interaction, supporting detection from images, video files, and live webcam feeds.

🚀 Features

Detects PPE items (Helmet, Vest, Gloves) in real-time

Supports detection from:

📷 Images

🎥 Video files

📡 Live webcam

Tkinter GUI for a user-friendly interface

Provides visual feedback with bounding boxes around detected PPE

Can be deployed on edge devices (Jetson Nano, Raspberry Pi) for on-site monitoring

🛠️ Tech Stack

Programming Language: Python

Deep Learning Models: YOLOv4, YOLOv5

Libraries & Tools: OpenCV, TensorFlow/Keras, NumPy, Pandas, Matplotlib, Tkinter

Hardware Support: Jetson Nano / Raspberry Pi (for edge deployment)

📂 Project Structure
PPE-Detection/
│── dataset/              # Training dataset
│── yolo/                 # YOLO model config & weights
│── gui.py                # Tkinter GUI for detection
│── detect.py             # Script for image/video/webcam detection
│── requirements.txt      # Dependencies
│── README.md             # Documentation

⚙️ Installation & Requirements

Clone the repository:

git clone https://github.com/your-username/PPE-Detection.git
cd PPE-Detection


Install dependencies:

pip install -r requirements.txt


Run detection:

python detect.py


Launch GUI:

python gui.py

📌 Future Enhancements

Improve detection accuracy using YOLOv8

Extend support for additional PPE (e.g., goggles, masks)

Cloud/Edge integration for real-time monitoring dashboards


![homepage](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/homepage.png)
![login](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/admin_login.png)
![image](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/image_detection.png)
![image_result](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/image_result.png)
![video](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video.png)
![video_result](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video_result1.png)
![video2](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video_result2.png)

