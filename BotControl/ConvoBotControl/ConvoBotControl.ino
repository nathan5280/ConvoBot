#include <MeAuriga.h>

const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;
boolean newCmd = false;
boolean pendingAction = false;
char cmd[32] = {0};
int seq = 0;
int distR = 0;
int distL = 0;
int speedR = 200;
int speedL = 200;

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    
    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
      Serial.print("New Data: ");
      Serial.println(receivedChars);
    }
  }
}

void parseData() {
  if (newData) {
    // Split the command into cmd:seq:distR:distL
    // cmd: action to perform
    // seq: unique command id
    // distR: right track position
    // distL: left track position
    char * strtokIndx;                        // this is used by strtok() as an index
    
    strtokIndx = strtok(receivedChars,":");   // get the first part - the string
    strcpy(cmd, strtokIndx);                  // copy it to messageFromPC
    
    strtokIndx = strtok(NULL, ":");           // this continues where the previous call left off
    seq = atoi(strtokIndx);                   // convert this part to an integer
    
    strtokIndx = strtok(NULL, ":");           // this continues where the previous call left off
    distR = atoi(strtokIndx);                 // convert this part to an integer
    
    strtokIndx = strtok(NULL, ":"); 
    speedR = atoi(strtokIndx);                 // convert this part to an integer
  
    strtokIndx = strtok(NULL, ":");           // this continues where the previous call left off
    distL = atoi(strtokIndx);                 // convert this part to an integer
    
    strtokIndx = strtok(NULL, ":"); 
    speedL = atoi(strtokIndx);                 // convert this part to an integer

    newData = false;
    newCmd = true;

    Serial.println("Command Parsed ...");
    Serial.print(cmd);
    Serial.print(", ");
    Serial.print(seq);
    Serial.print(", ");
    Serial.print(distR);
    Serial.print(", ");
    Serial.print(speedR);
    Serial.print(", ");
    Serial.print(distL);
    Serial.print(", ");
    Serial.println(speedL);
  }
}

MeEncoderOnBoard EncoderR(SLOT1);
MeEncoderOnBoard EncoderL(SLOT2);

boolean pendingMove[2];
int extIDR = 0;
int extIDL = 1;

void initializeEncoders() {
  attachInterrupt(EncoderR.getIntNum(), isrProcessEncoderRight, RISING);
  attachInterrupt(EncoderL.getIntNum(), isrProcessEncoderLeft, RISING);
  
  //Set PWM 8KHz
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);

  TCCR2A = _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS21);

  EncoderR.setPulse(9);
  EncoderL.setPulse(9);
  EncoderR.setRatio(39.267);
  EncoderL.setRatio(39.267);
  EncoderR.setPosPid(1.8,0,1.2);
  EncoderL.setPosPid(1.8,0,1.2);
  EncoderR.setSpeedPid(0.18,0,0);
  EncoderL.setSpeedPid(0.18,0,0);

  pendingMove[0] = false;
  pendingMove[1] = false;
}

void isrProcessEncoderRight(void)
{
  if(digitalRead(EncoderR.getPortB()) == 0)
  {
    EncoderR.pulsePosMinus();
  }
  else
  {
    EncoderR.pulsePosPlus();
  }
}

void isrProcessEncoderLeft(void)
{
  if(digitalRead(EncoderL.getPortB()) == 0)
  {
    EncoderL.pulsePosMinus();
  }
  else
  {
    EncoderL.pulsePosPlus();
  }
}

void encoderCompleteCallback(int16_t slot,int16_t extID)
{
  if (pendingMove[extID]) {
    pendingMove[extID] = false;
    
    if (!pendingMove[0] && !pendingMove[1]) {
      Serial.print("G:");
      Serial.println(seq);
      pendingAction = false;
    }
  }
}

void processCmd() {
  if (newCmd && !pendingAction) {
    Serial.println("Processing commnand ...");
    pendingAction = true;
    
    switch (cmd[0]) {
      case 'T':
        Serial.print("Moving to: ");
        Serial.print(distR);
        Serial.print(", ");
        Serial.print(speedR);
        Serial.print(", ");
        Serial.print(distL);
        Serial.print(", ");
        Serial.println(speedL);

        pendingMove[extIDR] = true;
        EncoderR.setPulsePos(0);
        EncoderR.moveTo(distR, speedR, extIDR, encoderCompleteCallback);

        pendingMove[extIDL] = true;
        EncoderL.setPulsePos(0);
        EncoderL.moveTo(-distL, speedL, extIDL, encoderCompleteCallback);
        break;
      default:
        Serial.print("B:");
        Serial.println(seq);
        break;
    }
    newCmd = false;
  }
}

void dumpStatus() {
  Serial.print("Sequence: ");
  Serial.println(seq);
  Serial.print("New Data: ");
  Serial.println(newData);
  Serial.print("New Command: ");
  Serial.println(newCmd);
  Serial.print("Cmd Pending: ");
  Serial.println(pendingAction);
  delay(10000);
}

void setup() {
  Serial.begin(115200);
  Serial.println("<Arduino is ready>");
  initializeEncoders();
}

void loop() {
//  dumpStatus();
  recvWithEndMarker();
  parseData();
  processCmd();
  EncoderR.loop();
  EncoderL.loop();  
}

