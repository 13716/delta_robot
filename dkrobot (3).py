from library import *
import socket
root = tk.Tk()
root.geometry("1030x610")
root.title('Bảng điều khiển')
# root.withdraw()

# login = tk.Toplevel(root)
# login.title("Login")
# login.geometry("300x200")
# ser = None
# baudrate=115200
# ip=""
url2 =  'http://192.168.31.208:5001/gcode'#'http://192.168.53.13:5001/data'
# url1 =  'http://192.168.31.208:5001/data'#http://192.168.53.13:5001/data'
# # url2 =  'http://192.168.1.4:5001/gcode'#'http://192.168.53.13:5001/data'
# # url1 =  'http://192.168.1.4:5001/data'#http://192.168.53.13:5001/data'
# # url2 =  'http://1.54.230.72:8802/gcode'#'http://192.168.53.13:5001/data'
# # url1 =  'http://1.54.230.72:8802/data'#http://192.168.53.13:5001/data'
# # url3 = 'http://192.168.31.7:5001/read_serial'
port = 8888  # Cổng HTTp
# def tcp_ip():
#     global port,ip
#     # start_range = 1
#     # end_range = 254
#     ip_prefix = "42.116.179.101"
#     ip=ip_prefix
   
#     login.withdraw()  # Hide the "Login" window
#     root.deiconify()

    
# host = "192.168.1.11"


def delay(microseconds):
    start_time = time.monotonic()
    while (time.monotonic() - start_time) * 1e6 < microseconds:
        pass
# def send_data(data):
#     global ip, port
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         # s.connect((ip, port))
#         s.sendall(data.encode())
#         s.sendall('\n'.encode())
# def command(data):
#     global ip,ser,port
#     # print(ip)
#     if ip:
#         send_data(data)
#     else:
#         ser.write(data.encode())
#     delay(400)


# def send_json_data(data):
#     """
#     Gửi dữ liệu JSON tới URL chỉ định và trả về phản hồi JSON.

#     :param url: Địa chỉ URL để gửi yêu cầu POST
#     :param data: Dữ liệu JSON để gửi
#     :return: Phản hồi JSON từ server
#     """
#     global url1
#     try:
        
#         # Gửi yêu cầu POST với dữ liệu Gcode
#         response = requests.post(url1, json=data)
#         # # Gửi yêu cầu POST với dữ liệu JSON
#         # response = requests.post(url1, json=data)
        
#         if response.status_code == 200:
#             # Trả về phản hồi JSON nếu yêu cầu thành công
#                 return response.json()
#         else:
#             # Trả về thông báo lỗi nếu yêu cầu không thành công
#             return {"error": f"Request failed with status code {response.status_code}"}
#     except Exception as e:
#         # Trả về thông báo lỗi nếu có ngoại lệ xảy ra
#         return {"error": str(e)}

def Get(data):
    global url2
    if 'X' and 'Y' and 'Z' in data:
        params = {'gcode': f'G0 {data}'}
    else:
        params = {'gcode': f'{data}'}

    # Gửi yêu cầu GET
    response = requests.get(url2, params=params)

    # Kiểm tra mã trạng thái của phản hồi
    if response.status_code == 200:
        # In nội dung của phản hồi
        print('Response:', response.json())
    else:
        print(f'Failed to get data. Status code: {response.status_code}')
# Sử dụng hàm để gửi dữ liệu JSON
# def read():
#     global url3
#     res= requests.get(url3)
#     if res.status_code ==200:
#         data = res.json()
#         # In dữ liệu JSON ra màn hình
#         print(data)

def gui_tdhut():
        global ser
        xhut_value = int(entr_xhut.get())
        yhut_value = int(entr_yhut.get())
        zhut_value = int(entr_zhut.get())
        if zhut_value <=0:
            data = f"X{xhut_value} Y{yhut_value} Z{zhut_value}"
            data1="Hut"
            # send_json_data(data1)
            Get(data)
            Get(data1)
            # read()
            # command1 = f"x{xhut_value}y{yhut_value}z{zhut_value}\n"
            # command2 ="hut\n"
            # command(command1)
            # # time.sleep(1)
            # command(command2)
            # print(f"Gửi lệnh đến Arduino: {command1},{command2}")

def gui_tdnha():
    global ser
    xnha_value = int(entr_xnha.get())
    ynha_value = int(entr_ynha.get())
    znha_value = int(entr_znha.get())
    if znha_value <=0:
        data = f"X{xnha_value} Y{ynha_value} Z{znha_value}"
        data1="Tha"
        # send_json_data(data1)
        Get(data)
        Get(data1)
        # read()
        # command1 = f"x{xnha_value}y{ynha_value}z{znha_value}\n"
        # command(command1)
        # command2 ="tha\n"
        # command(command1)
        # # time.sleep(1)
        # command(command2)
        # print(f"Gửi lệnh đến Arduino: {command1},{command2}")


def update_speed_from_slider(event):
    speed = int(speed_slider.get())
    speed_entry.delete(0, tk.END)
    speed_entry.insert(0, str(speed))

def update_speed_from_entry(event):
    global ser
    try:
        speed = int(speed_entry.get())
        if 0 <= speed <= 1000:
            speed_slider.set(speed)
            data=f'Speed{speed}'
            # send_json_data(data)
            Get(data)
            # read()
            # command(f"speed{speed}\n")
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
    h1 = "G28"
    data=h1
    # send_json_data(data)
    Get(data)
    # read()
   
    # command(h1)
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
    gui_toado()

def update_y_value(value):
    current_value =  entr_set_y.get()
    if current_value.isdigit() or (current_value[1:].isdigit() and current_value[0] == '-'):
        current_value = int(current_value)
    else:
        current_value = 0
    new_value = current_value + (10*value)
    entr_set_y.delete(0, tk.END)
    entr_set_y.insert(0, str(new_value))
    gui_toado()

def update_z_value(value):
    current_value = entr_set_z.get()
    if current_value.isdigit() or (current_value[1:].isdigit() and current_value[0] == '-'):
        current_value = int(current_value)
    else:
        current_value = 0
    new_value = current_value + (10*value)
    new_value = min(0, new_value)
    entr_set_z.delete(0, tk.END)
    entr_set_z.insert(0, str(new_value))
    gui_toado()

def gui_toado():
    global ser

    x_value = int(entr_set_x.get())
    y_value = int(entr_set_y.get())
    z_value = int(entr_set_z.get())
    if z_value <=0:
        data = f'X{x_value} Y{y_value} Z{z_value}'
        # print(send_json_data(data))
        # xx=f'X{x_value}'
        # yy=f'Y{y_value}'
        # zz=f'Z{z_value}'
        # Get(xx)
        # Get(yy)
        # Get(zz)
        Get(data)
        # read()
    #     command1 = f"x{x_value}y{y_value}z{z_value}\n"
    #     command(command1)
    #     print(f"Gửi lệnh đến Arduino: {command1}")
    # else:
    #     print("error")


def motor_on():
    global ser
    m1 = "G28"
    data=m1
    # send_json_data(data)
    Get(data)
    # read()
    # command(m1) 
def motor_off():
    global ser
    m2 = "M18"
    data=m2
    # send_json_data(data)
    Get(data)
    # read()
    # command(m2) 

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
ltoado = tk.Label(root,text='VỊ TRÍ HIỆN TẠI',font=('Times New Roman',10,'bold'),bg='gainsboro',fg='#663399')
ltoado.place(x=50,y=140)
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
            data={"bt_status":"convrun"}
            # send_json_data(data)
            Get(data)
            # read()
            # command("convrun\n")
    else:
        bang_tai = "Off"
        bt_button.config(text="BĂNG TẢI: OFF",font=('Times New Roman',10,'bold'))
        if ser is not None and ser.is_open:
            data={"bt_status":"convstop"}
            # send_json_data(data)
            Get(data)
            # read()
            # command("convstop\n")

bang_tai = "Off"  # Khởi tạo trạng thái mặc định
bt_button = tk.Button(root, text="BĂNG TẢI: OFF", font=('Times New Roman',10,'bold'),command=change_mode2)
bt_button.place(x=30, y=420)
bt_button.config(bg='#663399',fg='white')

def change_mode3():
    global hut_chankhong
    if hut_chankhong == "Off":
        hut_chankhong = "On"
        hck_button.config(text="HÚT CHÂN KHÔNG: ON",font=('Times New Roman',10,'bold'))
        # if ser is not None and ser.is_open:
        data="bom_on"
        # send_json_data(data)
        Get(data)
        # read()
        # command("bomon")
    
    else:
        hut_chankhong = "Off"
        hck_button.config(text="HÚT CHÂN KHÔNG: OFF",font=('Times New Roman',10,'bold'))
        # if ser is not None and ser.is_open:
        data="bom_off"
        # send_json_data(data)
        Get(data)
        # read()
        # command("bomoff")

hut_chankhong = "Off"  # Khởi tạo trạng thái mặc định
hck_button = tk.Button(root, text="HÚT CHÂN KHÔNG: OFF", font=('Times New Roman',10,'bold'),command=change_mode3)
hck_button.place(x=30, y=530)
hck_button.config(bg='#663399',fg='white')

# login_open_button = tk.Button(login, text="OPEN", font=("Times New Roman",10,'bold'), bg='#663399',fg='white', width=7, command=connect_manual)
# login_open_button.place(x=30, y=35)
# login_auto_button = tk.Button(login, text="AUTO CONNECT", font=("Times New Roman",10,'bold'), bg='#663399',fg='white', width=15, command=auto_connect)
# login_auto_button.place(x=100, y=100)
# login_Ip_button = tk.Button(login, text="IP CONNECT", font=("Times New Roman",10,'bold'), bg='#663399',fg='white', width=15, command=tcp_ip)
# login_Ip_button.place(x=100, y=130)
# ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7']  
# port_combobox = ttk.Combobox(login, values=ports, width=7)
# port_combobox.place(x=130, y=35)
# baud_rates = ['9600', '19200', '38400', '57600', '115200']
# baud_combobox = ttk.Combobox(login, width=7, values=baud_rates)
# baud_combobox.place(x=130, y=70)

# ... (Các thành phần khác trong cửa sổ "Login")

# Đảm bảo cửa sổ "Login" không hiển thị khi chạy ứng dụng

# but_close = tk.Button(root, text='CLOSE', font=("Times New Roman",10,'bold'), bg='#663399',fg='white',width=7, command=disconnect)
# but_close.place(x=40,y=70)
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
    # global ser
    entered_code = code_entry.get("1.0", tk.END)
    print("Entered code:")
    print(entered_code)
    data=f'{entered_code}'
    # send_json_data(data)
    Get(data)
    # read()
    # command(entered_code)
    # print("Code sent to Arduino")
        
program_button = tk.Button(root, text="Program", font=('Times New Roman', 10, 'bold'), command=show_hide_code_entry)
program_button.place(x=350, y=20)

# Auto mode
def Auto(frame,xyxy, names,clas,cof):
    global ser
    z=-200
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (int(xyxy[0][0]), int(xyxy[0][1]))
    font_scale = 1
    color = (255, 0, 0)
    thickness = 2

    start_point=(5,5)
    end_point=(int(frame.shape[1]/2),int(frame.shape[0]))
    thickness=2
    cv2.line(frame, start_point, end_point,color,thickness)
    if int(xyxy[0][2]<float(frame.shape[1]/2)):
        command("convstop\n")
        command('motor_on\n')
        command('bomon\n') 
        frame=cv2.rectangle(frame, (int(xyxy[0][0]), int(xyxy[0][1])),
                (int(xyxy[0][2]), int(xyxy[0][3])), color, thickness)
    # Print the center coordinates of the object
        center_x = int((xyxy[0][0] + xyxy[0][2]) / 2)
        center_y = int((xyxy[0][1] + xyxy[0][3]) / 2)
        center_x_true=int(center_x)
        center_y_true=int(center_y)
        center_coordinates = f"Center: ({center_x}, {center_y})"
        # Calculate the angle
        reference_line = [frame.shape[1] // 2, 0]  # Vertical line along the frame
        angle_rad = math.atan2(center_y - reference_line[1], center_x - reference_line[0])
        angle_deg = math.degrees(angle_rad)
        angle_text = f"Angle: {angle_deg:.2f} degrees"

        cv2.putText(frame, names[clas[0]]+" "+str(round(cof[0],2))+" "+center_coordinates, org, font, font_scale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, angle_text, (org[0], org[1] + 30), font, font_scale, color, thickness, cv2.LINE_AA)
        center_data = f"x{center_x_true}y{center_y_true}z{z}\n"
        print(center_data)
        angle_data = f"a{angle_deg:.2f} degrees"
        serial_data = f"{center_data}"  # Dữ liệu cần gửi
        data= {"x":center_x_true,
              "y":center_y_true,
              "z":z,
              "a":angle_deg
              }
        # send_json_data(data)  
        Get(data)
        # read()
        command(serial_data)


    
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
                        Auto(frame, box.xyxy, names, box.cls, box.conf)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

                    camera_label.imgtk = photo
                    camera_label.configure(image=photo)

    threading.Thread(target=update).start()

# Bind the on_window_closed function to the window closing event
# external_camera_index = 'http://42.116.179.101:8800/webcam/?action=stream'
external_camera_index = 0
cap = cv2.VideoCapture(external_camera_index)

# Tạo LabelFrame cho camera
camera_frame = tk.LabelFrame(root, text='[CAM]', font=("Times New Roman", 11, 'bold'), width=640, height=480, relief="groove")
camera_frame.place(x=370, y=100)

camera_label = ttk.Label(camera_frame, image=None)
camera_label.place(x=10, y=50)

def stop_camera():
    cap.release()  # Giải phóng camera


root.mainloop()