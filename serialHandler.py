import sys
import serial
import glob
import time
from threading import Thread, Lock

class SerialHandler():

    def __init__( 
        self, \
        port=None, \
        baudrate=115200, \
        bytesize=serial.EIGHTBITS, \
        parity=serial.PARITY_NONE, \
        timeout=None, \
        stopbits=serial.STOPBITS_ONE, \
        xonxoff=False, \
        rtscts=False, \
        write_timeout=None, \
        dsrdtr=False, \
        inter_byte_timeout=None, \
        exclusive=None \
    ):
        """
            This init function acts as a wrapper for pyserial. 
            All arguments are the exact same as in pyserial 
            making this a drop-in replacement.
        """
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.timeout = timeout
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.write_timeout = write_timeout
        self.dsrdtr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        self.exclusive = exclusive
        
        if port != None:
            self.__setSer()

        self.serThread = Thread(target=self.__run)
        self.mutex = Lock()
        self.txbuf = None
        self.rxbuf = None
        self.serPort = None
        self.ser = None
        self.stopFlag = False

    # PRIVATE METHODS

    def __setSer(self):
        """
            Sets the serial object.
        """
        self.ser = serial.Serial( \
            port=self.port, \
            baudrate=self.baudrate, \
            bytesize=self.bytesize, \
            parity=self.parity, \
            timeout=self.timeout, \
            stopbits=self.stopbits, \
            xonxoff=self.xonxoff, \
            rtscts=self.rtscts, \
            write_timeout=self.write_timeout, \
            dsrdtr=self.dsrdtr, \
            inter_byte_timeout=self.inter_byte_timeout, \
            exclusive=self.exclusive
        )

    def __run(self):
        """
            Function that runs in thread. Will send any data in 
            txbuf, sleep, then place any data received into the 
            rxbuf and sleep again.
        """
        cStopFlag = False
        while not cStopFlag:
            if self.ser != None:
                self.__sendDataTask()
                time.sleep(0.1)
                self.__receiveDataTask()
                time.sleep(0.1)

            if self.mutex.acquire():
                cStopFlag = self.stopFlag
                self.mutex.release()

    def __receiveDataTask(self):
        """
            Reads data into rxbuf
        """
        if self.mutex.acquire():
            self.ser.timeout = 100
            bytesToRead = self.ser.inWaiting()
            if bytesToRead == 0: 
                self.mutex.release()
                return

            if self.rxbuf == None:
                self.rxbuf = self.ser.read(1)
            else:
                self.rxbuf = self.ser.read(1)

            self.mutex.release()

    def __sendDataTask(self):
        """
            Sends all the data in txbuf
        """
        if self.mutex.acquire():
            if self.txbuf == None:
                self.mutex.release()
                return

            self.ser.write(bytes(self.txbuf, 'ascii'))
            self.txbuf = None
            self.mutex.release()

    # PUBLIC METHODS

    def start(self):
        if self.mutex.acquire():
            self.stopFlag = False
            self.mutex.release()
            self.serThread.start()
        
    
    def stop(self):
        if self.mutex.acquire():
            self.stopFlag = True
            self.mutex.release()
            self.serThread.join()
        
    def setPort(self, port):
        if self.mutex.acquire():
            if self.ser != None:
                if self.ser.isOpen():
                    self.ser.close()
            
            self.port = port
            self.ser = self.__setSer()
            self.mutex.release()

    def isAvailable(self):
        """
            Used to help determine if there is data in the buffer
        """
        hasData = True
        
        if self.mutex.acquire():
            if self.rxbuf == None:
                hasData = False
            self.mutex.release()
        
        return hasData


    def sendData(self, data):
        """
            Fills up the txbuf
        """
        if self.mutex.acquire():
            if self.txbuf == None:
                self.txbuf = data
            else:
                self.txbuf += data
            self.mutex.release()

    def receiveData(self):
        """
            Makes copy of rxbuf and then empties it and returns the copy
        """
        cData = ''
        if self.mutex.acquire():
            cData = self.rxbuf
            self.rxbuf = None
            self.mutex.release()
        return cData

    def get_serial_ports():
        """ 
            Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['com%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

if __name__ == "__main__":
    port = SerialHandler.get_serial_ports()
    print(port)

    ser = SerialHandler()
