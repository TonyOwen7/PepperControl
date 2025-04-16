import subprocess
import signal
import os
import time
import threading

class RobotProcessManager:
    def __init__(self):
        self.naoqi_process = None
        self.pepper_process = None
        self.current_robot_ip = None
        self.current_network_interface = None
        self.monitor_thread = None
        self.monitor_running = False

    def start(self, nao_ip, network_interface):
        """Start both naoqi_driver and pepper_dcm_bringup at the same time."""
        self.stop()  # Stop any existing processes

        # Store current connection details
        self.current_robot_ip = nao_ip
        self.current_network_interface = network_interface

       
        # Start pepper_dcm_bringup
        self.start_pepper_dcm_bringup()

        # Start naoqi_driver
        self.start_naoqi_driver()

        # Start the monitoring thread
        self.monitor_running = True
        self.monitor_thread = threading.Thread(target=self.monitor_processes)
        self.monitor_thread.start()

    def start_naoqi_driver(self):
        """Start the naoqi_driver process."""
        try:
            naoqi_driver_command = [
                "roslaunch", "naoqi_driver", "naoqi_driver.launch", 
                f"nao_ip:={self.current_robot_ip}", 
                "roscore_ip:=localhost", 
                f"network_interface:={self.current_network_interface}"
            ]

            self.naoqi_process = subprocess.Popen(
                naoqi_driver_command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Allows killing entire process group
            )
            print(f"Naoqi driver started for robot {self.current_robot_ip}")
        except Exception as e:
            print(f"Error starting naoqi driver: {e}")

    def start_pepper_dcm_bringup(self):
        """Start the pepper_dcm_bringup process."""
        try:
            pepper_dcm_command = [
                "roslaunch", "pepper_dcm_bringup", "pepper_bringup.launch", 
                f"robot_ip:={self.current_robot_ip}", 
                "roscore_ip:=localhost", 
                f"network_interface:={self.current_network_interface}"
            ]

            self.pepper_process = subprocess.Popen(
                pepper_dcm_command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Allows killing entire process group
            )
            print(f"Pepper DCM bringup started for robot {self.current_robot_ip}")
        except Exception as e:
            print(f"Error starting pepper_dcm_bringup: {e}")

    def stop_naoqi_driver(self):
        """Stop the naoqi_driver process."""
        if self.naoqi_process:
            try:
                os.killpg(os.getpgid(self.naoqi_process.pid), signal.SIGINT)
                self.naoqi_process = None
                print("Naoqi driver stopped successfully")
            except Exception as e:
                print(f"Error stopping naoqi driver: {e}")

    def stop_pepper_dcm_bringup(self):
        """Stop the pepper_dcm_bringup process."""
        if self.pepper_process:
            try:
                os.killpg(os.getpgid(self.pepper_process.pid), signal.SIGINT)
                self.pepper_process = None
                print("Pepper DCM bringup stopped successfully")
            except Exception as e:
                print(f"Error stopping pepper_dcm_bringup: {e}")

    def stop(self):
        """Stop both naoqi_driver and pepper_dcm_bringup."""
        self.monitor_running = False  # Stop the monitoring thread
        if self.monitor_thread:
            self.monitor_thread.join()  # Wait for the monitoring thread to finish

        self.stop_naoqi_driver()
        self.stop_pepper_dcm_bringup()
        print("All processes stopped.")

    def monitor_processes(self):
        """Monitor the processes and restart them if they stop unexpectedly."""
        while self.monitor_running:
            # Check naoqi_driver
            if self.naoqi_process and self.naoqi_process.poll() is not None:
                print("Naoqi driver has stopped. Restarting...")
                self.start_naoqi_driver()

            # Check pepper_dcm_bringup
            if self.pepper_process and self.pepper_process.poll() is not None:
                print("Pepper DCM bringup has stopped. Restarting...")
                self.start_pepper_dcm_bringup()

            # Sleep for a while before checking again
