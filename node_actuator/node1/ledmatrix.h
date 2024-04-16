#ifndef LEDMTRX
#define LEDMTRX
void IIC_start();
void IIC_send(unsigned char send_data);
void IIC_end();

void updateDisplay(unsigned char tb[16]);
void setupDisplay();
#endif
