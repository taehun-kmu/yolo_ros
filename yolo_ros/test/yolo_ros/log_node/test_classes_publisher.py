import time
from typing import List

import pytest

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from std_msgs.msg import String
from yolo_msgs.msg import Detection, DetectionArray


@pytest.mark.launch_test
def test_log_node_does_not_republish_same_class_with_new_id():
    """Ensure DetectionLog publishes only on new classes (not IDs)."""
    rclpy.init()

    # Import here to avoid initializing ROS 2 during collection time
    from yolo_ros.log_node import LogNode  # noqa: WPS433

    log_node = LogNode()
    helper = Node("log_node_class_test_helper")

    received: List[str] = []

    def ids_cb(msg: String):
        received.append(msg.data)

    # Subscribe to the topic where DetectionLog forwards messages
    helper.ids_sub = helper.create_subscription(String, "/yolo/classes", ids_cb, 10)

    # Publisher to trigger the log node callback
    pub = helper.create_publisher(DetectionArray, "/yolo/detections", 10)

    # Frame 1: class 'person', id 'p1' -> should publish (new class)
    det1 = Detection()
    det1.class_id = 0
    det1.class_name = "person"
    det1.score = 0.90
    det1.id = "p1"
    arr1 = DetectionArray()
    arr1.detections.append(det1)

    # Frame 2: same class 'person', new id 'p2' -> should NOT publish again
    det2 = Detection()
    det2.class_id = 0
    det2.class_name = "person"
    det2.score = 0.88
    det2.id = "p2"
    arr2 = DetectionArray()
    arr2.detections.append(det2)

    executor = SingleThreadedExecutor()
    executor.add_node(log_node)
    executor.add_node(helper)

    try:
        # Publish first frame and wait for one message
        pub.publish(arr1)
        start = time.time()
        while time.time() - start < 3.0 and len(received) < 1:
            executor.spin_once(timeout_sec=0.1)

        assert len(received) >= 1, "Expected one message for new class 'person'"

        # Publish second frame and ensure no new message is received
        before_count = len(received)
        pub.publish(arr2)
        start = time.time()
        while time.time() - start < 2.0:
            executor.spin_once(timeout_sec=0.1)

        assert (
            len(received) == before_count
        ), "Should not republish for same class despite new ID"
    finally:
        executor.shutdown()
        helper.destroy_node()
        log_node.destroy_node()
        rclpy.shutdown()
