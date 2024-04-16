#ifndef SEC32
#define SEC32

void createChecksum(uint8_t* data, size_t length, uint32_t* checksum, uint8_t* salt, size_t saltLength);
bool verifyChecksum(uint8_t* data, size_t length, uint32_t checksum, uint8_t* salt, size_t saltLength);

#endif
