


inline void setupValves()
{
  // initialize digital pin LED_BUILTIN as an output.
  for(int i=0; i<16; i++)
  {
    pinMode(valve_pin(i), OUTPUT);
    close_valve(i);
  }
}

inline void print_valve_status(HardwareSerial &serial)
{
  serial.print('|');
  for(int i=0; i<15; i++)
  {
    serial.print(digitalRead(valve_pin(i))  ? 'c' : 'o');
    serial.print('|');
  }
}

inline void loopValves()
{
  if( last_command_timestamp>0 && (millis()-last_command_timestamp) > SAFETY_OFF_TIMEOUT)
    close_all_valves();
}

inline void buzz(int period, int duration)
{
  for(int j=0; j<duration; j++)
  {
    open_valve(15); 
    delay(period);
    close_valve(15); 
    delay(period);
  }  
}

inline void open_valve(uint8_t valve_index)
{
  set_valve_state(valve_index, LOW);
}

inline void close_valve(uint8_t valve_index)
{
  set_valve_state(valve_index, HIGH);
}

inline void close_all_valves()
{  
  for(int i=0; i<16; i++)
    close_valve(i);
}

inline void set_valve_state(uint8_t valve_index, uint8_t valve_state)
{
  digitalWrite(valve_pin(valve_index), valve_state);

  if(debug_output)
  {
    Serial.print("set_valve_state(");
    Serial.print(valve_index, DEC);
    Serial.print(",");
    Serial.print(valve_state, DEC);
    Serial.println(")");
  }
  
}


inline uint8_t valve_pin(uint8_t valve_index)
{
  return 38+valve_index;
}
