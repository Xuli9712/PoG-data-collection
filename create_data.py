import os
import shutil
import json

def process_images(source_folder, destination_folder, dot_list, interval):
    # 读取所有文件名，并按数字排序
    filenames = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]
    filenames.sort(key=lambda x: int(x.split('.')[0]))

    # 跳过间隔的一半数量的图像，然后按照整个间隔来获取图像
    start_index = int(250)
    selected_filenames = filenames[start_index::interval][:60]

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 生成要保存到JSON文件的列表
    json_list = []

    # 复制选定的图片到新文件夹，并添加信息到json_list
    for i, filename in enumerate(selected_filenames):
        src_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(destination_folder, filename)
        shutil.copy(src_path, dest_path)

        image_info = [filename, dot_list[i]]
        json_list.append(image_info)

    # 将json_list保存到JSON文件
    json_filename = os.path.join(destination_folder, destination_folder.split('\\')[-1] + '.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_list, json_file, indent=4)


if __name__ == "__main__":
    src_root = r"F:\videos"
    dest_root = r"F:\dataset"
    video_name = 'GX010976'
    parti_name = 'WXL6'
    map_name = [video_name, parti_name]
    dot_list = [(137, 67), (959, 67), (1507, 742), (1781, 202), (1781, 472), (137, 472), (1233, 202), (1781, 337), (685, 1012), (959, 337), (959, 607), (137, 67), (959, 472), (137, 202), (1233, 67), (1781, 1012), (1233, 742), (1781, 607), (137, 1012), (959, 1012), (1233, 472), (959, 877), (137, 67), (1781, 742), (685, 472), (137, 337), (137, 607), (137, 742), (411, 472), (1507, 1012), (1233, 877), (685, 742), (1507, 202), (137, 67), (411, 742), (137, 877), (685, 337), (1507, 337), (1507, 877), (411, 67), (411, 607), (685, 877), (685, 67), (1781, 877), (137, 67), (411, 202), (411, 337), (1507, 472), (411, 877), (1233, 607), (685, 607), (1507, 607), (685, 202), (1233, 337), (1507, 67), (411, 1012), (1233, 1012), (959, 742), (959, 202), (1781, 67)]
    print('ALL DOT NUM', len(dot_list))
    source_folder = os.path.join(src_root, map_name[0])
    dest_folder = os.path.join(dest_root, map_name[1])
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    process_images(source_folder, dest_folder, dot_list, interval=323)
