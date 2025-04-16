import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def indicate_forward_with_arm():
    rospy.init_node("pepper_arm_gesture", anonymous=True, disable_signals=True)

    pub = rospy.Publisher('/pepper_dcm/JointTrajectory', JointTrajectory, queue_size=10)
    
    # Wait for the publisher to be ready
    rospy.sleep(1)

    # Define the joints of the right arm
    joint_names = [
        "RShoulderPitch",
        "RShoulderRoll",
        "RElbowYaw",
        "RElbowRoll",
        "RWristYaw"
    ]

    # Values to stretch the right arm forward
    # Values are in radians (approximately)
    point_forward_position = [
        0.0,      # RShoulderPitch: straight forward
        -0.3,     # RShoulderRoll: slightly outward
        1.5,      # RElbowYaw: align forearm
        0.5,      # RElbowRoll: extend elbow
        0.0       # RWristYaw: neutral
    ]

    trajectory_msg = JointTrajectory()
    trajectory_msg.joint_names = joint_names

    point = JointTrajectoryPoint()
    point.positions = point_forward_position
    point.time_from_start = rospy.Duration(2.0)  # move over 2 seconds

    trajectory_msg.points.append(point)

    pub.publish(trajectory_msg)
    rospy.loginfo("Sent gesture to point forward with right arm")

indicate_forward_with_arm()
