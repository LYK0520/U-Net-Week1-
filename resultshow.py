import os
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

result_path = '/home/luoyk/Learning/ZJU/Tao/Week1/data/test/'
all_files = os.listdir(result_path)

def sort_by_number(filename):
    return int(re.findall(r'\d+', filename)[0])

imgs_path = sorted([filename for filename in all_files if not filename.endswith("_res.png")], key=sort_by_number)
imgs_path1 = sorted([filename for filename in all_files if filename.endswith("_res.png")], key=sort_by_number)
#imgs_path = sorted(os.listdir(result_path))  # 确保按照文件名的顺序排列
print(len(imgs_path))
nrows = 6
ncols = 10

fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*2, nrows*2))

pic_index = 0
for i in range(nrows):
    for j in range(ncols//2):
        if pic_index >= len(imgs_path):
            break
        ax = axes[i, j*2]
        ax.axis('off')
        ax1 = axes[i, j*2+1]
        ax1.axis('off')
        print(imgs_path[pic_index])
        img_path_A = os.path.join(result_path, imgs_path[pic_index])
        # print(pic_index)
        img_path_A_res = os.path.join(result_path, imgs_path1[pic_index])
        print(imgs_path1[pic_index])
        img_A = mpimg.imread(img_path_A)
        img_A_res = mpimg.imread(img_path_A_res)
        ax.imshow(img_A)
        ax1.imshow(img_A_res)  # 使用 alpha 控制透明度
        pic_index += 1

plt.tight_layout()
plt.show()