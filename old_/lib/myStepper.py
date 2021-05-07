import RPi.GPIO as GPIO, time
import sys
import threading

def cleanAllGPIO():
	GPIO.cleanup()

class stepper:
	#instantiate stepper 
	#pins = [stepPin, directionPin, enablePin]
	def __init__(self, pins):
		#setup pins
		self.pins = pins
		self.stepPin = self.pins[0]
		self.directionPin = self.pins[1]
		self.enablePin = self.pins[2]
		self.endStopPin = self.pins[3]
		
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.stepPin, GPIO.OUT) #STEP
		GPIO.setup(self.directionPin, GPIO.OUT) #DIR
		GPIO.setup(self.enablePin, GPIO.OUT) #ENABLE

		GPIO.setup(self.endStopPin, GPIO.IN) #EndStop

		#set enable to high (i.e. power is NOT going to the motor)
		# GPIO.output(self.enablePin, True)
		 
		self.stepping = GPIO.PWM(self.stepPin, 7000)
		print("Stepper initialized (step=" + str(self.stepPin) + ", direction=" + str(self.directionPin) + ", enable=" + str(self.enablePin) + ")")

	#clears GPIO settings
	def cleanGPIO(self):
		GPIO.cleanup()
	
#step the motor
	# steps = number of steps to take
	# dir = direction stepper will move
	# speed = defines the denominator in the waitTime equation: waitTime = 0.000001/speed. As "speed" is increased, the waitTime between steps is lowered
	# stayOn = defines whether or not stepper should stay "on" or not. If stepper will need to receive a new step command immediately, this should be set to "True." Otherwise, it should remain at "False."
	def SpinMotor(self, dire, freq):
		print("start Spin")
		GPIO.output(self.enablePin, False)
		self.stepping.ChangeFrequency(freq)
		GPIO.output(self.directionPin,dire)
		self.stepping.start(1)
		time.sleep(0.01)
		return True

	def StopMotor(self):
		self.stepping.stop()

	def SpinSteps(self, dire, steps):
		self.motorSpins = threading.Thread(target=self.SpinMotorSteps,args=(dire,steps,))
		self.motorSpins.start()
		print(self.motorSpins.is_alive())

	def SpinMotorSteps(self, dire, steps):
		GPIO.output(self.enablePin, False)
		count = 0
		while count < steps:
			if self.checkEndstop():
				break
			GPIO.output(self.stepPin, True)
			time.sleep(0.001)
			GPIO.output(self.stepPin, False)
			time.sleep(0.001)
			count+=1

	def checkEndstop(self):
		if(GPIO.input(self.endStopPin)==1):
			print("ENDSTOP")
			return False
		return True
		