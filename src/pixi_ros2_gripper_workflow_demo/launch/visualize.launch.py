import os
import tempfile
from ament_index_python.packages import get_package_share_directory
from launch.actions import LogInfo
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    package_share = get_package_share_directory('pixi_ros2_gripper_workflow_demo')
    urdf_file = os.path.join(package_share, 'urdf', 'gripper.urdf')
    rviz_template_file = os.path.join(package_share, 'rviz', 'gripper.rviz')
    rviz_generated_file = os.path.join(
        tempfile.gettempdir(),
        'pixi_ros2_gripper_workflow_demo_runtime.rviz',
    )

    with open(urdf_file, 'r', encoding='utf-8') as infp:
        robot_desc = infp.read()
    with open(rviz_template_file, 'r', encoding='utf-8') as infp:
        rviz_config = infp.read().replace('__URDF_FILE__', urdf_file)
    with open(rviz_generated_file, 'w', encoding='utf-8') as outfp:
        outfp.write(rviz_config)

    return LaunchDescription([
        LogInfo(msg=f'Using URDF: {urdf_file}'),
        LogInfo(msg=f'Using RViz template: {rviz_template_file}'),
        LogInfo(msg=f'Using RViz config: {rviz_generated_file}'),
        Node(
            package='pixi_ros2_gripper_workflow_demo',
            executable='joint_state_relay',
            name='joint_state_relay',
            output='screen',
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_desc,
                'ignore_timestamp': True,
            }]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_generated_file, '-f', 'base_link'],
        )
    ])
