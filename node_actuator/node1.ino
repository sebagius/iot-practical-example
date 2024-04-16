#import <CRC32.h>
#import "ledmatrix.h"
#import "security.h"

//unsigned char table[16] = {0x00, 0x3E, 0x28, 0x28, 0x16, 0x00, 0x3E, 0x00, 0x26, 0x2A, 0x32, 0x00, 0x26, 0x2A, 0x32, 0x00};
unsigned char table[16] = {0x00, 0x32, 0x2A, 0x26, 0x00, 0x32, 0x2A, 0x26, 0x00, 0x3E, 0x00, 0x16, 0x28, 0x28, 0x3E, 0x00};
uint8_t* ourSecret = "thisisasmallstepforsecurity!";

void setup()
{
  Serial.begin(9600);
  setupDisplay();
}

void loop()
{
  //uint8_t* testdata = "hellooo";
  //verifyChecksum(testdata, 7, 0x00000001, ourSecret, 28);
  updateDisplay(table);
  if(Serial.available() == 0)
  {
    delay(1000);
    return;
  }

  String msg = Serial.readStringUntil('\n');
  updateDisplay(table);
  delay(100);
}
