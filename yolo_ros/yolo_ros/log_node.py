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
        self.get_logger().info('Listening to /yolo/detections...')

    def listener_callback(self, msg):
        for detection in msg.detections:
            self.get_logger().info(
                f'Class ID: {detection.class_id}, '
                f'Class Name: {detection.class_name}, '
                f'Score: {detection.score:.3f}, '
            )

def main():
    rclpy.init()
    node = DetectionLog()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
