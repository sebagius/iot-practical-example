#import "security.h"

/* Code below this point was solely written by myself (i do a lot of c coding i love it) - apart from the use of libraries ofc i didn't write the CRC32 framework */

/* CRC32 allows us to create a 32bit checksum (4 byte) while obviously not strong it is still a minor security implementation meaning that if serial communication man in the middle will be harder since the secret needs to be known to send data - we don't care if they can read data because they won't know the secret */

CRC32 crc;

void printuint8_t(uint8_t* st, size_t len)
{
  for(int i = 0; i < len; i++)
  {
    Serial.print(st[i]);
  }
  Serial.println();
}

void createChecksum(uint8_t* data, size_t length, uint32_t* checksum, uint8_t* salt, size_t saltLength)
{
  size_t totalLength = length + saltLength;
  uint8_t* salty = malloc(totalLength);
  memcpy(salty, data, length);
  memcpy(salty+length, salt, saltLength);
  uint32_t check = CRC32::calculate(salty, totalLength);
  free(salty);
  *checksum = check;
}

bool verifyChecksum(uint8_t* data, size_t length, uint32_t checksum, uint8_t* salt, size_t saltLength)
{
  uint32_t* check = malloc(sizeof(uint32_t));
  createChecksum(data, length, check, salt, saltLength);
  Serial.println("verifying data:");  
  Serial.println(*check);
  Serial.println("\n");

  return *check == checksum;
}
