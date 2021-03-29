import RPi.GPIO as GPIO, os, sys, kintone, time
from kintone import getCurrentTimeStamp

GPIO.setmode (GPIO.BCM)
motionPin=21
irledPin=4

#GPIO.setmode(GPIO.BOARD)
#motionPin = 40
#irledPin = 4

interval=3
timeStamp=getCurrentTimeStamp()
GPIO.setup (irledPin, GPIO.OUT)
GPIO.setup(motionPin, GPIO.IN)

GPIO.setwarnings(False)
GPIO.output(irledPin, GPIO.HIGH)   # make irledPin output HIGH level, turn off led

# Taka's kintone account
#sdomain="subaru-bingo"
#appId="5"
#token="Lce6iZOKCaxzlGLNiDlz0flt1DUvw5rjLc42rinr"

# Hiro's kintone account
sdomain = "montezuma-nm"
appId = "3"
token = "qj73xLYeAa1py4eIOFYA1gKEQfjW8cfW1tZK10yQ"

while True:
    try:
        if GPIO.input(motionPin)==GPIO.HIGH:
            videoFile=timeStamp+".h264"
            GPIO.output(irledPin, GPIO.LOW)
            command1 ="raspivid -t 30000 -w 640 -h 480 -o " + videoFile
            status = os.system(command1)
        

            if(status==0):
                print(timeStamp, end=" ")
                print("A bird came!")
                mp4File = timeStamp + ".mp4"
                command2 = "MP4Box -quiet -add " + videoFile + " " + mp4File
                os.system(command2)
                command3 = "rm " + videoFile
                os.system(command3)
                GPIO.output(irledPin, GPIO.HIGH)
            else:
                print("THE BIRD DOESN'T LIKE YOU")
                sys.exit()
            
            fileKey=kintone.uploadFile(subDomain=sdomain,
                                       apiToken=token,
                                       filePath=mp4File)
            if fileKey is None:
                sys.exit()
                
            memo="Bird activity! (MP4 Video)" + timeStamp + ". "
            payload={"app": appId,
                     "record": {"photo": {"value": [{"fileKey": fileKey}] },
                                "memo": {"value": memo} }}
            
            recordId=kintone.uploadRecord(subDomain=sdomain,
                                          apiToken=token,
                                          record=payload)
            if recordId is None:
                sys.exit()
            
            command4 = "rm " + mp4File
            os.system(command4)
            
    except KeyboardInterrupt:
        break
    
GPIO.cleanup()