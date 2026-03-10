from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'pixi_ros2_gripper_workflow_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hex',
    maintainer_email='xingxin.he@connect.ust.hk',
    description='ROS 2 workflow demo showing Pixi + RoboStack for gripper command and RViz visualization.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ui_node = pixi_ros2_gripper_workflow_demo.ui_node:main',
            'joint_state_relay = pixi_ros2_gripper_workflow_demo.joint_state_relay:main',
        ],
    },
)
