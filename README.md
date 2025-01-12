# ROS 2 Workspace Setup for My Robot

## 1. Create the workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

## 2. Create the `interfaces` package
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake my_robot_interfaces
```

### Add message and service definitions
```bash
mkdir -p my_robot_interfaces/msg my_robot_interfaces/srv
echo "string status" > my_robot_interfaces/msg/Status.msg
echo -e "string mode\n---\nbool success" > my_robot_interfaces/srv/SetMode.srv
```

### Update CMakeLists.txt
```txt
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Status.msg"
  "srv/SetMode.srv"
)
```

### Update package.xml
```bash
echo '
```
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
```

## 3. Create the `description` package
```bash
ros2 pkg create --build-type ament_cmake my_robot_description
```

### Add a sample URDF file
```bash
mkdir -p my_robot_description/urdf
echo '
```
```urdf
<robot name="my_robot">
  <link name="base_link"/>
  <joint name="base_to_link1" type="fixed">
    <parent link="base_link"/>
    <child link="link1"/>
  </joint>
</robot>
```

### Run Robot State Publisher Node
```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro ~/ros2_ws/src/my_robot_description/urdf/my_robot.urdf.xacro)"
```
### Visualization of URDF using rviz
```bash
/usr/bin/env QT_AUTO_SCREEN_SCALE_FACTOR=0 QT_SCREEN_SCALE_FACTORS=[1.0,1.0] ros2 launch urdf_tutorial display.launch.py model:=/home/srikanth/ros2_ws/src/my_robot_description/urdf/my_robot.urdf.xacro
```
### Launch Gazebo and spawn robot
```bash
ros2 launch gazebo_ros gazebo.launch.py
ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity my_robot
```

### Update CMakeLists.txt
```bash
echo '
```
```txt
install(DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf)
```


## 4. Create the `controller` package
```bash
ros2 pkg create --build-type ament_python my_robot_controller --dependencies rclpy
```

### Add a Python controller node
``` bash
mkdir -p my_robot_controller/my_robot_controller
echo 
```

``` python
import rclpy
from rclpy.node import Node

class ControllerNode(Node):
    def __init__(self):
        super().__init__("controller_node")
        self.get_logger().info("Controller Node started.")

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

### Update setup.py
```bash
echo '
```
``` py
from setuptools import setup

package_name = "my_robot_controller"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="your_name",
    maintainer_email="your_email@example.com",
    description="Controller package for my robot",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "controller_node = my_robot_controller.controller_node:main",
        ],
    },
)
```

## 5. Create the `bringup` package
```bash 
ros2 pkg create my_robot_bringup 
```

### Add a launch file
```bash
mkdir -p my_robot_bringup/launch
echo '
```
```py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="my_robot_controller",
            executable="controller_node",
            name="controller_node"
        ),
    ])
```

### Update setup.py
```bash
echo '
```

```py
from setuptools import setup

package_name = "my_robot_bringup"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="your_name",
    maintainer_email="your_email@example.com",
    description="Bringup package for my robot",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
```
## 6. Build the workspace
```bash
cd ~/ros2_ws
colcon build
```

## 7. Source the workspace
```bash
source install/setup.bash
```
## 8. Test the setup
```bash
ros2 launch my_robot_bringup bringup_launch.py
```
### For gazebo glitching
```bash
/usr/bin/env QT_AUTO_SCREEN_SCALE_FACTOR=0 QT_SCREEN_SCALE_FACTORS=[1.0,1.0] /usr/bin/gazebo
```

