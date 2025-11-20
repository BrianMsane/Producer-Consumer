import threading
import time

from client import start_client
from server import start_server
from utils import logger


def main():
    try:
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

        logger.info("Server thread started...")
        time.sleep(1)

        logger.info("Starting Client...")
        start_client()

    except KeyboardInterrupt:
        logger.debug("Program interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
