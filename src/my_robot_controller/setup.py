from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='srikanth',
    maintainer_email='srikanth@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "draw_circle = my_robot_controller.draw_circle:main",
            "publisher_node = my_robot_controller.publisher_node:main",
            "subscriber_node = my_robot_controller.subscriber_node:main",
            "add_two_ints_server = my_robot_controller.add_two_ints_server:main",
            "add_two_ints_client = my_robot_controller.add_two_ints_client:main",
            "number_publisher = my_robot_controller.number_publisher:main",
            "number_counter = my_robot_controller.number_counter:main"
        ],
    },
)
