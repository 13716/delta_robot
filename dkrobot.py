import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial.tools.list_ports
from tkinter import filedialog
import cv2 
from ultralytics import YOLO
import cv2
import numpy as np
import sys
import math
import threading
import serial
import serial.tools.list_ports
root = tk.Tk()
root.geometry("1030x610")
root.title('Bảng điều khiển')
root.withdraw()

login = tk.Toplevel(root)
login.title("Login")
login.geometry("300x200")
ser = None
baudrate=115200
def auto_connect():
    global ser
    def find_serial_ports():
        # Get a list of available COM ports
        ports = list(serial.tools.list_ports.comports())
        if len(ports)==0:
            print("ko có COM")
            return []
        else:
            return [port.device for port in ports]
    
    # Mở kết nối với cổng và baudrate cụ thể
    for port in find_serial_ports():
        ser = serial.Serial(port, baudrate, timeout=1)  
        # Gửi dữ liệu
        ser.write(b"hello\n")
    # Đọc dữ liệu sau khi gửi
        data = ser.readline().decode('utf-8').strip()
        print(f"Dữ liệu đọc được sau khi gửi: {data}")
        if 'ok' in data:
            if ser.is_open:
                print(f"Connected to Arduino on port {port} at baudrate {baudrate}")
                login.withdraw()  # Hide the "Login" window
                root.deiconify()  # Show the "Control" window
            else:
                ser.close()
                continue
            return ser
def connect_manual():
    global ser, root, login, control_frame

    # Get selected values from comboboxes
    serial_port = port_combobox.get()
    baud_rate = baud_combobox.get()

    # Check if any of the values are empty
    if not serial_port or not baud_rate:
        print("Please select both serial port and baudrate.")
        return

    try:
        # Attempt to open a connection to Arduino
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        if ser.is_open:
            print(f"Connected to Arduino on port {serial_port} at baudrate {baud_rate}")
            login.withdraw()  # Hide the "Login" window
            root.deiconify()  # Show the "Control" window
            return ser
    except serial.SerialException as e:
        print(e)

def disconnect():
    global ser, root, login

    if ser is not None:
        ser.close()
        print("Disconnected from Arduino")
        root.withdraw()  # Hide the "Control" window
        login.deiconify()  # Show the "Login" window
        stop_camera()
        ser = None  
    else:
        print("Serial is not connected")

def gui_tdhut():
    global ser
    if ser is not None and ser.is_open:
        xhut_value = int(entr_xhut.get())
        yhut_value = int(entr_yhut.get())
        zhut_value = int(entr_zhut.get())
        if zhut_value <=0:
            command = f"x{xhut_value}y{yhut_value}z{zhut_value}\n"
            command1 ="hut\n"
            ser.write(command.encode())
            time.sleep(5)
            ser.write(command1.encode())
            print(f"Gửi lệnh đến Arduino: {command},{command1}")
    else:
        print("Chưa kết nối với cổng serial")
def gui_tdnha():
    global ser
    if ser is not None and ser.is_open:
        xnha_value = int(entr_xnha.get())
        ynha_value = int(entr_ynha.get())
        znha_value = int(entr_znha.get())
        if znha_value <=0:
            command = f"x{xnha_value}y{ynha_value}z{znha_value}\n"
            ser.write(command.encode())
            command1 ="nha\n"
            time.sleep(5)
            ser.write(command1.encode())
            print(f"Gửi lệnh đến Arduino: {command}")
    else:
        print("Chưa kết nối với cổng serial")

def update_speed_from_slider(event):
    speed = int(speed_slider.get())
    speed_entry.delete(0, tk.END)
    speed_entry.insert(0, str(speed))

def update_speed_from_entry(event):
    try:
        speed = int(speed_entry.get())
        if 0 <= speed <= 1000:
            speed_slider.set(speed)
    except ValueError:
        pass

def open_usb():
    usb_path = filedialog.askdirectory()
    if usb_path:
        usb_entry.delete(0, tk.END)  # Xóa nội dung hiện có trong Entry
        usb_entry.insert(0, usb_path)  # Chèn đường dẫn USB vào Entry
    
#cập nhật vị trí home
def reset_positions():
    global ser
    h1 = "home\n"
    ser.write(h1.encode())
    entr_set_x.delete(0, tk.END)
    entr_set_x.insert(0, '0')
    entr_set_y.delete(0, tk.END)
    entr_set_y.insert(0, '0')
    entr_set_z.delete(0, tk.END)
    entr_set_z.insert(0, '0')
    # write home

def update_x_value(value):
    current_value = entr_set_x.get()
    if current_value.isdigit() or (current_value[1:].isdigit() and current_value[0] == '-'):
        current_value = int(current_value)
    else:
        current_value = 0
    new_value = current_value + (10*value)
    entr_set_x.delete(0, tk.END)
    entr_set_x.insert(0, str(new_value))

def update_y_value(value):
    current_value =  entr_set_y.get()
    if current_value.isdigit() or (current_value[1:].isdigit() and current_value[0] == '-'):
        current_value = int(current_value)
    else:
        current_value = 0
    new_value = current_value + (10*value)
    entr_set_y.delete(0, tk.END)
    entr_set_y.insert(0, str(new_value))

def update_z_value(value):
    current_value = entr_set_z.get()
    if current_value.isdigit() or (current_value[1:].isdigit() and current_value[0] == '-'):
        current_value = int(current_value)
    else:
        current_value = 0
    new_value = current_value - (10*value)
    new_value = min(0, new_value)
    entr_set_z.delete(0, tk.END)
    entr_set_z.insert(0, str(new_value))

def gui_toado():
    global ser
    if ser is not None and ser.is_open:
        x_value = int(entr_set_x.get())
        y_value = int(entr_set_y.get())
        z_value = int(entr_set_z.get())
        if z_value <=0:
            command = f"x{x_value}y{y_value}z{z_value}\n"
            ser.write(command.encode())
            print(f"Gửi lệnh đến Arduino: {command}")
        else:
            print("error")
    else:
        print("Chưa kết nối với cổng serial")

def motor_on():
    global ser
    m1 = "motor_on\n"
    ser.write(m1.encode()) 
def motor_off():
    global ser
    m2 = "motor_off\n"
    ser.write(m2.encode()) 

def change_mode1():
    global mode_act, camera_update_flag
    if mode_act == "Manual":
        mode_act = "Auto"
        mode_act_but.config(text="MODE: Auto", font=('Times New Roman', 10, 'bold'))
        # Start or resume camera update in Auto mode
        camera_update_flag = True
        threading.Thread(target=update_camera).start()
    else:
        mode_act = "Manual"
        mode_act_but.config(text="MODE: Manual", font=('Times New Roman', 10, 'bold'))
        # Stop or pause camera update in Manual mode
        camera_update_flag = False
mode_act = "Manual"  # Khởi tạo trạng thái mặc định
mode_act_but = tk.Button(root, text="MODE: Manual", font=('Times New Roman',10,'bold'),command=change_mode1)
mode_act_but.place(x=570,y=15)
mode_act_but.config(bg='#663399',fg='white')

control_frame = tk.LabelFrame(root,text='[Manual Mode]' ,font=("Times New Roman",11,'bold'), bg='gainsboro', width=330, height=470, relief="groove")
control_frame.place(x=20, y=120)
ltaodo = tk.Label(root,text='VỊ TRÍ HIỆN TẠI',font=('Times New Roman',10,'bold'),bg='gainsboro',fg='#663399')
ltaodo.place(x=50,y=140)
tdhut = tk.Label(root,text='ĐIỂM HÚT',font=('Times New Roman',10,'bold'),bg='gainsboro',fg='#663399')
tdhut.place(x=180,y=140)
tdnha = tk.Label(root,text='ĐIỂM NHẢ',font=('Times New Roman',10,'bold'),bg='gainsboro',fg='#663399')
tdnha.place(x=260,y=140)

entr_set_x = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_set_x.insert(0, '0')
entr_set_x.place(x=70,y=170)
entr_set_y = tk.Entry(root, font=("Times New Roman", 12), width=6)
entr_set_y.insert(0, '0')  # Khởi tạo giá trị mặc định là 0
entr_set_y.place(x=70, y=210)
entr_set_z = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_set_z.insert(0, '0')
entr_set_z.place(x=70,y=250)

entr_xhut = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_xhut.place(x=185,y=170)
entr_yhut = tk.Entry(root, font=("Times New Roman", 12), width=6)
entr_yhut.place(x=185, y=210)
entr_zhut = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_zhut.place(x=185,y=250)
entr_xnha = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_xnha.place(x=265,y=170)
entr_ynha = tk.Entry(root, font=("Times New Roman", 12), width=6)
entr_ynha.place(x=265, y=210)
entr_znha = tk.Entry(root,font=("Times New Roman",12),width=6)
entr_znha.place(x=265,y=250)


set_x = tk.Label(root,text='X',font=('Times New Roman',10,'bold'),bg='gainsboro')
set_x.place(x=50,y=170)
set_y = tk.Label(root,text='Y',font=('Times New Roman',10,'bold'),bg='gainsboro')
set_y.place(x=50,y=210)
set_z = tk.Label(root,text='Z',font=('Times New Roman',10,'bold'),bg='gainsboro')
set_z.place(x=50,y=250)

run_but = tk.Button(root,text='UPDATE',font=('Times New Roman',10,'bold'),bg='#663399',fg='white',width=7, command=gui_toado)
run_but.place(x=70,y=280)

PgUp = tk.Button(root,text='Y+',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_y_value(1))
PgUp.place(x=235,y=340)
PgDn = tk.Button(root,text='Y-',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_y_value(-1))
PgDn.place(x=235,y=440)
PgLeft = tk.Button(root,text='X+',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_x_value(1))
PgLeft.place(x=185,y=390)
PgRight = tk.Button(root,text='X-',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_x_value(-1))
PgRight.place(x=280,y=390)

z_Up = tk.Button(root,text='Z+',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_z_value(1))
z_Up.place(x=235,y=365)
z_Dn = tk.Button(root,text='Z-',font=('Times New Roman',10,'bold'),width=4, command=lambda: update_z_value(-1))
z_Dn.place(x=235,y=415)

style = ttk.Style()
style.configure("Green.Horizontal.TScale", background="gainsboro")
# Tạo thanh trượt cho tốc độ từ 0 đến 1000
speed_label = ttk.Label(root, text="TỐC ĐỘ",font=('Times New Roman',10,'bold'),background="gainsboro")
speed_label.place(x=40,y=340)
speed_slider = ttk.Scale(root, from_=1, to=500, orient="horizontal", style="Green.Horizontal.TScale")
speed_slider.place(x=40,y=360)

# Hiển thị giá trị tốc độ trong một Entry
speed_entry = tk.Entry(root, width=5,justify='center')
speed_entry.place(x=70,y=390)

# Kết nối sự kiện khi thay đổi giá trị tốc độ từ thanh trượt
speed_slider.bind("<Motion>", update_speed_from_slider)

# Kết nối sự kiện khi thay đổi giá trị tốc độ từ Entry
speed_entry.bind("<KeyRelease>", update_speed_from_entry)

# Tạo Entry để hiển thị đường dẫn USB
usb_entry = tk.Entry(root,width=15)
usb_entry.place(x=630,y=52)

    # Tạo nút để mở hộp thoại chọn USB
open_button = tk.Button(root, text="File USB", command=open_usb)
open_button.place(x=570,y=50)

Gripper = tk.Button(root,text='HÚT',font=('Times New Roman',10,'bold'),bg='#663399',fg='white',width=5,height=1, command=gui_tdhut)
Gripper.place(x=188,y=280)
drop = tk.Button(root,text='NHẢ',font=('Times New Roman',10,'bold'),bg='#663399',fg='white',width=5, command=gui_tdnha)
drop.place(x=270,y=280)
but_home = tk.Button(root,text='HOME',font=('Times New Roman',10,'bold'), width=5,command=reset_positions)
but_home.place(x=230,y=390)

def change_mode2():
    global bang_tai
    if bang_tai == "Off":
        bang_tai = "On"
        bt_button.config(text="BĂNG TẢI: ON",font=('Times New Roman',10,'bold'))
        if ser is not None and ser.is_open:
            ser.write("bt_on\n".encode())
    else:
        bang_tai = "Off"
        bt_button.config(text="BĂNG TẢI: OFF",font=('Times New Roman',10,'bold'))
        if ser is not None and ser.is_open:
            ser.write("bt_off\n".encode())

bang_tai = "Off"  # Khởi tạo trạng thái mặc định
bt_button = tk.Button(root, text="BĂNG TẢI: OFF", font=('Times New Roman',10,'bold'),command=change_mode2)
bt_button.place(x=30, y=420)
bt_button.config(bg='#663399',fg='white')

def change_mode3():
    global hut_chankhong
    if hut_chankhong == "Off":
        hut_chankhong = "On"
        hck_button.config(text="HÚT CHÂN KHÔNG: ON",font=('Times New Roman',10,'bold'))
        if ser is not None and ser.is_open:
            ser.write("bomon\n".encode())
    else:
        hut_chankhong = "Off"
        hck_button.config(text="HÚT CHÂN KHÔNG: OFF",font=('Times New Roman',10,'bold'))
        if ser is not None and ser.is_open:
            ser.write("bomoff\n".encode())

hut_chankhong = "Off"  # Khởi tạo trạng thái mặc định
hck_button = tk.Button(root, text="HÚT CHÂN KHÔNG: OFF", font=('Times New Roman',10,'bold'),command=change_mode3)
hck_button.place(x=30, y=530)
hck_button.config(bg='#663399',fg='white')

login_open_button = tk.Button(login, text="OPEN", font=("Times New Roman",10,'bold'), bg='#663399',fg='white', width=7, command=connect_manual)
login_open_button.place(x=30, y=35)
login_auto_button = tk.Button(login, text="AUTO CONNECT", font=("Times New Roman",10,'bold'), bg='#663399',fg='white', width=15, command=auto_connect)
login_auto_button.place(x=100, y=100)
ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7']  
port_combobox = ttk.Combobox(login, values=ports, width=7)
port_combobox.place(x=130, y=35)
baud_rates = ['9600', '19200', '38400', '57600', '115200']
baud_combobox = ttk.Combobox(login, width=7, values=baud_rates)
baud_combobox.place(x=130, y=70)

# ... (Các thành phần khác trong cửa sổ "Login")

# Đảm bảo cửa sổ "Login" không hiển thị khi chạy ứng dụng

but_close = tk.Button(root, text='CLOSE', font=("Times New Roman",10,'bold'), bg='#663399',fg='white',width=7, command=disconnect)
but_close.place(x=40,y=70)
#điều khiển động cơ
onmotor = tk.Button(root, text='MOTOR ON', font=("Times New Roman",10,'bold'), bg='#663399',fg='white',width=9,command=motor_on)
onmotor.place(x=40,y=450)
offmotor = tk.Button(root, text='MOTOR OFF', font=("Times New Roman",10,'bold'), bg='#663399',fg='white',width=12,command=motor_off)
offmotor.place(x=40,y=480)

def execute_entered_code():
    entered_code = code_entry.get("1.0", tk.END)
    print("Entered code:")
    print(entered_code)

code_entry_open = False  # Biến để theo dõi trạng thái của Entry code

def show_hide_code_entry():
    global code_entry_open, code_entry, run_button

    if not code_entry_open:
        # Nếu Entry code chưa mở, mở nó lên
        code_entry = tk.Text(root, font=("Times New Roman", 12), width=25, height=5)
        code_entry.place(x=338, y=50)
        run_button = tk.Button(root, text="Run", font=('Times New Roman', 10, 'bold'), command=run_code)
        run_button.place(x=490, y=20)
        # Cập nhật trạng thái biến
        code_entry_open = True
    else:
        # Nếu Entry code đang mở, tắt nó đi
        code_entry.destroy()
        run_button.destroy()
        code_entry_open = False

def run_code():
    global ser
    if ser is not None and ser.is_open:
        entered_code = code_entry.get("1.0", tk.END)
        print("Entered code:")
        print(entered_code)
        ser.write(entered_code.encode())
        print("Code sent to Arduino")
    else:
        print("Chưa kết nối với cổng serial")
        
program_button = tk.Button(root, text="Program", font=('Times New Roman', 10, 'bold'), command=show_hide_code_entry)
program_button.place(x=350, y=20)

# Auto mode
def draw_rectangle(frame,xyxy, names,clas,cof):
    global ser,z
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (int(xyxy[0][0]), int(xyxy[0][1]))
    font_scale = 1
    color = (255, 0, 0)
    thickness = 2
    z=-20
    # Draw rectangle around the object
    cv2.rectangle(frame, (int(xyxy[0][0]), int(xyxy[0][1])),
                (int(xyxy[0][2]), int(xyxy[0][3])), color, thickness)

    # Print the center coordinates of the object
    center_x = int((xyxy[0][0] + xyxy[0][2]) / 2)
    center_y = int((xyxy[0][1] + xyxy[0][3]) / 2)
    center_coordinates = f"Center: ({center_x}, {center_y})"
     # Calculate the angle
    reference_line = [frame.shape[1] // 2, 0]  # Vertical line along the frame
    angle_rad = math.atan2(center_y - reference_line[1], center_x - reference_line[0])
    angle_deg = math.degrees(angle_rad)
    angle_text = f"Angle: {angle_deg:.2f} degrees"

    cv2.putText(frame, names[clas[0]]+" "+str(round(cof[0],2))+" "+center_coordinates, org, font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.putText(frame, angle_text, (org[0], org[1] + 30), font, font_scale, color, thickness, cv2.LINE_AA)
    center_data = f"({center_x}, {center_y},{z})"
    angle_data = f"{angle_deg:.2f} degrees"
    serial_data = f"{center_data}, {angle_data}\n"  # Dữ liệu cần gửi

    d=ser.write(serial_data.encode())
    print(f'{d}')
def update_camera():
    global cap,camera_update_flag

    model = YOLO(r"D:\python\delta\runs\detect\train4\weights\last.pt").to("cpu")

    if model is None:
        print("Error loading the model.")
        sys.exit()

    def update():
        while camera_update_flag:
            ret, frame = cap.read()
            if ret:
                results = model(frame)
                for result in results:
                    names = result.names
                    boxes = result.boxes.cpu().numpy()
                    for box in boxes:
                        draw_rectangle(frame, box.xyxy, names, box.cls, box.conf)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

                    camera_label.imgtk = photo
                    camera_label.configure(image=photo)

    threading.Thread(target=update).start()

# Bind the on_window_closed function to the window closing event
external_camera_index = 0
cap = cv2.VideoCapture(external_camera_index)

# Tạo LabelFrame cho camera
camera_frame = tk.LabelFrame(root, text='[CAM]', font=("Times New Roman", 11, 'bold'), width=640, height=480, relief="groove")
camera_frame.place(x=370, y=110)

camera_label = ttk.Label(camera_frame, image=None)
camera_label.place(x=10, y=50)

def stop_camera():
    cap.release()  # Giải phóng camera


root.mainloop()