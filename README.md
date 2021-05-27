# serial_handler

Library that simplifies serial communication in Python while developing simple applications. This is done by creating a thread that handles the serial communication. Buffers are filled when data is ready to be sent or recieved.

## Supported OSs

-   Windows
-   Linux (should work, but untested)
-   Mac (should work, but untested)

## Dependancies

-   pyserial
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
