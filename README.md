# serial_handler
Library that simplifies serial communication in Python when making a simple application. This is done by creating a thread that handles a communication. Buffers are filled when data is to be sent and when data is received.

## Examples
### List Available Ports
```python
ports = SerialHandler.getAvailablePorts()
print(ports)
```
### Generic
```python
ser = SerialHandler(port=<port_to_use>, baudrate=<baudrate_to_use>)
ser.start() # Starts the thread that handles serial data
ser.sendData(<data_to_send>)

if ser.isAvailable(): # If data has been received
  dataReceived = ser.receiveData()
  print(dataReceived)
```
