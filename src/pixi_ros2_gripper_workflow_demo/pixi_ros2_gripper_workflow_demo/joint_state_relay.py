import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time
import os


class JointStateRelay(Node):
    INPUT_TOPIC = '/joint_states_cmd'
    OUTPUT_TOPIC = '/joint_states'
    JOINT_NAMES = ['left_finger_joint', 'right_finger_joint']

    def __init__(self):
        super().__init__('joint_state_relay')
        self._positions = [0.0, 0.0]
        self._last_logged_positions = [0.0, 0.0]
        self._publisher = self.create_publisher(JointState, self.OUTPUT_TOPIC, 10)
        self._subscriber = self.create_subscription(
            JointState,
            self.INPUT_TOPIC,
            self._on_joint_state_cmd,
            10,
        )
        self._timer = self.create_timer(0.1, self._publish_joint_state)
        self.get_logger().info(
            f"Relaying {self.INPUT_TOPIC} -> {self.OUTPUT_TOPIC} with default zero state."
        )
        self.get_logger().info(
            "ROS env: "
            f"ROS_DOMAIN_ID={os.environ.get('ROS_DOMAIN_ID', '<unset>')}, "
            f"ROS_LOCALHOST_ONLY={os.environ.get('ROS_LOCALHOST_ONLY', '<unset>')}, "
            f"RMW_IMPLEMENTATION={os.environ.get('RMW_IMPLEMENTATION', '<unset>')}"
        )

    def _on_joint_state_cmd(self, msg: JointState):
        name_to_index = {name: idx for idx, name in enumerate(msg.name)}
        for local_idx, joint_name in enumerate(self.JOINT_NAMES):
            if joint_name in name_to_index:
                source_idx = name_to_index[joint_name]
                if source_idx < len(msg.position):
                    self._positions[local_idx] = msg.position[source_idx]

        if any(abs(a - b) > 1e-5 for a, b in zip(self._positions, self._last_logged_positions)):
            self._last_logged_positions = list(self._positions)
            self.get_logger().info(
                f"Received cmd: left={self._positions[0]:.4f}, right={self._positions[1]:.4f}"
            )

    def _publish_joint_state(self):
        msg = JointState()
        now_ns = time.time_ns()
        msg.header.stamp.sec = now_ns // 1_000_000_000
        msg.header.stamp.nanosec = now_ns % 1_000_000_000
        msg.name = list(self.JOINT_NAMES)
        msg.position = list(self._positions)
        self._publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = JointStateRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
