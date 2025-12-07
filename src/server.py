import socket
import threading
import queue
from config import HOST, PORT
from utils import logger


buffer_queue = queue.Queue(maxsize=10) 


mutex = threading.Semaphore(1)
empty_slots = threading.Semaphore(10)
filled_slots = threading.Semaphore(0)


def handle_client(conn, addr):
    """Threaded handler for Producer/Consumer connections."""
    try:
        message = conn.recv(1024).decode().strip()
        
        if message.startswith("PRODUCE"):
            _, file_id = message.split()
            file_id = int(file_id)
            
            logger.info(f"Producer trying to add student{file_id}.xml...")
            
            empty_slots.acquire() 
            mutex.acquire()
            
            try:
                buffer_queue.put(file_id) # 
                response = f"ACK {file_id} added to buffer."
                logger.info(f"Buffer Update: Added ID {file_id}. Size: {buffer_queue.qsize()}/10")
            finally:
                mutex.release()
                filled_slots.release()
            
            conn.sendall(response.encode())

        elif message == "CONSUME":
            # CONSUMER LOGIC
            logger.info("Consumer requesting data...")
            
            filled_slots.acquire()
            mutex.acquire()
            
            file_id = None
            try:
                file_id = buffer_queue.get() # 
                response = str(file_id)
                logger.info(f"Buffer Update: Removed ID {file_id}. Size: {buffer_queue.qsize()}/10")
            finally:
                mutex.release()
                empty_slots.release()
            
            conn.sendall(response.encode())

    except Exception as e:
        logger.error(f"Error handling client: {e}")
    finally:
        conn.close()


def start_server():
    """Starts the socket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Server (Buffer) listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()


if __name__ == "__main__":
    start_server()