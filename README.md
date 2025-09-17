👷 Construction Site Safety PPE Detection

An AI-based system for real-time monitoring of Personal Protective Equipment (PPE) such as helmets, vests, and gloves. The system uses YOLO object detection and OpenCV to identify violations from images, videos, and live camera feeds. It also provides Telegram alerts and voice warnings to ensure worker safety.

🚀 Features

📷 Image Detection – Upload images to detect PPE violations

🎥 Video Detection – Upload videos and process PPE compliance

📡 Real-time Camera Detection – Live monitoring with YOLO + OpenCV

📢 Alerts

Telegram notifications to supervisors

Voice warnings for missing PPE items

🔐 Admin Login – Secure dashboard access

🛠️ Tech Stack

Backend: Flask

Model: YOLOv8 / YOLO (Ultralytics)

Libraries: OpenCV, NumPy, Pandas, TensorFlow/Keras, pyttsx3

Notifications: Telegram Bot API

Frontend: HTML, CSS, Bootstrap (templates)

📂 Project Structure
PPE-Detection/
│── app.py               # Main Flask application
│── detection.py         # Detection logic (YOLO + OpenCV)
│── static/uploads/      # Uploaded images & videos
│── static/processed/    # Processed detection outputs
│── templates/           # HTML templates
│── best.pt              # YOLO trained weights
│── requirements.txt     # Project dependencies
│── README.md            # Documentation

⚙️ Installation & Setup

Clone the repository:

git clone https://github.com/your-username/PPE-Detection.git
cd PPE-Detection


Install dependencies:

pip install -r requirements.txt


Add your YOLO model weights (e.g., best.pt) inside the project folder.

Configure Telegram Bot (in app.py):

Replace TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID with your credentials.

Run the Flask app:

python app.py


Open in browser:

http://127.0.0.1:5000/

📌 Future Enhancements

Add detection for more PPE items (goggles, masks, boots)

Cloud/Edge deployment (Jetson Nano, Raspberry Pi)

Centralized dashboard for multiple cameras


![homepage](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/homepage.png)
![login](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/admin_login.png)
![image](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/image_detection.png)
![image_result](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/image_result.png)
![video](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video.png)
![video_result](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video_result1.png)
![video2](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/video_result2.png)
![real](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/real.png)
![real1](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/real1.png)
![tele](https://github.com/latha-shree/Contruction-Site-Safety-PPE-Detection/blob/main/telegram.jpg)
