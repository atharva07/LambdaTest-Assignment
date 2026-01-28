import logging
import os

class Log_maker:
    @staticmethod
    def log_gen(testcase_id):
        # Define the log directory
        log_dir = "D://LambdaTestAssignment//amazonAssignment//logs"

        # Create a folder for the test case
        test_case_dir = os.path.join(log_dir, testcase_id)
        if not os.path.exists(test_case_dir):
            os.makedirs(test_case_dir)

        # Create a unique log file name based on the test case name
        log_file = os.path.join(test_case_dir, f"{testcase_id}.log")

        # Create a logger
        logger = logging.getLogger(testcase_id)
        logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(logging.INFO)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger