import mraa, time
import signal, sys

def control_c_handler(signum, frame):
  print('')
  print("show's over!")
  for led in leds:
    led.write(0)
  time.sleep(1)
  for led in leds:
    led.write(1)
  sys.exit(0)

signal.signal(signal.SIGINT, control_c_handler)

leds = []
for i in range(2,10):
  led = mraa.Gpio(i)
  led.dir(mraa.DIR_OUT)
  leds.append(led)
  led.write(1)

while True:
  leds[3].write(0)
  time.sleep(0.2)
  leds[3].write(1)
  leds[4].write(0)
  time.sleep(0.2)
  leds[4].write(1)
