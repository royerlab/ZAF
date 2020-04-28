
#define SAFETY_OFF_TIMEOUT 1000L*60L*5L // 5 minutes

long last_command_timestamp = 0;
bool debug_output=false;

void setup() 
{
  setupSerial();
  setupValves();
  setupPWM();
}

void loop() 
{
  loopSerial();
  loopValves();
  loopPWM();

  if( last_command_timestamp>0  && (millis()-last_command_timestamp) > SAFETY_OFF_TIMEOUT)
    last_command_timestamp=-1;

  delay(1000); // Loop runs once per second
}
