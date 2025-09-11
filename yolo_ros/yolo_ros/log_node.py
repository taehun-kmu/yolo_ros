import rclpy
from rclpy.node import Node
from yolo_msgs.msg import DetectionArray


class DetectionLog(Node):
    def __init__(self):
        super().__init__('detection_log')
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections',
            self.listener_callback,
            10
        )
        self.previous_ids = set()
        self.get_logger().info('Listening to /yolo/detections...')

    def listener_callback(self, msg):
        current_ids = set(detection.id for detection in msg.detections)
        new_ids = current_ids - self.previous_ids

        if new_ids:
            for detection in msg.detections:
                if detection.id in new_ids:
                    self.get_logger().info(
                        f'New Object Detected - Class ID: {detection.class_id}, '
                        f'Class Name: {detection.class_name}, '
                            f'Score: {detection.score:.2f} '
                    )

        self.previous_ids = current_ids

def main():
    rclpy.init()
    node = DetectionLog()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
