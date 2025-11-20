import random
import socket
import time

from config import HOST
from config import PORT
from student import ITstudent
from utils import logger


def start_client():
    for i in range(1, 11):
        student = ITstudent.generate_random(i)
        xml_data = student.get_xml_string()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(xml_data.encode("utf-8"))
                s.recv(1024)
        except ConnectionRefusedError:
            logger.error("Error: Could not connect to server. Is server.py running?")
            break

        time.sleep(random.uniform(1.0, 3.0))


if __name__ == "__main__":
    start_client()
