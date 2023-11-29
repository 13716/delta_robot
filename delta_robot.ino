
const int endStop[] = {22,32,33};
const int enPins[] = {0,3,6};

int speed=000;
int steps[3];
float theta1=0;
float theta2=0;
float theta3=0;
float thetas[3];
float x;
float y;
float z;
int step1;
int step2;
int step3;
// #include "analogWrite.h"
// #include "BluetoothSerial.h"
// BluetoothSerial SerialBT;
void setup() {
 // analogWriteFrequency(2, 10000);
  // analogServo(2, 90);
  Serial.begin(115200);
  // SerialBT.begin("RobotDelta")  ;
  for (int i = 0; i < 3; i++) {
    pinMode(endStop[i],INPUT_PULLUP);
  }
  motoroff();
}


void loop() {
  // Di chuyển 3 động cơ cùng một lúc
  // speed=200;
  // int steps[]={12800, 3200, 1000};
  // moveStepper(steps); 
  // gotohome();




  if (Serial.available()) {
    // String received= Serial.readString(); // Đọc một chuỗi từ cổng serial
    String received = Serial.readStringUntil('\n');
    //  String received = Serial.readStringUntil('\n');
    // Serial.println(received);



  

    // steps[0]=step1;
    // steps[1]=step2;
    // steps[2]=step3;
    // moveStepper(steps);
  if (received.equals("home")) {
    gotohome();
  }
  else if (received.equals("motor_on")) {
    motoron();
    }
  else if (received.equals("motor_off")) {
   motoroff();
   }
  else if (received.indexOf("speed") != -1){
    speed=(received.substring(received.indexOf("d")+1, received.length())).toInt();
  }
  else if (received.equals("bomon")) {
   bomon();
   }
  else if (received.equals("bomoff")) {
   bomoff();
  }
  else if (received.equals("hut")) {
   hut();
  }
  else if (received.equals("tha")) {
   tha();
  }
  else if (received.equals("hello")){
    Serial.println("ok");
  }
  else {
    x=(received.substring(received.indexOf("x")+1, received.indexOf("y"))).toInt();
    y=(received.substring(received.indexOf("y")+1, received.indexOf("z"))).toInt();
    z=(received.substring(received.indexOf("z")+1, received.length())).toInt();    
    // sscanf(received, "x%d y%d z%d", &axis[0], &axis[1], &axis[2]);
      // sscanf(inputString.c_str(), "x%d y%d z%d", &x, &y, &z);

    
    
    Serial.println(x);
    Serial.println(y);
    Serial.println(z-183);
    delta_calcInverse(x,y,z-183,thetas);
      
    Serial.println(thetas[0]);
    Serial.println(thetas[1]);
    Serial.println(thetas[2]);

    theta_step(thetas,steps);
    Serial.println(steps[0]);
    Serial.println(steps[1]);
    Serial.println(steps[2]);
    moveStepper(steps);
  }

  }


  // static String inputString = ""; // Chuỗi để lưu dữ liệu từ cổng serial

  // while (Serial.available()) {
  //   char inChar = (char)Serial.read(); // Đọc một ký tự từ cổng serial

  //   if (inChar == '\n') { // Nếu gặp ký tự xuống dòng
  //     // Xử lý chuỗi đã đọc ở đây
  //     Serial.println("Received: " + inputString);
  //     inputString = ""; // Đặt lại chuỗi đầu vào để chuẩn bị cho chuỗi tiếp theo
  //   } else {
  //     inputString += inChar; // Nếu không phải ký tự xuống dòng, thêm ký tự vào chuỗi
  //   }
  // }
  //delay(1000); // Đợi 1 giây trước khi di chuyển lại
}
