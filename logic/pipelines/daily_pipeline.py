import os
from utils.mail_module.email_module_functions import send_scan_recap_email

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "daily_pipeline.log.txt")



