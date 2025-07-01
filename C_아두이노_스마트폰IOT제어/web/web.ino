#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "U+Net1CE4";
const char* password = "730A51@G8A";

ESP8266WebServer server(80);

String latestData = "데이터 수신 대기 중...";

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi 연결됨, IP 주소: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.on("/setServo", handleSetServo);  // 버튼 처리용 엔드포인트 추가
  server.on("/command", []() {
    String cmd = server.arg("cmd");
    if (cmd.length() > 0) {
      Serial.println(cmd);  // 예: SET_SERVO 출력 → 이게 Arduino로 전송됨
    }
    server.send(200, "text/plain", "OK");
  });
  server.begin();
  Serial.println("웹 서버 시작됨");
}

void loop() {
  if (Serial.available()) {
    latestData = Serial.readStringUntil('\n');
    latestData.trim();
  }

  server.handleClient();
}

void handleRoot() {
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'>";
  html += "<title>ESP-01 센서 상태 보기</title></head><body>";
  html += "<h1>ESP-01 센서 상태 보기</h1>";
  html += "<pre id='sensorData'>로딩 중...</pre>";
  html += "<button onclick='setServo()'>서보모터 강제 180도</button><br><br>";
  html += "<button onclick=\"sendCommand()\">서보모터 강제 닫기</button>";
  html += R"rawliteral(
  <script>
    function sendCommand() {
      fetch('/command?cmd=SET_SERVO');
    }
  </script>
  )rawliteral";

  html += R"rawliteral(
    <script>
      function fetchData() {
        fetch('/data')
          .then(response => response.text())
          .then(data => {
            document.getElementById('sensorData').innerHTML = data;
          });
      }
      function setServo() {
        fetch('/setServo')
          .then(response => response.text())
          .then(data => {
            alert(data);  // 결과 알림창 출력
            fetchData();  // 버튼 누른 후에도 데이터 갱신
          });
      }
      setInterval(fetchData, 2000);
      fetchData();
    </script>
  )rawliteral";

  html += "</body></html>";

  server.send(200, "text/html; charset=utf-8", html);
}

void handleData() {
  server.send(200, "text/plain; charset=utf-8", latestData);
}

void handleSetServo() {
  Serial.println("SET_SERVO");  // ATmega328에게 신호 보냄
  server.send(200, "text/plain; charset=utf-8", "서보모터를 180도로 설정했습니다.");
}