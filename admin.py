from flask import Flask, render_template, jsonify, request, send_file, g
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('server.log')
app.logger.addHandler(handler)

logs = []

# Store the previous logs to avoid duplicates in either way
app.config['previous_logs'] = ''

@app.route('/')
def home():
    log_request_info()
    logs = read_logs()
    return render_template('index.html', logs=logs)

@app.route('/refresh_logs')
def refresh_logs():
    current_logs = read_logs()
    new_logs = get_new_logs(current_logs)
    return jsonify(logs=new_logs)

@app.route('/download_logs')
def download_logs():
    log_request_info()
    logs = read_logs()
    write_logs_to_file(logs)
    return send_file('server.log', as_attachment=True)

@app.route('/clear_logs')
def clear_logs():
    log_request_info()
    with open('server.log', 'w'):
        pass
    return "Logs cleared."

@app.route('/login')
def login():
    log_request_info() 
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    log_request_info() 
    return render_template('admin.html')

@app.route('/<path:path>')
def handle_nonexistent_path(path):
    log_request_info() 
    if not path.startswith('static/'):
        return render_template('404.html')
    return 'Not Found', 404

def read_logs():
    with open('server.log', 'r') as file:
        logs = file.read()
    return logs

def write_logs_to_file(logs):
    with open('server.log', 'w') as file:
        file.write(logs)

def get_new_logs(current_logs):
    previous_logs = app.config['previous_logs']
    if current_logs == previous_logs:
        return None  # No new logs lately

    current_logs_list = current_logs.split('\n')
    previous_logs_list = previous_logs.split('\n')
    new_logs_list = [log for log in current_logs_list if log not in previous_logs_list]
    new_logs = '\n'.join(new_logs_list)

    return new_logs

def log_request_info():
    ip_address = request.remote_addr
    http_method = request.method
    user_agent = request.headers.get('User-Agent')
    query_parameters = dict(request.args)
    log_entry = f'IP: {ip_address} | Method: {http_method} | User-Agent: {user_agent} | Query Params: {query_parameters}'
    app.logger.info(log_entry)
    logs.append(log_entry)

if __name__ == '__main__':
    app.run(debug=False)
