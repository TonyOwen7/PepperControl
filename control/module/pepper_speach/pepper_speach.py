import rospy
from std_msgs.msg import String
import subprocess

def pepper_speak(text):
    """
    Publishes a speech message to Pepper using the rostopic pub command.

    Args:
        text (str): The text that Pepper will say.
    """
    # Escape single quotes in the text to prevent command injection
    escaped_text = text.replace("'", "\\'")

    # Construct the rostopic pub command
    command = f"rostopic pub -1 /speech std_msgs/String \"data: '{escaped_text}'\""

    try:
        # Execute the command
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Capture standard output and errors
        stdout, stderr = process.communicate()

        # Check the return code to determine success or failure
        if process.returncode == 0:
            print(f"Successfully published: '{text}'")
        else:
            print(f"Error publishing message: {stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Exception occurred: {e}")




