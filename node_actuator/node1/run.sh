#arduino-clin core install arduino:avr
#arduino-cli lib install crc32
arduino-cli board attach -p /dev/ttyACM0 -b arduino:avr:uno
arduino-cli compile
arduino-cli upload
