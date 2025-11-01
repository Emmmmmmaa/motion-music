class GestureClassifier:
    def __init__(self):
        self.gesture_duration = {}
        self.min_duration = 0.5  # 0.5秒稳定
    
    def _is_finger_up(self, landmarks, finger):
        # 简化版：根据关键点y坐标判断手指伸直
        finger_indices = [[4, 3, 2], [8, 6], [12, 10], [16, 14], [20, 18]]
        tips = [4, 8, 12, 16, 20]
        
        if finger == 0:  # 拇指
            return landmarks[tips[0]][1] < landmarks[3][1]
        else:
            return landmarks[tips[finger]][1] < landmarks[finger_indices[finger][1]][1]
    
    def classify(self, landmarks):
        if not landmarks or len(landmarks[0]) < 21:
            return None
        
        lm = landmarks[0]
        
        # 计算手指状态
        fingers = [self._is_finger_up(lm, i) for i in range(5)]
        up_count = sum(fingers)
        
        # 手势识别
        if all(fingers[1:]):  # 张开手掌
            return "open_palm"
        elif up_count == 0:  # 握拳
            return "fist"
        elif fingers[0] and not any(fingers[1:]):  # 竖起拇指
            return "thumbs_up"
        elif not fingers[0] and sum(fingers[1:]) == 1:  # 拇指向下
            return "thumbs_down"
        elif fingers[1] and fingers[4] and not any([fingers[2], fingers[3]]):  # 摇滚手势
            return "rock"
        
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
        
        # 动作映射
        actions = {
            "open_palm": "play",
            "fist": "pause",
            "thumbs_up": "next",
            "thumbs_down": "previous",
            "rock": "random"
        }
        
        return actions.get(gesture)

