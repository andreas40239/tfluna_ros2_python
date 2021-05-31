from setuptools import setup

package_name = 'pub_lidar_tfluna'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Andreas W',
    maintainer_email='aw40239@gmail.com',
    description='Publishes distance measurements from a connected Benewake TF-Luna LiDAR (in centimeters, up to 8 meters)',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'talker = pub_lidar_tfluna.publisher_function:main',
                'listener = pub_lidar_tfluna.subscriber_function:main'
        ],
    }
)