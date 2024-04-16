#define IIC_SCL A5
#define IIC_SDA A4

#import "ledmatrix.h"

/* Code below this point is based on the datasheet for the LCD Matrix - modified by myself */
void setupDisplay()
{
  pinMode(IIC_SCL, OUTPUT);
  pinMode(IIC_SDA, OUTPUT);
  digitalWrite(IIC_SCL, LOW);
  digitalWrite(IIC_SDA, LOW);
}

void updateDisplay(unsigned char tb[16])
{
  IIC_start();
  IIC_send(0x40);
  IIC_end();
  IIC_start();
  IIC_send(0xc0);// set the initial address as 0

  /* Data Display */
  for (char i = 0; i < 16; i++)
  {
    Serial.write(tb[i]);
    IIC_send(tb[i]);
  }
  IIC_end();

 
  /* brightness */
  IIC_start();
  IIC_send(0x8A);
  IIC_end();
}

/* Code below here is directly taken from the LCD Matrix datasheet without modification */
/* Couldn't get hardware i2c working so had to rely on software i2c instead */
void IIC_start()
{
  digitalWrite(IIC_SCL, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SCL, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, LOW);
  delayMicroseconds(3);
}

void IIC_send(unsigned char send_data)
{
  for (char i = 0; i < 8; i++)
  {
    digitalWrite(IIC_SCL, LOW);
    delayMicroseconds(3);
    if (send_data & 0x01)
    {
      digitalWrite(IIC_SDA, HIGH);
    }
    else
    {
      digitalWrite(IIC_SDA, LOW);
    }
    delayMicroseconds(3);
    digitalWrite(IIC_SCL, HIGH);
    delayMicroseconds(3);
    send_data = send_data >> 1;
  }
}

void IIC_end()
{
  digitalWrite(IIC_SCL, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, LOW);
  delayMicroseconds(3);
  digitalWrite(IIC_SCL, HIGH);
  delayMicroseconds(3);
  digitalWrite(IIC_SDA, HIGH);
  delayMicroseconds(3);
}
