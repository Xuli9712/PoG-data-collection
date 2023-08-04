import cv2
import random
import pyautogui
import numpy as np
import math
import os

def get_monitor_dimensions():
    screenWidthPixel, screenHeightPixel = pyautogui.size()
    print(f"Screen size: {screenWidthPixel}x{screenHeightPixel}")
    return (screenWidthPixel, screenHeightPixel)

def create_black_image(monitor_pixels):
    width, height = monitor_pixels
    img = np.zeros((height, width, 3), np.float32)
    return img

def create_image(monitor_pixels, center, circle_scale, inner_radius):
    width, height = monitor_pixels
    img = np.zeros((height, width, 3), np.float32)
    radius = int(circle_scale)
    cv2.circle(img, center, radius, (1, 1, 1), -1)  # Fill the circle with white color
    cv2.circle(img, center, 5, (0, 1, 0), -1)  # Mark the center with a different color (green in this case)
    end_animation_loop = circle_scale <= inner_radius  # Stop when the circle is smaller than inner_radius
    return img, end_animation_loop

def generate_points(monitor_pixels, num_points=60):
    width, height = monitor_pixels
    num_original_points = 56
    num_points_per_row = int(math.sqrt(num_original_points))
    num_points_per_column = num_original_points // num_points_per_row
    grid_x = width // num_points_per_row
    grid_y = height // num_points_per_column

    points = [(i * grid_x + grid_x // 2, j * grid_y + grid_y // 2) for i in range(num_points_per_row) for j in range(num_points_per_column)]
    points.sort(key=lambda x: (x[1], x[0]))  # Sort the points from top-left to bottom-right

    # Get the first and last points, and remove them from the list
    first_point = points.pop(0)
    last_point = max(points, key=lambda x: (x[0], -x[1]))
    points.remove(last_point)

    # Shuffle the remaining points
    random.seed(1)  # Set seed for reproducibility
    random.shuffle(points)

    # Add the repeated first points at regular intervals
    interval = len(points) // 5
    for i in range(4, 0, -1):  # We start from the end to keep the indices correct while inserting
        insert_position = interval * i
        points.insert(insert_position, first_point)

    # Add the first and last points back to their respective positions
    points.insert(0, first_point)
    points.append(last_point)

    return points

def create_video(frame_folder, video_name, fps, monitor_pixels, total_frames):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width, height = monitor_pixels
    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
    for i in range(total_frames):
        filename = os.path.join(frame_folder, f"frame_{i}.png")
        img = cv2.imread(filename)
        out.write(img)
    out.release()

def show_point_on_screen(outer_radius: float, inner_radius: float):
    monitor_pixels = get_monitor_dimensions()
    circle_reduction_per_frame = (outer_radius - inner_radius) / 179

    frame_folder = "frames"
    os.makedirs(frame_folder, exist_ok=True)
    total_frames_per_point = 180
    total_frames = total_frames_per_point * 60

    # 添加60帧的纯黑屏
    black_image = create_black_image(monitor_pixels)
    for i in range(60):
        filename = os.path.join(frame_folder, f"frame_{i}.png")
        cv2.imwrite(filename, black_image * 255)

    frame_count = 60
    points = generate_points(monitor_pixels)
    print(points)
    for center in points:
        circle_scale = outer_radius
        for frame_number in range(total_frames_per_point):
            image, _ = create_image(monitor_pixels, center, circle_scale, inner_radius)
            filename = os.path.join(frame_folder, f"frame_{frame_count}.png")
            cv2.imwrite(filename, image * 255)
            circle_scale -= circle_reduction_per_frame
            frame_count += 1

    create_video(frame_folder, 'circle_video1.avi', 60, monitor_pixels, total_frames + 60)  # 注意更新总帧数
    print("Finished")

if __name__ == "__main__":
    show_point_on_screen(40, 10)
