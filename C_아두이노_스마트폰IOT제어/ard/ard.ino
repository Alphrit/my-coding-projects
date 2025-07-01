#include <DHT.h>
#include <Servo.h>

// DHT 센서 핀 정의
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// 조도 센서 핀 정의
#define LDR_PIN A0

// 서보 모터 핀 정의
#define servo1Pin 9
#define servo2Pin 10
Servo servo1;
Servo servo2;

// LED 핀 정의
#define lowHumidityLedPin 6
#define highHumidityLedPin 7

void setup() {
  Serial.begin(9600); // ESP-01과 통신
  Serial1.begin(9600);
  dht.begin();

  pinMode(lowHumidityLedPin, OUTPUT);
  pinMode(highHumidityLedPin, OUTPUT);

  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  Serial.println("아두이노 시작됨"); // 시작 메시지 추가
}

void loop() {
  Serial.println("명령 대기...");
  if (Serial.available() > 0) {
    Serial.println("데이터 수신됨:");
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.print("수신된 명령: ");
    Serial.println(command);
    if (command == "SET_SERVO") {
      Serial.println("서보 모터 제어 명령 실행");
      servo1.write(180); // 블라인드 강제 닫기
      servo2.write(180); // 창문 열기 등 원하면 같이 추가
      Serial.println("서보 모터 180도 회전 완료");
    } else {
      Serial.println("알 수 없는 명령입니다.");
    }
  }
  // ... (DHT, 조도 센서, LED 제어 및 ESP-01로 데이터 전송 코드는 그대로 유지) ...
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int light = analogRead(LDR_PIN);

  bool lowHum = false;
  bool highHum = false;

  if (hum < 50) {
    digitalWrite(lowHumidityLedPin, HIGH);
    digitalWrite(highHumidityLedPin, LOW);
    lowHum = true;
  } else {
    digitalWrite(lowHumidityLedPin, LOW);
    digitalWrite(highHumidityLedPin, HIGH);
    highHum = true;
  }

  int servo1Angle = (light > 512) ? 180 : 0;
  String blind = (servo1Angle > 90) ? "닫힘" : "열림";
  int servo2Angle = (temp > 25.0) ? 180 : 0;
  String window = (servo2Angle > 90) ? "열림" : "닫힘";
  String ledStatus = (lowHum) ? "LOW, 가습기 가동" : (highHum ? "HIGH, 제습기 가동" : "OFF");
  servo1.write(servo1Angle);
  servo2.write(servo2Angle);

  String allData = "온도:" + String(temp) + "도" + "        습도:" + String(hum) + "%" + "        조도:" + String(light) + "<br>" +
                     "<br>" + "<br>" + "<br>" +
                     "서보모터1 각도:" + String(servo1Angle) + "도" + ", 블라인드:" + blind + "<br>" +
                     "서보모터2 각도:" + String(servo2Angle) + "도" + ", 창문:" + window + "<br>" +
                     "LED:" + ledStatus;

  Serial1.println(allData);

  delay(2000);
}