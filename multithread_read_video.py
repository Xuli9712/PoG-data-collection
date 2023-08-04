import cv2
import os
from concurrent.futures import ThreadPoolExecutor

def save_frame(frame, frame_filename):
    cv2.imwrite(frame_filename, frame)

def save_frames_from_video(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    with ThreadPoolExecutor() as executor:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = f"{output_folder}/{frame_count:06d}.jpg"

            # 提交保存帧的任务到线程池
            executor.submit(save_frame, frame, frame_filename)

            frame_count += 1

    cap.release()

if __name__ == "__main__":
    video_folder = r"F:\videos"

    for filename in os.listdir(video_folder):
        if filename.endswith('.MP4'):
            video_path = os.path.join(video_folder, filename)
            output_folder = os.path.join(video_folder, os.path.splitext(filename)[0])

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            save_frames_from_video(video_path, output_folder)
            print(f'Finished processing {filename}')
