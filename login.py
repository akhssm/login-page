from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import psycopg2

# HTML template for the register page
register_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Register Page</title>
</head>
<body>
    <h2>Register</h2>
    <form method="post" action="/register">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <label for="role">Role:</label><br>
        <select id="role" name="role">
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
        </select><br>
        <input type="submit" value="Register">
    </form>
</body>
</html>
"""

# HTML template for the login page
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post" action="/login">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

# Function to handle the registration process
def register_user(username, password, role):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="akshay@2002",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        if role == 'teacher':
            cur.execute("INSERT INTO teachers (username, password) VALUES (%s, %s)", (username, password))
        elif role == 'student':
            cur.execute("INSERT INTO students (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error inserting user:", e)
        return False

# Function to verify user credentials for login
def verify_login(username, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="akshay@2002",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM teachers WHERE username = %s AND password = %s", (username, password))
        teacher = cur.fetchone()
        if teacher:
            return teacher, 'teacher'
        else:
            cur.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
            student = cur.fetchone()
            if student:
                return student, 'student'
        conn.close()
        return None, None
    except psycopg2.Error as e:
        print("Error verifying login:", e)
        return None, None

# Function to handle HTTP requests
def handle_requests(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    class Handler(handler_class):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(login_page.encode())
            elif self.path == '/register':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(register_page.encode())
            elif self.path == '/login':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(login_page.encode())
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            if self.path == '/register':
                username = params['username'][0]
                password = params['password'][0]
                role = params['role'][0]
                if register_user(username, password, role):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("<h3>Registration successful!</h3>".encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("<h3>Error registering user!</h3>".encode())
            elif self.path == '/login':
                username = params['username'][0]
                password = params['password'][0]
                user, user_type = verify_login(username, password)
                if user:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    if user_type == 'teacher':
                        self.wfile.write("<h3>Welcome Teacher!</h3>".encode())
                    elif user_type == 'student':
                        self.wfile.write("<h3>Welcome Student!</h3>".encode())
                else:
                    self.send_response(401)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("<h3>Invalid username or password!</h3>".encode())
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

    server_address = ('', 8000)
    httpd = server_class(server_address, Handler)
    print('Server running on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    handle_requests()
