from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for demonstration purposes
courses = []
enrollments = {}

# Authentication
# Implement authentication logic here

# Course Management Routes
@app.route('/create_course', methods=['POST'])
def create_course():
    data = request.json
    course_name = data.get('course_name')
    teacher_id = data.get('teacher_id')
    # Create course logic here
    course = {'course_name': course_name, 'teacher_id': teacher_id}
    courses.append(course)
    return jsonify({'message': 'Course created successfully'})

@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    # Enroll in course logic here
    enrollments.setdefault(student_id, []).append(course_id)
    return jsonify({'message': 'Enrolled in course successfully'})

@app.route('/drop_course', methods=['POST'])
def drop_course():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    # Drop course logic here
    enrollments.get(student_id, []).remove(course_id)
    return jsonify({'message': 'Dropped course successfully'})

if __name__ == '__main__':
    app.run(debug=True)
