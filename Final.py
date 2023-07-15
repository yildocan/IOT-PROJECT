from machine import Pin, PWM, UART, ADC
import time
import network
import BlynkLib

uart = UART(0, 9600)

led1 = Pin(2, Pin.OUT)
led2 = Pin(3, Pin.OUT)
led3 = Pin(12, Pin.OUT)
led4 = Pin(13, Pin.OUT)
touch_pin = Pin(14, Pin.IN)  # Replace 4 with the appropriate digital pin number for the touch sensor

# set PWM
pwm = PWM(Pin(15))
pwm.freq(50)  # 20ms PWM period

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ÖĞRENCİEVİ', 'Berkay347')

BLYNK_AUTH = "LJbM-3z4SjDcTX0rc7tAFhxfbRctnkjM"

# connect the network
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)


"Connection to Blynk"
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)


# Register virtual pin handler
@blynk.on("V0")  # virtual pin V0
def v0_write_handler(value):  # read the value
    if int(value[0]) == 1:
        print("ON")
        print("Left")
        pwm.duty_ns(1000000)  # dutyCycle 1ms
        time.sleep(1)
        print("Middle")
        pwm.duty_ns(1500000)  # dutyCycle 1.5ms
        time.sleep(1)
        print("Right")
        pwm.duty_ns(2000000)  # dutyCycle 2ms
        time.sleep(1)
        print("Middle")
        pwm.duty_ns(1500000)  # dutyCycle 1.5ms
        time.sleep(1)
    else:
        print("OFF")
        pwm.deinit()
        time.sleep(1)


while True:
    blynk.run()
    touch_value = touch_pin.value()  # Read the digital value of the touch sensor pin

    # Control LED on pin 13 based on touch sensor value
    if touch_value == 1:
        led4.on()
    else:
        led4.off()

    if uart.any():
        command = uart.readline()
        command = command.strip().decode()
        print(command)
        if command == "1":
            led1.on()
            led2.off()
            led3.off()
        elif command == "2":
            led1.off()
            led2.on()
            led3.off()
        elif command == "3":
            led1.off()
            led2.off()
            led3.on()