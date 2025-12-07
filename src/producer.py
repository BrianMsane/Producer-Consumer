import socket
import time
from config import HOST, PORT
from utils import logger
from student import ITstudent


def run_producer():
    """Produces 10 students and sends IDs to buffer via socket."""
    for i in range(1, 11):
        student = ITstudent.generate_random(i)
        student.to_xml()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                msg = f"PRODUCE {i}"
                s.sendall(msg.encode())
                
                data = s.recv(1024)
                logger.info(f"Server says: {data.decode()}")
                
            except ConnectionRefusedError:
                logger.error("Connection failed. Is server.py running?")
                break
        
        time.sleep(1)

if __name__ == "__main__":
    print("Starting Producer...")
    run_producer()
    print("Producer finished.")