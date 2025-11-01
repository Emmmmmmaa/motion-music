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
        
    def _add_log(self, msg):
        self.logs.append(msg)
        if len(self.logs) > 5:
            self.logs.pop(0)
        print(msg)
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 检测手势
            landmarks, frame = self.detector.detect(frame)
            gesture = self.classifier.classify(landmarks)
            action = self.classifier.get_action(gesture)
            
            # 执行动作
            if action and action != self.current_action:
                self.current_action = action
                song = None
                
                if action == "play":
                    song = self.music.play_music()
                    self._add_log(f"[Gesture] Open Palm → [Action] Play")
                elif action == "pause":
                    song = self.music.pause_music()
                    self._add_log(f"[Gesture] Fist → [Action] Pause")
                elif action == "next":
                    song = self.music.next_music()
                    self._add_log(f"[Gesture] ThumbsUp → [Action] Next")
                elif action == "previous":
                    song = self.music.previous_music()
                    self._add_log(f"[Gesture] ThumbsDown → [Action] Previous")
                elif action == "random":
                    song = self.music.random_play()
                    self._add_log(f"[Gesture] Rock → [Action] Random")
                
                if song:
                    self._add_log(f"[Music] {song}")
            
            # 显示手势
            if gesture:
                cv2.putText(frame, gesture, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
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

