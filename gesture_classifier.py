import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
import cv2

class GestureClassifier:
    def __init__(self):
        self.gesture_duration = {}
        self.min_duration = 0.5
        
        # 使用 MediaPipe GestureRecognizer
        model_path = 'models/gesture_recognizer.task'
        if not os.path.exists(model_path):
            print("Warning: gesture_recognizer.task not found.")
            print("Please download from:")
            print("https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task")
            print("Placing it in the project root directory.")
            self.recognizer = None
        else:
            base_options = python.BaseOptions(model_asset_path=model_path)
            options = vision.GestureRecognizerOptions(base_options=base_options)
            self.recognizer = vision.GestureRecognizer.create_from_options(options)
    
    # ===== 旧的运算规则（已注释，保留作为参考）=====
    # def _is_finger_up(self, landmarks, finger):
    #     # 简化版：根据关键点y坐标判断手指伸直
    #     finger_indices = [[4, 3, 2], [8, 6], [12, 10], [16, 14], [20, 18]]
    #     tips = [4, 8, 12, 16, 20]
    #     
    #     if finger == 0:  # 拇指
    #         return landmarks[tips[0]][1] < landmarks[3][1]
    #     else:
    #         return landmarks[tips[finger]][1] < landmarks[finger_indices[finger][1]][1]
    # 
    # def classify_old(self, landmarks):
    #     if not landmarks or len(landmarks[0]) < 21:
    #         return None
    #     
    #     lm = landmarks[0]
    #     
    #     # 计算手指状态
    #     fingers = [self._is_finger_up(lm, i) for i in range(5)]
    #     up_count = sum(fingers)
    #     
    #     # 手势识别
    #     if all(fingers[1:]):  # 张开手掌
    #         return "open_palm"
    #     elif up_count == 0:  # 握拳
    #         return "fist"
    #     # elif fingers[0] and not any(fingers[1:]):  # 竖起拇指
    #     #     return "thumbs_up"
    #     elif not fingers[0] and sum(fingers[1:]) == 1:  # 拇指向下
    #         return "thumbs_down"
    #     elif fingers[1] and fingers[4] and not any([fingers[2], fingers[3]]):  # 摇滚手势
    #         return "rock"
    #     
    #     return None
    
    def classify(self, frame):
        """
        使用 MediaPipe GestureRecognizer 识别手势
        frame: numpy array (OpenCV BGR format)
        """
        if self.recognizer is None:
            return None
        
        try:
            # 将 BGR 转换为 RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 确保数据格式正确（numpy array）
            rgb_frame = np.ascontiguousarray(rgb_frame)
            
            # 创建 MediaPipe Image (SRGB 格式)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 识别手势
            recognition_result = self.recognizer.recognize(mp_image)
            
            # 获取识别结果
            if recognition_result.gestures and len(recognition_result.gestures) > 0:
                # 获取置信度最高的手势
                top_gesture = recognition_result.gestures[0][0]
                gesture_name = top_gesture.category_name.lower()
                
                # MediaPipe 手势名称转换为我们的格式
                gesture_map = {
                    "open_palm": "open_palm",
                    "closed_fist": "fist",
                    "thumb_up": "thumb_up",
                    "thumb_down": "thumb_down",
                    "victory": "rock",  # Victory 手势作为摇滚手势
                    "pointing_up": None  # 暂不使用
                }
                
                # 返回标准化的手势名称
                mapped_gesture = gesture_map.get(gesture_name, gesture_name)
                return mapped_gesture if mapped_gesture else None
            
            return None
        except Exception as e:
            print(f"Error in gesture recognition: {e}")
            return None
    
    def get_action(self, gesture):
        if not gesture:
            return None
        
        # 去抖动
        from time import time
        now = time()
        
        if gesture not in self.gesture_duration:
            self.gesture_duration[gesture] = now
        
        if now - self.gesture_duration[gesture] < self.min_duration:
            return None
        
        # 清理其他手势计时
        self.gesture_duration = {gesture: now}
        
        # 动作映射（MediaPipe 手势 -> 音乐控制动作）
        actions = {
            "open_palm": "play",
            "closed_fist": "pause",
            "fist": "pause",
            "thumb_up": "previous",
            "thumb_down": "next",
            "victory": "random",  # Victory 手势作为随机播放
            "rock": "random"
        }
        
        return actions.get(gesture)

