# This file contains the commands to start both APIs
# It will be used by the render.yaml configuration

import subprocess
import os
import sys

def start_apis():
    # Get port from environment variable or use default
    port1 = os.getenv('PORT', '8000')
    port2 = int(port1) + 1  # Use next port for second service
    
    # Command for Inventory Forecast API
    cmd1 = f"gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{port1}"
    
    # Command for Tariff Impact API
    cmd2 = f"gunicorn main2:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{port2}"
    
    try:
        # Start both processes
        process1 = subprocess.Popen(cmd1.split())
        process2 = subprocess.Popen(cmd2.split())
        
        # Wait for both processes
        process1.wait()
        process2.wait()
        
    except KeyboardInterrupt:
        print("Shutting down servers...")
        process1.terminate()
        process2.terminate()
        sys.exit(0)

if __name__ == "__main__":
    start_apis()