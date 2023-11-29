#include <ShiftRegister74HC595.h>
// parameters: <number of shift registers> (data pin, clock pin, latch pin)
ShiftRegister74HC595<3> sr(27, 25, 26);


const int stepPins[] = {1, 4, 7};  // Chân Step cho 3 động cơ
const int dirPins[] = {2, 5, 8};   // Chân Direction cho 3 động cơ
const int stepsPerRevolution = 16000; // Số bước trên mỗi vòng quay của động cơ
bool cont[]={1,1,1};
int direction[]={0,0,0};



void moveStepper(int steps[3]) {
  int maxAbsoluteValue = abs(steps[0]); // Lấy giá trị tuyệt đối của phần tử đầu tiên
//Chiều động cơ
  for (int i = 0; i < 3; i++) {
    if (steps[i]<0){
      direction[i]=LOW;
    }
    else{
      direction[i]=HIGH;
    }
    sr.set(dirPins[i], direction[i]);


    int absoluteValue = abs(steps[i]); // Lấy giá trị tuyệt đối của phần tử thứ i
    if (absoluteValue > maxAbsoluteValue) {
      maxAbsoluteValue = absoluteValue; // Cập nhật giá trị lớn nhất nếu tìm thấy giá trị tuyệt đối lớn hơn
    }
  }
  for (int i = 0; i < maxAbsoluteValue; i++) {
    
    for (int st=0;st<3;st++){
      if (i<abs(steps[st])){
        sr.set(stepPins[st], HIGH);
      }
    }
    delayMicroseconds(500-speed); 
    // delay(5);
    for (int st=0;st<3;st++){
      sr.set(stepPins[st], LOW);
    }
    delayMicroseconds(500-speed);
    // delay();
  }
}


void gotohome(){
float x=0;
float y=0;
float z=0;
int thetas[]={0, 0, 0};
int steps[]={0, 0, 0};
  for (int i = 0; i < 3; i++) {
    sr.set(dirPins[i], LOW);
  }
  for (int i = 0; i < 3; i++) {
      cont[i]=1;
  }

  //   for (int i = 0; i < 1600; i++) {
  //     for (int st=0;st<3;st++){
  //         if (digitalRead(endStop[i])==0){
  //           cont[i]=0;
  //         }
  //         if (cont[i]==1){
  //           sr.set(stepPins[st], HIGH);
  //         }
  //   }
  //   delayMicroseconds(500-speed); 

  //   for (int st=0;st<3;st++){
  //     sr.set(stepPins[st], LOW);
  //   }
  //   delayMicroseconds(500-speed);
  //   // delay();
  // }

int ac=5;
  for (int st = 0; st < 10000; st++) {
  
    for (int i=0;i<3;i++){
      if (digitalRead(endStop[i])==0){
        cont[i]=0;
      }
      if (cont[i]==1){
        sr.set(stepPins[i], HIGH);
      }
    }
    delayMicroseconds(500-speed); 
    // delay(5);
    for (int i=0;i<3;i++){
      sr.set(stepPins[i], LOW);
    }
    delayMicroseconds(500-speed);
    // delay();
  }
}

void motoron(){
  for (int i = 0; i < 3; i++) {
      sr.set(enPins[i], LOW);
  }
}

void motoroff(){
   for (int i = 0; i < 3; i++) {
      sr.set(enPins[i], HIGH);
  }
}

void bomon(){
  sr.set(17,HIGH);
}
void bomoff(){
  sr.set(17,LOW);
}

void hut(){
  sr.set(18,LOW);
}
void tha(){
  sr.set(18,HIGH);
}





// const int stepPin = 2;  // Chân số bước
// const int dirPin = 3;   // Chân hướng

// void setup() {
//   pinMode(stepPin, OUTPUT);
//   pinMode(dirPin, OUTPUT);
//   digitalWrite(dirPin, HIGH);  // Thiết lập hướng di chuyển, HIGH là hướng dương
// }

// void loop() {
//   moveWithInputShaping(1000, 3);  // Di chuyển động cơ đến vị trí 1000 bước, shapingFactor = 3

//   // Dừng lại 1 giây
//   delay(1000);
// }

// void moveWithInputShaping(int targetPosition, int shapingFactor) {
//   int currentPosition = 0;
//   int shapingValue = 1;

//   while (currentPosition != targetPosition) { 9 1000
//     currentPosition += shapingValue; -27 
    
//     // Áp dụng shaping factor để giảm dao động
//     shapingValue = -shapingValue * shapingFactor;-27 72

//     // Di chuyển động cơ bước
//     digitalWrite(stepPin, HIGH);
//     delayMicroseconds(500);  // Điều chỉnh thời gian tín hiệu HIGH để kiểm soát tốc độ
//     digitalWrite(stepPin, LOW);
//     delayMicroseconds(500);  // Điều chỉnh thời gian tín hiệu LOW để kiểm soát tốc độ

//     // Bạn có thể thêm thêm thời gian delay nếu cần
//   }
// }
