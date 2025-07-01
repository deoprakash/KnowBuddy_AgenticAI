import os
log_file = "logs/processed_linls.txt"
os.makedirs("logs", exist_ok = True)

def was_processed(url):
    if not os.path.exists(log_file):
        return False
    with open(log_file, 'r') as f:
        return url.strip() in f.read()
    

def mark_as_processed(url):
    with open(log_file, 'a') as f:
        f.write(url.strip() + '\n')