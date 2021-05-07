import RPi.GPIO as GPIO, time
import sys
import threading
import queue

stepPin = 10
dirPin = 12
enablePin = 8

count = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepPin, GPIO.OUT) #STEP
GPIO.setup(dirPin, GPIO.OUT) #DIR
GPIO.setup(enablePin, GPIO.OUT) #ENABLE

GPIO.setup(37, GPIO.IN) #input

GPIO.output(enablePin, True)

p = GPIO.PWM(stepPin, 7000)

def SpinMotor(dire):
    GPIO.output(enablePin, False)
    p.ChangeFrequency(500)
    GPIO.output(dirPin,dire)
    p.start(1)
    print("test")
    time.sleep(0.01)
    return True



def runner(run_queue):
    running = False
    global count
    while True:
        try:
            speed = run_queue.get_nowait()
            if speed==0:
                running = False
            elif speed<0:
                running = True
                dire = 0
            elif speed>0:
                running = True
                dire = 1
        except queue.Empty:
            pass

        if(running):
            GPIO.output(dirPin,dire)
            GPIO.output(enablePin, False)
            GPIO.output(stepPin, True)
            time.sleep(abs(0.001/speed))
            GPIO.output(stepPin, False)
            time.sleep(abs(0.001/speed))
            count+=1
        


def SpinMotorSteps(steps):
    GPIO.output(enablePin, False)
    count = 0
    while count < steps:
        GPIO.output(stepPin, True)
        time.sleep(0.001)
        GPIO.output(stepPin, False)
        time.sleep(0.001)
        count+=1

def testME(steps):
    count = 0
    while count < steps:
        print("test")
        time.sleep(1)
        count+=1

run_queue = queue.Queue()
threading.Thread(target=runner, args=(run_queue,)).start()

while True:
    dir_input = input("Enter your dir: ") 
    if dir_input == "F":
        SpinMotor(True)
    elif dir_input == "B":
        SpinMotor(False)
    elif dir_input == "test":
        motorSpins = threading.Thread(target=SpinMotorSteps,args=(10000,))
        motorSpins.start()
    elif dir_input == "stop":
        p.stop()  
        dir_input = ""
    elif dir_input == "SHOW":
        print(count)
        GPIO.output(enablePin, True)
    elif dir_input == "RUN1":
        run_queue.put(50)
    elif dir_input == "RUN2":
        run_queue.put(-10)
    elif dir_input == "NORUN":
        run_queue.put(0)
    elif dir_input == "shutdown":
        p.stop()
        GPIO.cleanup()
        break
