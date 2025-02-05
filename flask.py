from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

def connect_to_server(server_ip, username, password, command):
    try:
        #create an SSH client
        client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #connect to the server 
        client.connect(server_ip, username=username, password=password)

        #Execute a command
        stdin, stdout, stderr = client.exec_command(command=command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        client.close()

    except Exception as e:
        return None, str(e)

@app.route('/run_command', methods=['POST'])
def run_command():
    data = request.json
    server_ip = data.get("server_ip")
    username = data.get("username")
    password = data.get("password")
    command  = data.get("command")

    #Check for missing required data
    if not server_ip or not username or not password:
        return jsonify({
            "error" : "Pleas provide remot_ip, username, password"
        }), 400
    output, error = connect_to_server(server_ip,username,password,command)

    if error:
        return jsonify({"error" : error}), 500
    
    return jsonify({"output" : output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", post =5000)
    