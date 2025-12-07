import socket
import time
from config import HOST, PORT
from utils import logger
from student import ITstudent

def run_consumer():
    """Continuously consumes IDs from buffer and processes XML."""

    consumed_count = 0
    while consumed_count < 10:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                s.sendall(b"CONSUME")
                
                data = s.recv(1024).decode()
                
                if data:
                    file_id = int(data)
                    logger.info(f"Received ID from buffer: {file_id}")
                    
                    student = ITstudent.from_xml_file(file_id)
                    
                    if student:
                        student.print_report()
                        consumed_count += 1
                else:
                    logger.warning("Empty response from server.")

            except ConnectionRefusedError:
                logger.error("Connection failed. Is server.py running?")
                break
            except ValueError: # when server sends a non-negative number
                pass
        
        time.sleep(1.5)

if __name__ == "__main__":
    print("Starting Consumer...")
    run_consumer()
    print("Consumer finished.")