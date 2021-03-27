# serial_handler
Library that simplifies serial communication in Python when making a simple application. This is done by creating a thread that handles a communication. Buffers are filled when data is to be sent and when data is received.

## Supported OSs
* Windows
* Linux (untested)
* Mac (untested)

## Dependancies
* pyserial
  > `pip install pyserial`

## Examples

When SerialHandler is run as main, it will act as a crude serial console. 

### List Available Ports
```python
ports = SerialHandler.getAvailablePorts()
print(ports)
```
### General Send/Receive
```python
ser = SerialHandler(port=<port_to_use>, baudrate=<baudrate_to_use>)
ser.start() # Starts the thread that handles serial data
ser.sendData(<data_to_send>)

if ser.isAvailable(): # If data has been received
  dataReceived = ser.receiveData()
  print(dataReceived)
```
### Arduino Test Code
This is can be used to test the library to ensure that the correct data is being sent and received on an arduino
```cpp

void setup() {
  Serial.begin(115200);
}

void loop() {
  if(Serial.available()) {
    char temp = '\0';
    String rxData = "";
    while(Serial.available()) {
      temp = Serial.read();
      rxData += String(temp);
    }
    Serial.print(rxData);
  }
}
```
