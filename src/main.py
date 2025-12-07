import threading
import time
from server import start_server
from producer import run_producer
from consumer import run_consumer
from utils import logger


def main():
    try:

        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        logger.info("Server thread started...")
        time.sleep(1)

        consumer_thread = threading.Thread(target=run_consumer)
        consumer_thread.start()
        logger.info("Consumer thread started...")


        producer_thread = threading.Thread(target=run_producer)
        producer_thread.start()
        logger.info("Producer thread started...")


        producer_thread.join()
        consumer_thread.join()

        logger.info("All tasks completed successfully.")

    except KeyboardInterrupt:
        logger.warning("Program interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
