import serial, time

ser = serial.Serial('/dev/cu.wchusbserial1420', 115200)

exit = False

seq = 0
while not exit:
    time.sleep(2)
    # Need to clean up how we are reading the responses from the bot.
    # Right now it is sending a bunch of comments and we aren't cleaning them up.
    while ser.inWaiting() > 0:
        myData = ser.readline()
        cleanedData = myData.strip().decode('utf-8')
        print(cleanedData)

    seq += 1
    cmd = input('Enter command: ')
    if cmd == 'x':
        exit = True
    elif cmd == 'T':
        # Need to check to make sure the speed is positive.  If we specify
        # a negative speed and a positive distance we will run for ever as
        # we will never reach the encoder positive location.
        right_dist = input('Right distance: ')
        right_speed = input('Right speed: ')
        left_dist = input('Left distance: ')
        left_speed = input('Left speed: ')
        cmdText = cmd + ':' + str(seq) + ':' + \
                    str(right_dist) + ':' + \
                    str(right_speed) + ':' + \
                    str(left_dist) + ':' + \
                    str(left_speed) + '\n'
        print(cmdText.encode('utf-8'))
        ser.write(cmdText.encode('utf-8'))
