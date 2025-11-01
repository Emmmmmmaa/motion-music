import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """使用 OpenCV 手动绘制关键点，避免 matplotlib 依赖"""
        h, w, c = frame.shape
        
        # MediaPipe HAND_CONNECTIONS 的连接关系
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # 拇指
            (0, 5), (5, 6), (6, 7), (7, 8),  # 食指
            (0, 9), (9, 10), (10, 11), (11, 12),  # 中指
            (0, 13), (13, 14), (14, 15), (15, 16),  # 无名指
            (0, 17), (17, 18), (18, 19), (19, 20),  # 小指
            (5, 9), (9, 13), (13, 17)  # 掌部连接
        ]
        
        # 绘制连接线
        for start_idx, end_idx in connections:
            start = hand_landmarks.landmark[start_idx]
            end = hand_landmarks.landmark[end_idx]
            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 绘制关键点
        for lm in hand_landmarks.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
    
    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self._draw_landmarks(frame, hand_landmarks)
                landmarks.append([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])
        
        return landmarks, frame
    
    def release(self):
        self.hands.close()