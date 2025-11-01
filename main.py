import cv2
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from music_controller import MusicController

class GestureMusicPlayer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector()
        self.classifier = GestureClassifier()
        self.music = MusicController()
        self.current_action = None
        self.logs = []
        # 启动时自动播放音乐
        self._auto_start_music()
        
    def _add_log(self, msg):
        self.logs.append(msg)
        if len(self.logs) > 5:
            self.logs.pop(0)
        print(msg)
    
    def _auto_start_music(self):
        """程序启动时自动播放音乐"""
        if self.music.playlist:
            song = self.music.play_music()
            if song:
                self._add_log(f"[Auto] Music started: {song}")
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 检测手部和绘制关键点
            landmarks, frame = self.detector.detect(frame)
            
            # 使用 MediaPipe GestureRecognizer 识别手势（直接传入 frame）
            gesture = self.classifier.classify(frame)
            action = self.classifier.get_action(gesture)
            
            # 显示识别到的手势（用于调试）
            if gesture:
                cv2.putText(frame, f"Gesture: {gesture}, action: {action}, current_action={self.current_action}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # 执行动作
            if action and action != self.current_action:
                self.current_action = action
                song = None
                
                if action == "play":
                    # 如果暂停了，继续播放；如果正在播放，不做任何操作
                    if self.music.paused:
                        song = self.music.play_music()
                        self._add_log(f"[Gesture] Open Palm → [Action] Resume")
                    else:
                        # 已经在播放，不做任何操作
                        self.current_action = None  # 重置，避免重复触发
                        continue
                elif action == "pause":
                    # 切换暂停/继续状态
                    if self.music.paused:
                        song = self.music.play_music()
                        self._add_log(f"[Gesture] Fist → [Action] Resume")
                    else:
                        song = self.music.pause_music()
                        self._add_log(f"[Gesture] Fist → [Action] Pause")
                elif action == "next":
                    song = self.music.next_music()
                    self._add_log(f"[Gesture] ThumbsUp → [Action] Next")
                    self.current_action = None  # 切歌后重置，允许连续切歌
                elif action == "previous":
                    song = self.music.previous_music()
                    self._add_log(f"[Gesture] ThumbsDown → [Action] Previous")
                    self.current_action = None  # 切歌后重置，允许连续切歌
                elif action == "random":
                    song = self.music.random_play()
                    self._add_log(f"[Gesture] Rock → [Action] Random")
                    self.current_action = None  # 切歌后重置，允许连续切歌
                
                if song:
                    self._add_log(f"[Music] {song}")
            
            # 如果手势消失，重置 current_action 以允许再次触发
            if not gesture and self.current_action:
                self.current_action = None
            
            
            # 显示日志
            y = 60
            for log in self.logs:
                cv2.putText(frame, log, (10, y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y += 25
            
            # 显示当前歌曲
            if self.music.playlist:
                current = self.music.playlist[self.music.current_index]
                song_name = current.replace('\\', '/').split('/')[-1][:50]
                cv2.putText(frame, f"Now: {song_name}", (10, frame.shape[0] - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Gesture Music Player', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.detector.release()

if __name__ == "__main__":
    player = GestureMusicPlayer()
    player.run()

