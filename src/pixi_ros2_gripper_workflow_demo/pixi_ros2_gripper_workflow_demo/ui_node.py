import threading
import time
import os

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rich.console import Console
from rich.table import Table
from rich.prompt import FloatPrompt


class GripperUI(Node):
    TOPIC_NAME = '/joint_states_cmd'
    MIN_WIDTH = 0.0
    MAX_WIDTH = 0.08
    PUBLISH_HZ = 10.0

    def __init__(self):
        super().__init__('gripper_ui_node')
        self.publisher_ = self.create_publisher(JointState, self.TOPIC_NAME, 10)
        self.console = Console()
        self.current_width = 0.0
        self._stop_event = threading.Event()
        self._width_lock = threading.Lock()
        self._publisher_thread = threading.Thread(target=self._publisher_loop, daemon=True)

    def render_ui(self, old_width, target_width):
        self.console.clear()
        table = Table(title="[bold cyan]Pixi ROS 2 Gripper Workflow Demo[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Parameter", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Current Width", f"{old_width:.4f} m")
        table.add_row("Target Width", f"{target_width:.4f} m")
        self.console.print(table)

    def _build_joint_state_msg(self, width):
        msg = JointState()
        now_ns = time.time_ns()
        msg.header.stamp.sec = now_ns // 1_000_000_000
        msg.header.stamp.nanosec = now_ns % 1_000_000_000
        msg.name = ['left_finger_joint', 'right_finger_joint']
        msg.position = [width / 2.0, width / 2.0]
        return msg

    def _publisher_loop(self):
        period = 1.0 / self.PUBLISH_HZ
        while rclpy.ok() and not self._stop_event.is_set():
            with self._width_lock:
                width = self.current_width
            self.publisher_.publish(self._build_joint_state_msg(width))
            time.sleep(period)

    def run(self):
        self.console.clear()
        self.console.print("[bold green]Starting Pixi ROS 2 Gripper Workflow Demo CLI...[/bold green]")
        self.console.print(
            "[dim]ROS_DOMAIN_ID="
            f"{os.environ.get('ROS_DOMAIN_ID', '<unset>')}, "
            "ROS_LOCALHOST_ONLY="
            f"{os.environ.get('ROS_LOCALHOST_ONLY', '<unset>')}, "
            "RMW_IMPLEMENTATION="
            f"{os.environ.get('RMW_IMPLEMENTATION', '<unset>')}[/dim]"
        )
        self.console.print(f"[dim]Streaming {self.TOPIC_NAME} at {self.PUBLISH_HZ:.0f} Hz[/dim]")
        self._publisher_thread.start()

        while rclpy.ok():
            try:
                target = FloatPrompt.ask("\n[bold yellow]Enter target gripper width (0.0 to 0.08)[/bold yellow]")
                target = max(self.MIN_WIDTH, min(self.MAX_WIDTH, target))

                with self._width_lock:
                    previous = self.current_width
                    self.current_width = target

                self.render_ui(previous, target)
                self.console.print(f"[dim]Updated target, publishing on {self.TOPIC_NAME}[/dim]")
            except KeyboardInterrupt:
                self.console.print("\n[bold red]Exiting...[/bold red]")
                break

        self._stop_event.set()
        if self._publisher_thread.is_alive():
            self._publisher_thread.join(timeout=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = GripperUI()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
