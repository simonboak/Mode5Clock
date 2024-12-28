from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from luma.core.render import canvas
from datetime import datetime
import mode5, os, time, digits, pyky040, threading

def rotary_callback(scale_position):
  global sleepy_time
  sleepy_time = scale_position

def shutdown_callback():
  os.system("sudo shutdown now -h")

def get_current_time_digits():
  global hour_first_digit
  global hour_second_digit
  global minute_first_digit
  global minute_second_digit

  now = datetime.now()
  hour = now.hour
  hour_first_digit = hour // 10
  hour_second_digit = hour % 10
  minute = now.minute
  minute_first_digit = minute // 10
  minute_second_digit = minute % 10

def draw_digit(draw, digit, xPos, yPos):
  x = xPos
  for col in digits.get_digit(digit):
    y = yPos
    for i in range(7, -1, -1):
      if (col & (1 << i)):
        draw.rectangle((x + 1, y + 1, x + 3, y + 3), fill="white")
      y += 4
    x += 4

def draw_time(draw):
  if hour_first_digit > 0: draw_digit(draw, hour_first_digit, 72, 16)
  draw_digit(draw, hour_second_digit, 100, 16)
  draw_digit(draw, minute_first_digit, 136, 16)
  draw_digit(draw, minute_second_digit, 164, 16)

  draw.rectangle((129, 25, 131, 27), fill="white")
  draw.rectangle((129, 37, 131, 39), fill="white")

def main():
  global in_time_transition
  global hour_first_digit
  global hour_second_digit
  global minute_first_digit
  global minute_second_digit

  rotary_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)
  rotary_encoder.setup(scale_min=0.01, scale_max=0.1, initial_pos=0.05, step=0.01, chg_callback=rotary_callback, sw_callback=shutdown_callback)
  rotary_thread = threading.Thread(target=rotary_encoder.watch)
  rotary_thread.daemon = True
  rotary_thread.start()

  fill = 50
  fill_direction = 1
  fill_string = "rgb(50%,50%,50%)"

  get_current_time_digits()
  current_minutes = datetime.now().minute

  while True:
    with canvas(device) as draw:
      x = 0
      for row in mode5.rows:
        y = 0
        for i in range(15, -1, -1):
          if not (row & (1 << i)):
            draw.rectangle((x + 1, y + 1, x + 3, y + 3), fill=fill_string)
          y += 4
        x += 4
      draw_time(draw)
    
    # Check if the minutes have changed since the previous loop
    if current_minutes != datetime.now().minute:
      in_time_transition = True
      current_minutes = datetime.now().minute

    # A clumsy way of fading the animation in and out when the minute changes
    if in_time_transition:
      if fill_direction > 0:
        fill -= 5
        if fill < 40:
          fill = 40
          fill_direction = -1
          in_time_transition = False
      else:
        fill += 5
        if fill > 150:
          fill = 100
          fill_direction = 1
          get_current_time_digits()
    fill_string = "rgb({}%,{}%,{}%)".format(fill, fill, fill)

    mode5.next_cycle()
    time.sleep(sleepy_time)

if __name__ == "__main__":
  try:
    in_time_transition = False
    sleepy_time = 0.05
    serial = spi(device=0, port=0)
    device = ssd1322(serial)
    main()
  except KeyboardInterrupt:
    pass
