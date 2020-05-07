
#define min_speed 30
#define max_speed 255

#include <Servo.h>
Servo myservo;

inline void setupPWM()
{
  //Setup Channel B
  for(int i=0; i<10; i++)
  {
    pinMode(pwm_pin(i), OUTPUT);
    set_pwm_state(i, 0);
  }
  myservo.attach(7);
  
}

inline void print_pwm_status(HardwareSerial &serial)
{
  serial.print('|');
  for(int i=0; i<10; i++)
  {
    serial.print(digitalRead(pwm_pin(i)), DEC);
    serial.print('|');
  }
}

inline void loopPWM()
{
  if( last_command_timestamp>0 && (millis()-last_command_timestamp) > SAFETY_OFF_TIMEOUT)
    turn_off_all_pwm();
}

inline void turn_off_all_pwm()
{  
  for(int i=0; i<10; i++)
    set_pwm_state(i, 0);
  myservo.write(0); 
}

inline void set_pwm_state(uint8_t pwm_index, uint8_t pwm_value)
{
  if(pwm_index==5)
  {
   myservo.write(constrain(pwm_value,0,200)); 
  }
  else
  {
    analogWrite(pwm_pin(pwm_index), pwm_value);
    
    if(debug_output)
    {
      Serial.print("set_pwm_state(");
      Serial.print(pwm_index, DEC);
      Serial.print(",");
      Serial.print(pwm_value, DEC);
      Serial.println(")");
    }
  }
}


inline uint8_t pwm_pin(uint8_t pwm_index)
{
  return 2+pwm_index;
}
