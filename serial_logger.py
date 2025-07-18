# serial_logger.py

import serial

class SerialLogger:
    """
    A class to manage serial port communication for logging alerts.
    """
    def __init__(self, port, baudrate):
        """
        Initializes the SerialLogger, attempting to open the serial port.

        Args:
            port (str): The serial port name (e.g., 'COM1' or '/dev/ttyUSB0').
            baudrate (int): The baud rate for serial communication.
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self._is_active = False # Flag to indicate if serial port is successfully open

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self._is_active = True
            print(f"SerialLogger: Successfully opened serial port {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"SerialLogger Error: Could not open serial port {self.port}: {e}")
            print("Serial output will be disabled.")
        except Exception as e:
            print(f"SerialLogger Unexpected Error: {e}")
            print("Serial output will be disabled.")

    def log_alert(self, message):
        """
        Sends an alert message to the serial port if it's active.

        Args:
            message (str): The string message to send. A newline character will be added.
        """
        if self._is_active and self.ser:
            try:
                # Ensure message ends with a newline and encode to bytes
                if not message.endswith('\n'):
                    message += '\n'
                self.ser.write(message.encode('utf-8'))
                # print(f"SerialLogger: Sent: {message.strip()}") # Uncomment for debug
            except serial.SerialException as e:
                print(f"SerialLogger Error: Failed to write to serial port: {e}")
                print("Serial output disabled for remaining session.")
                self.close() # Attempt to close on write error
            except Exception as e:
                print(f"SerialLogger Unexpected Error during write: {e}")
                print("Serial output disabled for remaining session.")
                self.close()

    def close(self):
        """
        Closes the serial port if it's open.
        """
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
                self._is_active = False
                print(f"SerialLogger: Serial port {self.port} closed.")
            except serial.SerialException as e:
                print(f"SerialLogger Error: Failed to close serial port: {e}")
            except Exception as e:
                print(f"SerialLogger Unexpected Error during close: {e}")

    def is_active(self):
        """
        Checks if the serial logger is currently active (port is open).
        """
        return self._is_active

