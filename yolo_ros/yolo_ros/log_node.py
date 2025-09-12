# Copyright (C) 2023 Miguel Ángel González Santamarta

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from yolo_msgs.msg import DetectionArray


class LogNode(Node):
    """
    Node that logs detections and publishes first-seen classes.

    - Subscribes: `/yolo/detections` (DetectionArray)
    - Publishes: `/yolo/classes` (String) when a new class appears for the first time
    """

    def __init__(self):
        super().__init__('log_node', namespace='yolo')

        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections',
            self.listener_callback,
            10,
        )
        self.classes_pub = self.create_publisher(String, '/yolo/classes', 10)
        self.previous_classes = set()

        self.get_logger().info('Listening to /yolo/detections...')

    def listener_callback(self, msg: DetectionArray) -> None:
        """Handle incoming detections and publish new classes once."""
        current_classes = {detection.class_name for detection in msg.detections}
        new_classes = current_classes - self.previous_classes

        if new_classes:
            for detection in msg.detections:
                if detection.class_name in new_classes:
                    # Log any newly observed object Classes
                    log = (
                        f'New Object Detected - Class ID: {detection.class_id}, '
                        f'Class Name: {detection.class_name}, '
                        f'Score: {detection.score:.2f}'
                    )
                    # Log to console
                    self.get_logger().info(log)
                    # Publish the same log to /yolo/classes
                    self.classes_pub.publish(String(data=log))

        self.previous_classes = current_classes


def main():
    rclpy.init()
    node = LogNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
