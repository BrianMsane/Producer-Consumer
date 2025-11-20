import os
import socket

from config import HOST
from config import PORT
from student import ITstudent
from utils import logger


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info("Server started, listening on %s: %d \n", HOST, PORT)

        while True:
            conn, addr = s.accept()
            with conn:
                logger.info(f"Connected by {addr}")

                data = conn.recv(4096)
                if not data:
                    break

                temp_filename = "received_student.xml"
                with open(temp_filename, "wb") as f:
                    f.write(data)

                # Unwrap and process student info from XML
                student = ITstudent.process_xml_file(temp_filename)
                os.remove(temp_filename)

                if student:
                    logger.info(
                        "Consumer Processed Student: %s (%d) - Average: %.2f%% - Status: %s",
                        student.name,
                        student.student_id,
                        student.compute_average(),
                        student.get_pass_status(),
                    )
                    conn.sendall(b"Processed successfully")


if __name__ == "__main__":
    start_server()
