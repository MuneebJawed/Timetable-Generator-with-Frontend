from flask import Flask, send_file, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COURSE_FILE = 'courses_info.txt'
TIMETABLE_HTML = 'timetable.html'  # File for saving the generated timetable
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('index-2.html')  # Serve the frontend HTML

@app.route('/upload-courses', methods=['POST'])
def upload_courses():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], COURSE_FILE))
        return jsonify({"message": "File uploaded successfully"}), 200
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/generate-timetable', methods=['POST'])
def generate_timetable():
    data = request.get_json()
    print(f"Received Data: {data}")  # Log the data received from the frontend
    
    courses = data.get('courses', [])  # Get the courses list sent from frontend

    if not courses:
        return jsonify({"error": "No courses received"}), 400
    
    timetable_html = "<h3>Generated Timetable</h3><table><tr><th>Course</th><th>Instructor</th><th>Credit Hours</th><th>Lecture Hall</th><th>Days</th></tr>"
    
    for course in courses:
        days = ", ".join(course['days'])
        timetable_html += f"<tr><td>{course['name']}</td><td>{course['instructor']}</td><td>{course['creditHours']}</td><td>{course['lectureHall']}</td><td>{days}</td></tr>"
    
    timetable_html += "</table>"

    # Save the timetable to a file
    with open(TIMETABLE_HTML, 'w') as f:
        f.write(timetable_html)
    
    return timetable_html


@app.route('/view-timetable', methods=['GET'])
def view_timetable():
    if os.path.exists(TIMETABLE_HTML):
        return send_file(TIMETABLE_HTML)
    return jsonify({"error": "Timetable file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
