from lora import LoRa
from machine import Pin, SPI, UART
from time import sleep


mainuart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
gpsuart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

led = Pin(25, Pin.OUT)
led.on()

# Chip select
CS   = 13
# Receive IRQ
RX   = 15
# Setup SPI
spi = SPI(1, baudrate=10000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
spi.init()

# Setup LoRa
lora = LoRa(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    frequency=868.0,
    bandwidth=600000,
    spreading_factor=7,
    coding_rate=5,
)

def uart_send(chosenuart, data):
    try:
        chosenuart.write(data)
        
    except Exception as e:
        print("Send Error: " +str(e))
    

# Receive handler
def handler(x):
    led.off()
    if x[:1] == b"$":
        uart_send(gpsuart, x)
    else:
        uart_send(mainuart, x)
        uart_send(mainuart, "rssi("+lora.get_rssi()+")"+"\r\n".encode('utf-8'))
        
    #temp    
    try:
        x = x.decode('utf-8')
        x = x.strip()
        print(x)
    except:
        print("Error" + str(x))
    #print(lora.get_rssi())


# Set handler
lora.on_recv(handler)
# Put module in recv mode
lora.recv()
print("Running..")

while True:
    led.on()
    pass

