# Models Directory

Place your YOLO weight files here.

Supported examples:
- `.pt`, `.pth` (PyTorch)
- `.onnx` (ONNX)
- `.engine`, `.plan` (TensorRT)
- `.weights` (Darknet)
- `.tflite` (TensorFlow Lite)

- Do not commit large model files to the repository.
- Reference these weights via the `model` launch parameter, e.g. `model:=yolo_bringup/models/yolov8m.pt`.
- Keep filenames descriptive (e.g., `yolov8m.pt`, `yolov11x-seg.pt`).

This directory is intended for local development only.
