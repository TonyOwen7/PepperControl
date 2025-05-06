import rospy
from std_msgs.msg import String
import subprocess
import yaml

def pepper_speak2(text):
    """
    Publishes a speech message to Pepper using the rostopic pub command.
    Args:
        text (str): The text that Pepper will say.
    """
    # Create the message dictionary
    message = {'data': text}
    
    # Dump it into valid YAML
    yaml_text = yaml.dump(message, default_style='"', allow_unicode=True)
    
    # Construct the rostopic pub command - fixing the quoting issue
    command = ['rostopic', 'pub', '-1', '/speech', 'std_msgs/String', yaml_text.strip()]
    
    try:
        # Execute the command as a list of arguments instead of a shell string
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"Successfully published: '{text}'")
        else:
            print(f"Error publishing message: {stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Exception occurred: {e}")


def pepper_speak(text):
    """
    Alternative version using shell=True but with proper escaping
    """
    # Create the message dictionary
    message = {'data': text}
    
    # Dump it into valid YAML
    yaml_text = yaml.dump(message, default_style='"', allow_unicode=True)
    
    # Escape quotes properly for shell command
    yaml_escaped = yaml_text.strip().replace('"', '\\"')
    command = f'rostopic pub -1 /speech std_msgs/String "{yaml_escaped}"'
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"Successfully published: '{text}'")
        else:
            print(f"Error publishing message: {stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Exception occurred: {e}")


# Example usage with clean test preparation advice
study_advice = "Study a few days before the test. Don't cram for a test. As soon as the date is announced, start preparing. Look over your notes and textbook to review the material each day for a few days before the test. This way, you avoid anxiety the night before the test by trying to learn everything in a few hours. Write down all the formulas you need at the start of the test. Most math tests involve remembering numerous formulas to solve different problems. Even if you studied and know them well, you could forget some if you get nervous during the test. Prevent this by doing a brain dump and writing down all the necessary formulas at the beginning of the test. Then refer back to this list if you forget any formulas. Pay attention during class. The work of preparing for a test begins long before the actual test. If you're attentive during class, you'll know the material much better for test day. Always get to class on time, take out your pen and notebook, and be ready to work."

# Uncomment to use:
pepper_speak(study_advice)