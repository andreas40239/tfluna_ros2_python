# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

class MinimalPublisher(Node):
    interface_luna = serial.Serial('/dev/ttyUSB0',115200)

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'LiDAR/TfLuna', 10)
        timer_period = 0.5  # seconds
        luna_enableOutput  = [0x5a,0x05,0x07,0x01,0x00]

        if self.interface_luna.isOpen() :
            self.get_logger().info("TF-Luna sucessfully opened")
            self.interface_luna.write(luna_enableOutput)
            time.sleep(0.5)
            self.timer = self.create_timer(timer_period, self.timer_callback)
            self.i = 0

        else :
            self.get_logger().info("could not open TF-Luna, won't publish anything.")


    def timer_callback(self):
        counter = self.interface_luna.in_waiting
        bytes_to_read = 9
        if counter > bytes_to_read-1:
            bytes_serial = self.interface_luna.read(bytes_to_read) 
            self.interface_luna.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8) - 256 # temp scaling and offset

                msg = String()
                msg.data = 'Distance: %d cm' % distance
                #   f"Strength: {strength:2.0f} / 65535 (16-bit), "
                #   f"Chip Temperature: {temperature:2.1f} C")
                self.publisher_.publish(msg)
                self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
