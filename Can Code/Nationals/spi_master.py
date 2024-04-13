from machine import Pin, SPI
import utime

# Initialize SPI0 as master
spi0 = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cs = Pin(13, Pin.OUT)

# Set the CS pin to an idle high state
cs.value(1)

# Sample data to send
sample_data = bytearray([0x04, 0x07, 0x82, 0x03])

def send_data(data):
    cs.value(0)  # Set CS low to start transmission
    spi0.write(data)  # Write data to the SPI bus
    cs.value(1)  # Set CS high to end transmission

while True:
    send_data(sample_data)
    utime.sleep(1)  # Delay for 1 second
