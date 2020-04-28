

#define SERIAL_SPEED 500000

inline void setupSerial()
{
  // FROM USB:
  Serial.begin(SERIAL_SPEED); 

  //Forward to next arduino in the chain:
  Serial1.begin(SERIAL_SPEED);

  //Receive from another arduino:
  Serial2.begin(SERIAL_SPEED);

  //not used, just a 'terminator':
  Serial3.begin(SERIAL_SPEED);

  // Set timeouts:
  Serial.setTimeout(100);
  Serial1.setTimeout(100);
  Serial2.setTimeout(100);
  
  
  Serial.println("ZAF's Arduino Control Module (ROYER LAB)\n");
}


inline void loopSerial()
{
  // nothing to do here
}


void serialEvent() 
{
  if(debug_output)
    Serial.println("Received data on Serial0");
  process_serial(Serial, Serial1);
}

void serialEvent1() 
{
  if(debug_output)
    Serial.println("Received data on Serial1");
  while (Serial1.available())
  { 
    char c = Serial1.read();
    Serial.write(c);
    Serial2.write(c);
  }
}

void serialEvent2() 
{
  if(debug_output)
    Serial.println("Received data on Serial2");
  process_serial(Serial2, Serial3);
}

void process_serial(HardwareSerial &input_serial, HardwareSerial &forward_serial)
{
  while (input_serial.available()) 
  {
    // get the new byte:
    char startchar = (char)input_serial.read();

//    if(debug_output)
//      Serial.println(startchar);

    // Start of command
    if(startchar == '#')
    {
      //update last_command_timestamp:
      last_command_timestamp = millis();
      
      // Read command type:
      char command = (char)input_serial.read();
//      if(debug_output)
//        Serial.println(command);

      if(command == '?')
      {
        print_valve_status(input_serial);
        print_pwm_status(input_serial);
        forward_serial.print("#?\n");
      }
      else if (command== '!')
      {
        close_all_valves();
        turn_off_all_pwm();
        forward_serial.print(startchar);
        forward_serial.print(command);
        forward_serial.print("\n");
        forward_serial.flush();  
      }
      else if (command== 'd')
      {
        debug_output = input_serial.parseInt(SKIP_WHITESPACE) > 0;
      }
      else if(command == 'b')
      {
        int period = input_serial.parseInt(SKIP_WHITESPACE);
        int duration = input_serial.parseInt(SKIP_WHITESPACE);
        buzz(period, duration);  
      }
      else if(command == 't')
      {
        //  type of test?
        char type = (char)input_serial.read();
        int repeats = input_serial.parseInt(SKIP_WHITESPACE);
        int port_index = input_serial.parseInt(SKIP_WHITESPACE);

        for(int r=0; r<repeats; r++)
        {
          
          buzz(10,10);
          //forward_serial.print("#b 10 10\n"); 

          forward_serial.print(startchar);
          forward_serial.print(command);
          forward_serial.print(type);
          forward_serial.print(1, DEC);
          forward_serial.print(port_index-10, DEC);
          forward_serial.print("\n");
          forward_serial.flush();  

          if(type=='v')
          {
            for(int i=0; i<15; i++)
            {
               open_valve(i); 
               delay(300);
               close_valve(i); 
               delay(300);
            }
          }
          else if(type=='p')
          {
            if(port_index>=0 && port_index<10)
              for(int j=0; j<180; j++)
              {
                if(debug_output)
                  Serial.println(j, DEC);
                set_pwm_state(port_index, j); 
                delay(10);
              }         
          }
        }
      }
      else if(command == 'v')
      {
        // Command to open/close valves:

        //  Open or close?
        char openclose = (char)input_serial.read();

        // valve index:
        int valve_index = input_serial.parseInt(SKIP_WHITESPACE);

        if(valve_index<15)
        {
          if(openclose == 'o')
            open_valve(valve_index);
          else if (openclose == 'c')
            close_valve(valve_index);
          else if (openclose == '!')
          {
            close_all_valves();
            forward_serial.print("#v!\n");
            forward_serial.flush();
          }
        }
        else
        {
          forward_serial.print(startchar);
          forward_serial.print(command);
          forward_serial.print(openclose);
          forward_serial.print(valve_index-15, DEC);
          forward_serial.print("\n");
          forward_serial.flush();  
        }
      }
      else if (command == 'p')
      {
        int pwm_index = input_serial.parseInt(SKIP_WHITESPACE);
        int pwm_state = input_serial.parseInt(SKIP_WHITESPACE);
          
        if(pwm_index<10)
        {      
          pwm_state = constrain(pwm_state, 0, 255); 
          set_pwm_state(pwm_index, pwm_state); 
        }
        else
        {
          forward_serial.print(startchar);
          forward_serial.print(command);
          forward_serial.print(pwm_index-10, DEC);
          forward_serial.print("\t");
          forward_serial.print(pwm_state, DEC);      
          forward_serial.print("\n");
          forward_serial.flush();
        }
        
      }
      else
      {
        if(debug_output)
          input_serial.print("command not recognised!\n");
      }

      input_serial.print("done!\n");
      forward_serial.flush();
    }

  }
}
