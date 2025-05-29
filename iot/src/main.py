# Este script é feito para ser executado no Ubuntu oficial da Orange Pi
# A instalação do wiringpi deve ser feita seguindo o passo a passo 

import asyncio
import time
import wiringpi as wp


WHI_LED_PIN = 2
RED_LED_PIN = 5
DOOR_SENSOR_PIN = 11


wp.wiringPiSetup()
wp.pinMode(WHI_LED_PIN, wp.GPIO.OUTPUT)
wp.pinMode(RED_LED_PIN, wp.GPIO.OUTPUT)
wp.pinMode(DOOR_SENSOR_PIN, wp.GPIO.INPUT)
#wp.pullUpDnControl(DOOR_SENSOR_PIN, wp.GPIO.PUD_UP)


async def send_state():
    wp.digitalWrite(WHI_LED_PIN, wp.GPIO.HIGH)
    await asyncio.sleep(2)
    wp.digitalWrite(WHI_LED_PIN, wp.GPIO.LOW)
    await asyncio.sleep(2)


async def receive_message():
    wp.digitalWrite(RED_LED_PIN, wp.GPIO.HIGH)
    await asyncio.sleep(2)
    wp.digitalWrite(RED_LED_PIN, wp.GPIO.LOW)
    await asyncio.sleep(2)


async def task_send_state():
    while True:
        await send_state()


async def task_receive_message():
    while True:
        await receive_message()


async def main():
    asyncio.create_task(task_send_state())
    asyncio.create_task(task_receive_message())

    print("Blinking – Ctrl-C to stop")
    prev_door_sensor = wp.digitalRead(DOOR_SENSOR_PIN)
    try:
        while True:
            door_state = wp.digitalRead(DOOR_SENSOR_PIN)
            print(door_state)

            if door_state != prev_door_sensor:
                print(f"The door is {'open' if door_state else 'closed'}")
                prev_door_sensor = door_state

            await asyncio.sleep(0.1)
    except:
        print("error occurred")
    finally:
        wp.digitalWrite(RED_LED_PIN, wp.GPIO.LOW)
        wp.digitalWrite(WHI_LED_PIN, wp.GPIO.LOW)
        [t.cancel() for t in asyncio.all_tasks()]
        print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())

