# ZAF 2.0 ControlBox

This is the Arduino code for ZAF's 2.0 'ControlBox'
The control box centralises control to the valves, pumps, 
and servo and more

## How to install/update on the arduino:

The main sketch (controlbox) must be uploaded to _both_ arduino megas.
Nothing else needs to be done.

## Connections:

The ControlBox firmware supports a nearly unlimited of chained arduinos, 
making the design infinitely scalable. We use serial connections via USB 
and UART at a speed of at 500'000 bps.

The first arduino in the chain receives messages per USB, messages are forwarded 
on the Serial1 port. Corresponding (Serial1) TX and RX lines must be connected 
to the RX and TX lines of the next arduino's Serial2. For the next arduinos in 
the chain the pattren is repeated: Serial1 to send to the next arduino, 
Serial2 to receive from the previous arduino. USB is operational for all arduinos 
in the chain but it is recommended to only inject messages at the beginning of 
the chain...    

Pins 38 to 53 are reserved for valves. Pins 2 to 12 are reserved for PWM,
with pin 7 reserved for 1 servo per arduino. 

NOTE: arduino pins are _not_ the same than the PWM and Valve indexes!

## Protocol:

The ControlBox protocol is very simple and human-writable. 
The commands are received by the first arduino in the chain 
and if needed are forwarded recursively to the next arduinos.

### Valve and PWM channels:

Each Arduino has 15 relay/valve channels, the 16th channel is 
used for the buzzer, and 10 PWM channels, of which channel 5 is 
reserved for servos. Valve channel of index 15 is therefore the 1st
(index=0) valve channel of the second arduino. Each Arduino added
inceases the number of available valve and PWM channels. The 
indexing starts at the first arduino and is incremented to span
across all Arduinos ths offering a unified indexing.    

### Command structure:

Commands always start with the character: '#' and end with '\n'.
A successfully parsed command causes a return message of 'done!\n'.
Integer numbers must be surrounded by some whitespace for delimitation 
(quite flexible in the type and number of whitespaces).

### Command list:

    .
    '#?\n'
    Returns the current state of the ControlBox. 
    For example,for two arduinos chained, the result is:
    
    |c|o|c|c|c|c|c|c|c|c|c|c|c|c|c||0|0|0|0|1|0|0|0|0|0|done!
    |o|c|c|c|c|c|c|c|c|c|c|c|c|c|c||0|0|0|0|0|0|0|0|0|0|done!
    
    Where we can see that (second) valve 1 of the first arduino (first line)
     is open, and the (first) valve 0 of the second arduino (second line) is
     open. Also, the 5th PWM channel (index=4) of the first arduino is set at 
     a non zero value (for now we cannot know the exact value, only if it is 'on'). 
     
    '#!\n' 
    Shutsdown all valves and all PWMs and brings back all servos to position 
    (angle) 0. This is called recursively on all arduinos in the chain.
    
    '#dX\n' 
    Turns on or off debugging messages: 'd0' -->  off, 'd1' --> on.
    
    '#b P D \n' 
    Makes noise using the unnused relay (index=15).
    P is the periode in milliseconds, D is the duration in number of periods.
    
    '#tT R I \n'
    Runs a test. There is two kinds of tests: 'v'alve and 'p'wm.
    Therefore T is either 'v' or 'p'. R is an integer that indicates 
    how many times to repreat the test sequence.
    I is optional and only needed for the 'p' test, it indicates which PWM channel 
    to use for the PWM test sequence.
     
    '#vS I \n' 
    Opens (S='o') or closes (S='c') valve at index I. 
    
    '#p I S \n' 
    Sets the PWM value (or servo angle) of PWM channel I to value S.
    S is an integer in the interval [0, 255], except for channel 5 (modulo 10)
    fro which the value S must be in the interval [0, 180] (angles).
     
    Unrecognised commands are ignored (in debug mode a notification is sent.).
    
     
    
       





