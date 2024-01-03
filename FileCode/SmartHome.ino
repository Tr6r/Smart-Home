#include <Servo.h>
#include <Stepper.h>
#include<SPI.h>
#include<MFRC522.h>
const int stepsPerRevolution = 2048;
      //Đọc dữ liệu từ DHT11 ở chân 2 trên mạch Arduino


#define SS_PIN 10
#define RST_PIN 9

int UID[4],i,count,count_end;
int ID1[3][4] = {{74,234,55,22},{19,179,176,9},{51,144,14,8}};
MFRC522 mfrc522(SS_PIN,RST_PIN); // .


Stepper mystep = Stepper (stepsPerRevolution,2,3,4,5);

Servo myservo1; 
Servo myservo2; 

void setup() {
  Serial.begin(9600);
  pinMode(6,OUTPUT);//còi
  myservo1.attach(8);
  myservo2.attach(7);
  mystep.setSpeed(18);
  SPI.begin();     // bắt đầu giao thức SPI
  mfrc522.PCD_Init(); // khởi tạo module
  myservo1.write(10);
  myservo2.write(120);
}
void quaytien(){
  mystep.step(stepsPerRevolution);
  }
void quaynguoc(){
 mystep.step(-stepsPerRevolution);

}
void tien()
{
  quaytien();
  quaytien();
  quaytien();
  quaytien();
  quaytien();
  quaytien();
  quaytien();
  quaytien();
}
void lui()
{ 
  quaynguoc();
  quaynguoc();
  quaynguoc();
  quaynguoc();
  quaynguoc();
  quaynguoc();
  quaynguoc();
  quaynguoc();
}
void loop() {
      int gas = analogRead(A0);
      Serial.println(gas);
      delay(200);
      if(gas >= 200)
      {
        digitalWrite(6,1);
      }
      else if (gas < 200)
      {
        digitalWrite(6,0);
      }
 


//      if (Serial.available() > 0) {
//        
//        String str = Serial.readString();
//        Serial.println(str);
//        if (str == "mocuaso")
//          {     
//            Serial.println("Mo cua");
//            lui();
//          }
//        else 
//          if(str == "dongcuaso")
//            {
//              Serial.println("Dong cua");
//             tien();
//            }
//         else 
//         if(str == "mocong")
//            {
//              digitalWrite(6,1);
//              delay(100);
//              digitalWrite(6,0);
//              myservo1.write(120);
//              myservo2.write(20);
//            }
//         else 
//         if(str == "dongcong")
//            {
//              digitalWrite(6,1);
//              delay(100);
//              digitalWrite(6,0);
//                   myservo1.write(20);
//                   myservo2.write(120);
//            }
//        }
//        else
//        {
                 
 if(!mfrc522.PICC_IsNewCardPresent())
 {
  
  return;
 }
 // Đọc hết thông tin trong thẻ
 if(!mfrc522.PICC_ReadCardSerial())
 {
   return;
 }
       

         digitalWrite(6,1);
    delay(100);
    digitalWrite(6,0);
    count = 0;
  for(byte i=0;i<mfrc522.uid.size;i++)
  {
  UID[i] = mfrc522.uid.uidByte[i];
 }
  count_end =0;
 
 for(int j = 0;j<3;j++)
 {
    for(int i = 0;i<4;i++)
    {
        if(UID[i] == ID1[j][i])
        {
             count++;
             if(count == 4)
                 {
                  
                   myservo1.write(120);
                   myservo2.write(20);
                   delay(5000);
                   myservo1.write(20);
                   myservo2.write(120);
                   count_end++;
                 }
       }
    }
 }
  if(count_end == 0)
    {
      digitalWrite(6,1);
      delay(1000);
      digitalWrite(6,0);
    }
  mfrc522.PICC_HaltA();//dừng việc đọc thẻ
  mfrc522.PCD_StopCrypto1();
          
          }
  
