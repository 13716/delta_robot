from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime
import serial
import time

app = Flask(__name__)

dataa = {
    'heater_bed': {
        'temperature': 31.33,
        'target': 20,
        'power': 0.0
    },
    'toolhead': {
        'homed_axes': '',
        'axis_minimum': [-35.0, -21.0, -10.0, 0.0],
        'axis_maximum': [300.0, 300.0, 320.0, 0.0],
        'print_time': 4589.504179702381,
        'stalls': 0,
        'estimated_print_time': 93324.51044305357,
        'extruder': 'extruder',
        'position': [0, 0, 0, 98.52104],
        'max_velocity': 1500.0,
        'max_accel': 7000.0,
        'minimum_cruise_ratio': 0.0,
        'square_corner_velocity': 5.0
    },
    'gcode_move': {
        'homed_axes': '',
        'speed_factor': 1.0,
        'homing_origin': [0.0, 0.0, 0.0, 0.0],
        'position': [0, 0, 0, 0],
        'gcode_position': [0, 0, 0, 0]
    },
    'fan': {
        'speed': 0.12,
        'rpm': None
    }
}

list_files = {'result': [{'path': 'EN3_BabyShark_KeyChain.gcode', 'modified': 1712800402.0, 'size': 2233884, 'permissions': 'rw'}, {'path': 'EN3_DezullonL.gcode', 'modified': 1713142039.0, 'size': 18803095, 'permissions': 'rw'}, {'path': 'EN3_Dragon_Stache_v0.gcode', 'modified': 1714065518.0, 'size': 107053, 'permissions': 'rw'}, {'path': 'EN3_Dragon_v2.gcode', 'modified': 1714038813.0, 'size': 28096475, 'permissions': 'rw'}, {'path': 'EN3_housing.gcode', 'modified': 1712817983.0, 'size': 9776204, 'permissions': 'rw'}, {'path': 'EN3_MagnetConnector.gcode', 'modified': 1712487698.0, 'size': 1216109, 'permissions': 'rw'}, {'path': 'EN3_Tank.gcode', 'modified': 1713392346.0, 'size': 4605613, 'permissions': 'rw'}, {'path': 'key.gcode', 'modified': 1712639025.0, 'size': 13589578, 'permissions': 'rw'}, {'path': 'knuckle-spikev1.gcode', 'modified': 1712647535.0, 'size': 13589577, 'permissions':  'rw'}]}

checkok = {'result': 'ok'}

ser = serial.Serial('COM1', 115200, timeout=1)

def log_command_to_csv(command):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "command"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, command])

@app.route('/', methods=['GET'])
def get_json():
    response_data = dataa
    return jsonify(response_data)

@app.route('/get', methods=['GET'])
def get_json2():
    response_data = dataa
    return jsonify(response_data)

@app.route('/server/files/list', methods=['GET'])
def list_files_route():
    return jsonify(list_files)

@app.route('/printer/gcode/script', methods=['GET'])
def home():
    return jsonify(checkok)

@app.route('/home', methods=['GET'])
def home2():
    dataa['gcode_move']['homed_axes'] = 'xyz'
    dataa['gcode_move']['gcode_position'] = [0, 0, 0, 0]
    return jsonify(checkok)

@app.route('/post', methods=['POST'])
def post_json():
    data = request.get_json()
    response_data = {
        'message': 'This is a POST request',
        'received_data': data
    }
    return jsonify(response_data)

@app.route('/gcode', methods=['GET'])
def gcode_script():
    script = request.args.get('gcode')
    if script:
        log_command_to_csv(script)

    if 'G1' in script:
        x, y, z, _ = dataa['gcode_move']['gcode_position']
        if 'X' in script:
            x_index = script.find('X')
            if x_index != -1:
                value = script[x_index + 1:]
                x = eval(f"x{value}")
        if 'Y' in script:
            y_index = script.find('Y')
            if y_index != -1:
                value = script[y_index + 1:]
                y = eval(f"y{value}")
        if 'Z' in script:
            z_index = script.find('Z')
            if z_index != -1:
                value = script[z_index + 1:]
                z = eval(f"z{value}")

        xyz = f'G0 X{x}Y{y}Z{z}'
        ser.write(xyz.encode())
        dataa['gcode_move']['gcode_position'] = [x, y, z, 0]
        
    if 'G0' in script:
        x, y, z, _ = dataa['gcode_move']['gcode_position']
        current_variable = ''
        current_number = ''

        for char in script:
            if char.isalpha():
                if current_variable:
                    if current_variable == 'X':
                        x = int(current_number)
                    elif current_variable == 'Y':
                        y = int(current_number)
                    elif current_variable == 'Z':
                        z = int(current_number)
                current_variable = char
                current_number = ''
            else:
                current_number += char

        if current_variable == 'X':
            x = int(current_number)
        elif current_variable == 'Y':
            y = int(current_number)
        elif current_variable == 'Z':
            z = int(current_number)

        ser.write(script.encode())
        dataa['gcode_move']['gcode_position'] = [x, y, z, 0]

    if script == "M18":
        dataa['gcode_move']['homed_axes'] = ''
        ser.write('motor_off\n'.encode())
        
    if "Speed" in script:
        dataa['gcode_move']['speed_factor'] = int(script.split('d')[1]) / 100
        ser.write(f'{script}\n'.encode())
        
    if script == "G28":
        dataa['gcode_move']['homed_axes'] = 'xyz'
        dataa['gcode_move']['gcode_position'] = [0, 0, 0, 0]
        ser.write('motor_on\n'.encode())
        ser.write('home\n'.encode())

    if script:
        dataa['last_gcode'] = script
        ser.write(f'{script}/n'.encode())
    
    response_data = {'message': 'Received script', 'gcode': script}
    return jsonify(response_data), 200

@app.route('/data', methods=['GET'])
def home3():
    global dataa
    return jsonify(dataa)

# @app.route('/data', methods=['POST'])
# def json_endpoint():
    # global dataa
    # try:
    #     data = request.get_json()
    #     if data is None:
    #         return jsonify({"error": "No JSON data received"}), 400

    #     x = data.get('x')
    #     y = data.get('y')
    #     z = data.get('z')

    #     if x is None or y is None or z is None:
    #         return jsonify({"error": "Missing x, y, or z values"}), 400

    #     dataa['gcode_move']['gcode_position'] = [x, y, z, 0]
    #     gcode_command = f"G1 X{x} Y{y} Z{z}\n"
    #     # #ser.write(gcode_command.encode())

    #     return jsonify({"message": "JSON received and data updated", "data": data}), 200
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
    ser.close()
