from machine import Pin
from mfrc522 import MFRC522
import time
import utime



from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 63 
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def greeting():
    
    lcd.clear()
    lcd.move_to(5,0)
    lcd.putstr("Bienvenido ")
    lcd.move_to(3,1)
    lcd.putstr("Verifique")

    
greeting()    

#lcd.move_to(0,0)
#lcd.putstr("Cust")
#lcd.move_to(0,1)
#lcd.putchar(chr(0))
#lcd.move_to(4,1)
#lcd.putchar(chr(1))
#lcd.move_to(8,1)
#lcd.putchar(chr(2))
#lcd.move_to(12,1)
#lcd.putchar(chr(3))
#lcd.move_to(15,1)
#lcd.putchar(chr(4))


buzzer = machine.PWM(machine.Pin(15))
servo = machine.PWM(machine.Pin(28))
servo.freq(90)


lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
    

rojo = Pin(13, Pin.OUT)
verde = Pin(14, Pin.OUT)
azul = Pin( 16, Pin.OUT)


TARJETA_1 = 540024224
LLAVERO_1 = 3070031507
TARJETA_2 = 552912016
LLAVERO_2 = 3074339651




def tone(pin,frequency,duration):
    pin.freq(frequency)
    pin.duty_u16(90000)
    utime.sleep_ms(duration)
    pin.duty_u16(0)
    
def interval_mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def servo_write(pin,angle):
    pulse_width=interval_mapping(angle, 0, 90, 0.5,2.5)
    duty=int(interval_mapping(pulse_width, 0, 20, 0,65535))
    pin.duty_u16(duty)
    



print("Lector activo...\n")




while True:
    
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
                identificador = int.from_bytes(bytes(uid),"little",False)
                
                
                if identificador == TARJETA_1:
                    print("UID: "+ str(identificador)+" Acceso concedido")
                
                
                
                rojo.value(0)
                verde.value(1)
                for angle in range(90):
                   servo_write(servo,angle)
                   utime.sleep_ms(50)
                for angle in range(0):
                    servo_write(servo,angle)
                    utime.sleep_ms(50)
                verde.value(0)
                
                
                
                if identificador == TARJETA_2:
                 lcd.putstr("Verifiqjggn")
                print("UID: "+ str(identificador)+" Acceso concedido")
                rojo.value(0)
                verde.value(1)
                time.sleep(5)
                verde.value(0)
                
            elif identificador == LLAVERO_1:
              print("UID: "+ str(identificador)+" Acceso concedido")
              rojo.value(0)
              verde.value(1)
              time.sleep(5)
              verde.value(0)
              
            elif identificador == LLAVERO_2:
              print("UID: "+ str(identificador)+" Acceso concedido")
              rojo.value(0)
              verde.value(1)
              time.sleep(5)
              verde.value(0)
                
            else:
                print("UID: "+ str(identificador)+" desconocido: Acceso denegado")
                rojo.value(1)
                tone(buzzer,700,700,)
                verde.value(0)
                time.sleep(3)
                rojo.value(0)
                            
                            
greeting() 