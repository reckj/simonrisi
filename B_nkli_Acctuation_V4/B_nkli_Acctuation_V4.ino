#define SwitchPin1 2 // Setze den 1. Interruptpin auf 2
#define SwitchPin2 3 // Setze den 2. Interruptpin auf 3
#define MOTOR_IN11 9 //Definiere Motor PWM Signal Motor 1
#define MOTOR_IN12 10//Definiere Motor PWM Signal Motor 1
#define MOTOR_IN21 5 //Definiere Motor PWM Signal Motor 2
#define MOTOR_IN22 6 //Definiere Motor PWM Signal Motor 1
int state = 0; // state of state machine at initialisation
int motionState = 0; // state of motion before interrupt is called (to ensure sensor cannot be called twice in a row)
int i = 0; //pwm ramp up Variabel initialisieren
unsigned long randtime; //Variabl für randomisierte Pause
int minTime = 20; //Minimale Warte Zeit in Minuten
int maxTime = 100; //Maximale Warte Zeit in Minuten

void setup()// put your setup code here, to run once:
{
  Serial.begin(9600); //Serial com
  Serial.println("Bänkil_Motion");
  pinMode(MOTOR_IN11, OUTPUT); //Definiere Pin Mode
  pinMode(MOTOR_IN12, OUTPUT);
  pinMode(MOTOR_IN21, OUTPUT);
  pinMode(MOTOR_IN22, OUTPUT);
  pinMode(8, INPUT_PULLUP); //Pin Für Schalter
  pinMode(SwitchPin1, INPUT_PULLUP);
  pinMode(SwitchPin2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SwitchPin1), stopUno, FALLING); //Interupt von Switch Sensoren --> Wechselt State auf "Stop" wenn interrupt aktiv
  attachInterrupt(digitalPinToInterrupt(SwitchPin2), stopDue, FALLING);
  randomSeed(analogRead(0)); //Initialize Random function every time Programm starts

  //Initialize Statemachine with current state
  if (digitalRead(SwitchPin1) == LOW)
  {
    state = 0;
    Serial.println("Switch1 active");
  }
  else if (digitalRead(SwitchPin2) == LOW)
  {
    state = 1;
    Serial.println("Switch2 active");
  }
  else
  {
    state = 2;
    Serial.println("None active");
  }
}

void loop() // Läuft ununterbrochen ab
{
  if (digitalRead(8) == LOW) //überprüft ob schalter an oder aus ist
  {
    /*Serial.println(state);*/
    switch (state) //Verschiedene States und damit verbundene Aktionen
      //state = 0: Switch1 (Motor eingezogen) aktiv: Stoppt Bewegung, um nach random Zeit zu Ausfahren zu wechseln
      //state = 1: Switch2 (Motor ausgefahren) aktiv: Stoppt Bewegung, um nach random Zeit zu Einfahren zu wechseln
      //state = 2: Ausfahren
      //state = 3: Einfahren
    {
      case 0: //Switch1 (Motor eingezogen) aktiv: Stoppt Bewegung, um nach random Zeit zu Ausfahren zu wechseln
        if (motionState == 3)
        {
          digitalWrite(MOTOR_IN11, LOW);
          digitalWrite(MOTOR_IN12, LOW);
          digitalWrite(MOTOR_IN21, LOW);
          digitalWrite(MOTOR_IN22, LOW);
          Serial.println("Switch2 active"); //Ausgabe des Status
          i = 0;
          randtime = random(minTime, (maxTime + 1)) * 1000;
          Serial.println((randtime / 1000));
          delay(randtime);
          state = 2;
        }
        else
        {
          state = 2;
        }
        break;

      case 1: //Switch2 (Motor ausgefahren) aktiv: Stoppt Bewegung, um nach random Zeit zu Einfahren zu wechseln
        if (motionState == 2)
        {
          digitalWrite(MOTOR_IN11, LOW);
          digitalWrite(MOTOR_IN12, LOW);
          digitalWrite(MOTOR_IN21, LOW);
          digitalWrite(MOTOR_IN22, LOW);
          Serial.println("Switch1 active"); //Ausgabe des Status
          i = 0;
          randtime = random(minTime, (maxTime + 1)) * 1000;
          Serial.println((randtime / 1000));
          delay(randtime);
          state = 3;
        }
        else
        {
          state = 3;
        }
        break;

      case 2: //Ausfahren
        motionState = 2;
        digitalWrite(MOTOR_IN11, LOW); //Definiere Ground
        digitalWrite(MOTOR_IN21, LOW);
        digitalWrite(MOTOR_IN12, HIGH); //Motor auf Full Speed
        digitalWrite(MOTOR_IN22, HIGH);
        Serial.println("Push");
        break;

      case 3://Einfahren
        motionState = 3;
        digitalWrite(MOTOR_IN12, LOW); //Definiere Ground
        digitalWrite(MOTOR_IN22, LOW);
        digitalWrite(MOTOR_IN11, HIGH); //Motor auf Full Speed falls vorhin kein Stillstand (und somit kein Ramp up nötig)
        digitalWrite(MOTOR_IN21, HIGH);
        Serial.println("Pull"); //Ausgabe des Status
        break;
    }
  }
  else
  {
    digitalWrite(MOTOR_IN11, LOW); //Motoren Abstellen falls Schalter auf Aus ist
    digitalWrite(MOTOR_IN12, LOW);
    digitalWrite(MOTOR_IN21, LOW);
    digitalWrite(MOTOR_IN22, LOW);
  }
}

void stopUno() //Funktion wenn Switchsensor 1 ausgelost wird (Wechsel zu case/state 0)
{
  state = 0;
}

void stopDue() //Funktion wenn Switchsensor 1 ausgelost wird (Wechsel zu case/state 0)
{
  state = 1;
}
