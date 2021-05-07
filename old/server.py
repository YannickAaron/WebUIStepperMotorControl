from aiohttp import web
import socketio
import RPi.GPIO as GPIO, time
import sys

from lib import myStepper

myStepper.cleanAllGPIO()

motor = []

motor.append(myStepper.stepper([10, 12, 8, 37])) #step dir enable endstop

motor.append(myStepper.stepper([13, 11, 15, 37])) #step dir enable endstop


## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
    with open('slider.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('SpinMotor')
async def print_message(sid, speed, motorNr, direction):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print('Spin Motor')
    print(direction)
    speed = int(speed)*10
    motor[motorNr].SpinMotor(direction,speed)

@sio.on('SpinMotorSteps')
async def print_message(sid, speed, motorNr, direction, steps):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print('Spin Motor')
    print(steps)
    steps = int(steps)
    motor[motorNr].SpinSteps(direction,steps)

@sio.on('ChangeSpeed')
async def print_message(sid, motorNr, speed):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print('Change Speed')
    speed = int(speed)*10
    motor[motorNr].stepping.ChangeFrequency(speed)

@sio.on('StopMotor')
async def print_message(sid, motorNr):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print('STOP MOTOR')
    motor[motorNr].StopMotor()

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)
app.router.add_static('/src/',path='src',name='src')

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)