import machine
import time


# UART channels for APC220 radio setup
uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))

uart2 = machine.UART(0, baudrate=9600, tx=machine.Pin(12), rx=machine.Pin(13))

# Onboard LED setup
led = machine.Pin(25, machine.Pin.OUT)


def read_uart(uart):
    if uart.any():
        try:
            return (uart.read()).decode('utf-8')
        except:
            return "None"


def write_uart(uart, data):
    uart.write((data+"\r").encode('utf-8'))


def blink_led():
    led.toggle()



while True:
    
    blink_led()
    
    # Read data from UART2 (APC220 Radio 2, Receiver)
    uart1_data = str(read_uart(uart1))
    
    uart2_data = str(read_uart(uart2))
    #write_uart(uart2, "hello")
    
    
    if uart1_data != "None":
        write_uart(uart1, uart1_data)
        print(uart1_data)

    if uart2_data != "None":
        write_uart(uart1, uart2_data)


 