#define SwitchPin1 2 // Setze den 1. Interruptpin auf 2
#define SwitchPin2 3 // Setze den 2. Interruptpin auf 3
//defining pin configuration
#define OnOffSwitchPin 8  //Set pin for on-off switch
#define MOTOR_IN11 9 //Definiere Motor PWM Signal Motor 1
#define MOTOR_IN12 10//Definiere Motor PWM Signal Motor 1
#define MOTOR_IN21 5 //Definiere Motor PWM Signal Motor 2
#define MOTOR_IN22 6 //Definiere Motor PWM Signal Motor 2

//setting global variables
unsigned long randtime; //Variabl für randomisierte Pause
int minTime = 20; //Minimale Warte Zeit in Sekunden
int maxTime = 100; //Maximale Warte Zeit in Sekunden
boolean motorPosition; //0 = retracted / 1 = extended
boolean isTestMove = 0; //0 = normal operation / 1 = testmove


void setup() {
  //only for debug -> wait 3 seconds for us slow humans to activate serial monitor
  delay(3000);
  
  //--initialize--
  //turn on serial communication
  Serial.begin(9600);
  //welcome message
  Serial.println("Hi there! Bänkli is powering up, please wait.");

  //define pin modes
  pinMode(MOTOR_IN11, OUTPUT);
  pinMode(MOTOR_IN12, OUTPUT);
  pinMode(MOTOR_IN21, OUTPUT);
  pinMode(MOTOR_IN22, OUTPUT);
  pinMode(OnOffSwitchPin, INPUT_PULLUP);
  pinMode(SwitchPin1, INPUT_PULLUP);
  pinMode(SwitchPin2, INPUT_PULLUP);
  
  //initialize seed for random function with random voltage reading from analog pin 0
  randomSeed(analogRead(0));
  
  //print successfull initialization
  Serial.println("Initialized successfully!");
  
  //check on-off switch and do testmove if switch is on
  if (digitalRead(OnOffSwitchPin) == 0) {
    //print test move state
    Serial.println("Doing tests moves.");
    //wait a short time before test moves
    delay(1000);

    //turning test state mode on
    isTestMove = 1;

    //doing first test move
    onState();
    
    //doing second test move
    onState();
    
    //print end of test move state
    Serial.println("Bänkli did both test moves. Proceeding to normal operation.");
    Serial.println();

    //turning test state mode off
    isTestMove = 0;
  }
  else {
    //print situation with switch off in setup
    Serial.println("Bänkli was off during initialization: did not perform test moves.");
  }
}


//main function -> checking if bänkli is on or off, if on call main function during on state, if off turn off motors
void loop() {
  //run onState if switch is on or do nothing -> turn off motors
  if (digitalRead(OnOffSwitchPin) == 0) {
    onState();
  }
  else {
    //turn off motors
    digitalWrite(MOTOR_IN11, LOW);
    digitalWrite(MOTOR_IN12, LOW);
    digitalWrite(MOTOR_IN21, LOW);
    digitalWrite(MOTOR_IN22, LOW);
    
    //print off state
    Serial.println("Bänkli is turned off.");
  } 
}


//main function during on state -> checking backrest position, setting moving direct, calculating wait time, waiting and then executing move function.
void onState() {
  //check position: switch1 activated -> motors retracted / switch2 activated -> motors extended / no switch activated -> in between position set push direction / both switches activated -> turn off motors
  //set moving direction
  if (digitalRead(SwitchPin1) == 0) {
    //switch 1 activated -> motors retracted
    motorPosition = 0;

    //print motor position and switchstate
    Serial.println("Switch 1 activated: Motors are retracted.");
  }
  else if (digitalRead(SwitchPin2) == 0) {
    //switch 2 activated -> motors extended
    motorPosition = 1;

    //print motor position and switchstate
    Serial.println("Switch 2 activated: Motors are extended.");
  }
  else if (digitalRead(SwitchPin1) == 1 & digitalRead(SwitchPin2) == 1) {
    //both switches off -> set motor to retracted position
    motorPosition = 0;

    //print motor position and switchstate
    Serial.println("No switch activated: set motors to retracted position.");
  }
  else {
    //both switches on -> turn off motors
    digitalWrite(MOTOR_IN11, LOW);
    digitalWrite(MOTOR_IN12, LOW);
    digitalWrite(MOTOR_IN21, LOW);
    digitalWrite(MOTOR_IN22, LOW);
    
    //print error state
    Serial.println("Both switches activated: Motors turned off, check for mechanical error!");
  }

  //calculate random time if no test move
  if (isTestMove == 0) {
    //calculate random time
    randtime = random(minTime, (maxTime + 1)) * 1000;
  }
  else {
    //set waittime between moves to 1 second while doing testmoves
    randtime = 1000;
  }
  
  //print waittime
  Serial.print("Bänkli will make its next move in ");
  Serial.print((randtime / 1000));
  Serial.println(" seconds.");
  
  //wait random time
  delay(randtime);

  //print activation of motor move
  Serial.println("Activating motors.");
  
  //move Backrest
  moveBackrest(motorPosition);
}


//function to move motors to desired position and then turning them off
void moveBackrest(int moveDirection) {
  //switch-case which moving direction. moveDirection = 0 -> motors retracted -> push / moveDirection = 1 -> motors extended -> pull
  switch (moveDirection) {
    //move motors to extended position until switch2 gets activated
    case 0:
      //print motor extension move
      Serial.println("Extending motors until Switch 2 gets activated");
      
      //move motors until switch 2 gets activated
      while (digitalRead(SwitchPin2) == 1) {
        digitalWrite(MOTOR_IN11, LOW);
        digitalWrite(MOTOR_IN21, LOW);
        digitalWrite(MOTOR_IN12, HIGH);
        digitalWrite(MOTOR_IN22, HIGH);
      }
      //print switch 2 activation
      Serial.println("Switch 2 was activated.");
      break;
      
    //move motors to retracted until switch1 gets activated
    case 1:
      //print motor extension move
      Serial.println("Retracting motors until Switch 1 gets activated");

      //move motors until switch 1 gets activated
      while (digitalRead(SwitchPin1) == 1) {
        digitalWrite(MOTOR_IN12, LOW);
        digitalWrite(MOTOR_IN22, LOW);
        digitalWrite(MOTOR_IN11, HIGH);
        digitalWrite(MOTOR_IN21, HIGH);
      }
      //print switch 1 activation
      Serial.println("Switch 1 was activated.");
      break;
  }
  
  //turn off motors after move is done
  digitalWrite(MOTOR_IN11, LOW);
  digitalWrite(MOTOR_IN12, LOW);
  digitalWrite(MOTOR_IN21, LOW);
  digitalWrite(MOTOR_IN22, LOW);

  //print motor turn off and move made
  Serial.println("Moved motors to new position and turned them off");
  Serial.println();
}
