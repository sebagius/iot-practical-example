#import <CRC32.h>
#import "ledmatrix.h"
#import "security.h"

//unsigned char table[16] = {0x00, 0x3E, 0x28, 0x28, 0x16, 0x00, 0x3E, 0x00, 0x26, 0x2A, 0x32, 0x00, 0x26, 0x2A, 0x32, 0x00};
unsigned char table[16] = {0x00, 0x32, 0x2A, 0x26, 0x00, 0x32, 0x2A, 0x26, 0x00, 0x3E, 0x00, 0x16, 0x28, 0x28, 0x3E, 0x00};
uint8_t* ourSecret = "thisisasmallstepforsecurity!";

uint8_t* currentMessage;

void setup()
{
  Serial.begin(9600);
  setupDisplay();
}

void writeuintarray(uint8_t* d, size_t len)
{
  for(int i = 0; i < len; i++)
  {
    Serial.write(d[i]);
  }
}

int readPacket(char* msg, int len, uint8_t** uid, bool* auth)
{
  int idLen = 0;
  int authLen = 0;
  int zeroPacks = 0;
  for(int i = 0; i < len; i++)
  {
    if(zeroPacks == 3)
    {
      *uid = malloc(i-3);
      auth = malloc(1);
      memcpy(*uid, msg, i-3);
      *auth = msg[i+1] == 218; // or 0xda our magic auth number!!
      writeuintarray(*uid, i-3);
      return i-3;
    }
    if(msg[i] == 0) // gap byte
    {
      zeroPacks++;
      continue;
    }
  }

  return 0;
}

void loop()
{
  //uint8_t* testdata = "hellooo";
  //verifyChecksum(testdata, 7, 0x00000001, ourSecret, 28);
  //Serial.print("uhhh");
  updateDisplay(table);
  if(Serial.available() == 0)
  {
    delay(100);
    return;
  }

  String msg = Serial.readStringUntil('\n');
  if(msg == "")
  {
    delay(100);
    return;
  }
  uint8_t* uid;
  bool* auth;
  int uidLen = readPacket(msg.c_str(), msg.length(), &uid, auth);
  if(uidLen == 0)
  {
    delay(100);
    return;
  }
  writeuintarray(uid, uidLen);
  //Serial.write((uint8_t)auth);
  Serial.print("  ");
  Serial.write(uidLen);
  Serial.write("\n");
  delay(100);
}
