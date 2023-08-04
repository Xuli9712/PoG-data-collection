import vlc
import time
import mouse # pip install mouse
import keyboard # pip install keyboard
from datetime import datetime

def play_video(video_path: str):
    Instance = vlc.Instance("--no-xlib")
    player = Instance.media_player_new()
    Media = Instance.media_new(video_path)
    Media.get_mrl()
    player.set_media(Media)

    # 设置全屏并播放1秒，然后暂停
    player.set_fullscreen(True)
    player.play()
    time.sleep(1) # 让视频播放1秒
    player.pause()

    print("Press ESC to start playing...")
    keyboard.wait("esc")
    

    # 从暂停的位置开始播放
    player.play()

    start_time = datetime.now()
    print(f"Started playing at {start_time}")

    print(f"Mouse position: {mouse.get_position()}")

    # 等待视频播放完毕或再次按下esc键
    while player.get_state() != vlc.State.Ended:
        time.sleep(0.1)
        if keyboard.is_pressed('esc'):
            print("Escape key pressed, stopping playback")
            break

    end_time = datetime.now()
    print(f"Stopped playing at {end_time}")
    print(f"Actual duration: {(end_time - start_time).seconds / 60} minutes")

    # 释放资源
    player.release()

if __name__ == "__main__":
    video_path = 'circle_video1.avi' # 更改为你的视频路径
    play_video(video_path)