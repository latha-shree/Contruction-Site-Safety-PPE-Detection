from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import os, cv2, time, requests
from datetime import datetime
from ultralytics import YOLO
import pyttsx3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

model = YOLO('best.pt')
classNames = model.names

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''

def send_telegram_alert(missing_items, mode=''):
    if not missing_items:
        return
    if isinstance(missing_items, str):
        missing_items = [missing_items]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"🚨 *PPE Violation Detected ({mode})*\n"
        f"⚠️ *Missing Items:* {', '.join(missing_items)}\n"
        f"👷 Please inform workers to wear proper safety equipment.\n"
        f"📅 *Time:* {timestamp}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
        print("📤 Telegram message sent.")
    except Exception as e:
        print("❌ Telegram send failed:", e)

def speak_warning(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except:
        print("❌ pyttsx3 failed")

        
@app.route('/')
def home():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin123':
        session['admin'] = True
        return redirect('/dashboard')
    flash('Invalid credentials!', 'danger')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

"""@app.route('/image-detect', methods=['GET', 'POST'])
def image_detect_page():
    if not session.get('admin'):
        return redirect('/')
    
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            from detection import detect_ppe
            result_img_path, missing_items = detect_ppe(filepath)
            if isinstance(missing_items, str):
                missing_items = [missing_items]
            if missing_items:
                send_telegram_alert(missing_items, mode='Image')
            return render_template('result.html', image=result_img_path, violations=missing_items)
        flash("Please upload a valid image.", "warning")
    return render_template('image_detect.html')"""


"""@app.route('/image-detect', methods=['GET', 'POST'])
def image_detect_page():
    if not session.get('admin'):
        return redirect('/')

    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Run detection
            from detection import detect_ppe
            result_img_path, missing_items = detect_ppe(filepath)

            # Extract only relative path for HTML
            result_filename = os.path.basename(result_img_path)
            relative_path = f"processed/{result_filename}"

            # Ensure missing_items is a list
            if isinstance(missing_items, str):
                missing_items = [missing_items]

            # ✅ Send Telegram alert
            if missing_items:
                print("📤 Sending Telegram message...")
                send_telegram_alert(missing_items, mode='Image')

            return render_template('result.html', image=relative_path, violations=missing_items)

        flash("Please upload a valid image.", "warning")

    return render_template('image_detect.html')
"""

@app.route('/image-detect', methods=['GET', 'POST'])
def image_detect_page():
    if not session.get('admin'):
        return redirect('/')

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            from detection import detect_ppe
            result_img_path, missing_items = detect_ppe(filepath)

            # ✅ Ensure correct relative path to /static/
            result_filename = os.path.basename(result_img_path)
            relative_path = f"processed/{result_filename}"

            if isinstance(missing_items, str):
                missing_items = [missing_items]

            if missing_items:
                print("📤 Sending Telegram alert...")
                send_telegram_alert(missing_items, mode='Image')

            return render_template('result.html', image=relative_path, violations=missing_items)

        flash("Please upload a valid image.", "warning")

    return render_template('image_detect.html')

@app.route('/video-detect', methods=['GET', 'POST'])
def video_detect():
    if not session.get('admin'):
        return redirect('/')
    
    if request.method == 'POST':
        file = request.files['video']
        if file:
            filename = file.filename
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)

            processed_path, alert_msg, alarm = detect_and_preview(input_path)
            session['video_file'] = os.path.basename(processed_path)
            session['message'] = alert_msg
            session['alarm'] = alarm
            violations = [v.strip().replace(" missing", "") for v in alert_msg.split(',') if "missing" in v]
            session['violations'] = violations

            print("📌 Final Violations:", violations) 
            if alarm:
                send_telegram_alert(violations, mode="Video")
            return redirect('/video-result')
    return render_template('video_detect.html')

@app.route('/video-result')
def video_result():
    video_filename = session.get('video_file')
    if not video_filename:
        flash("No video processed yet.", "danger")
        return redirect('/video-detect')

    message = session.get('message', '')
    alarm = session.get('alarm', False)
    violations = session.get('violations', [])
    if isinstance(violations, str):
        violations = [violations]

    return render_template('video_result.html', 
                           video_file=video_filename,
                           message=message,
                           alarm=alarm,
                           violations=violations)

@app.route('/camera-detect')
def camera_detect():
    return render_template('realtime_detect.html')

@app.route('/start-realtime')
def start_realtime():
    return render_template("realtime_detect_live.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    cap = cv2.VideoCapture(0)
    alerts_sent = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, stream=True)
        violations = set()
        alarm = False

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = classNames[cls]
                color = (0, 255, 0)

                if label.startswith("NO-"):
                    color = (0, 0, 255)
                    violations.add(label.replace("NO-", ""))
                    alarm = True

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if alarm and not alerts_sent:
            send_telegram_alert(list(violations), mode="Real-Time")
            speak_warning("⚠️ " + ", ".join(violations) + " missing. Wear safety gear.")
            alerts_sent = True

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def detect_and_preview(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Error opening video", False

    output_path = os.path.join(PROCESSED_FOLDER, 'processed_' + os.path.basename(video_path))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    alerts = set()
    alarm = False
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = classNames[cls]
                color = (0, 255, 0)

                if label.startswith("NO-"):
                    color = (0, 0, 255)
                    alerts.add(f"{label.replace('NO-', '')} missing")
                    alarm = True

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        out.write(frame)
        cv2.imshow("🔍 PPE Detection Preview", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time > 20):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    message = ', '.join(alerts) if alerts else "✅ All PPE worn correctly."
    return output_path, message, alarm

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
