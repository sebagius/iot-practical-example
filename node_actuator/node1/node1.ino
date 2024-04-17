#import <CRC32.h>
#import "ledmatrix.h"
#import "security.h"

//unsigned char table[16] = {0x00, 0x3E, 0x28, 0x28, 0x16, 0x00, 0x3E, 0x00, 0x26, 0x2A, 0x32, 0x00, 0x26, 0x2A, 0x32, 0x00};
unsigned char table[16] = {0x00, 0x32, 0x2A, 0x26, 0x00, 0x32, 0x2A, 0x26, 0x00, 0x3E, 0x00, 0x16, 0x28, 0x28, 0x3E, 0x00};
uint8_t* ourSecret = "thisisasmallstepforsecurity!";
size_t ourSecretLen = 28;

uint8_t* currentMessage;
size_t currentMessageLen;

void setup()
{
  Serial.begin(9600);
  setupDisplay();
  updateDisplay(table);
}

void writeuintarray(uint8_t* d, size_t len)
{
  for(int i = 0; i < len; i++)
  {
    Serial.write(d[i]);
  }
}

uint8_t magic = 0xda;

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
      memcpy(*uid, msg, i-3);
      *auth = (uint8_t)msg[i] == magic; // or 0xda our magic auth number!!
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
  //updateDisplay(table);
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
  currentMessage = msg.c_str();
  currentMessageLen = msg.length();
  uint8_t* uid;
  bool *auth = malloc(sizeof(bool));
  int uidLen = readPacket(currentMessage, currentMessageLen, &uid, auth);
  if(uidLen == 0)
  {
    delay(100);
    return;
  }
  unsigned char* buf = malloc(4);
  Serial.readBytes(buf, 4);
  uint32_t checks = 0;
  memcpy(&checks, buf, 4);
  bool verify = verifyChecksum(currentMessage, currentMessageLen, checks, ourSecret, 28);
  if(!verify)
  {
    delay(100);
    return;
  }
  char* tab = calloc(sizeof(char), 16);
  memcpy(tab, uid, uidLen);
  updateDisplay(tab);
  Serial.write("\n");
  delay(100);
}
