# Download Selected classes Images From Open-Images-Dataset V6


## Tutorials

```shell
# Step 1: Download annotations
mkdir annotations
wget -P annotations/ -O train-annotations-bbox.csv https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
wget -P annotations/ https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
wget -P annotations/ https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv
wget -P annotations/ https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv

# Step 2: Generate filelist
python generate_filelist.py Window Door --filelist filelist2.txt --splits train validation test

# Step 3: Download Images to `./images` with generated filelist
# Modify official downloader.py: skip images that are already downloaded
python downloader.py filelist.txt --num_processes 5 --download_folder ./images

# Step 4: Visualize downloaded images with bboxes. Three params to be modified.
# splits = ["train", "validation", "test"]
# class_names_file = "annotations/class-descriptions-boxable.csv"
# images_dir = "./images"
python visualize.py

# Step 5: Convert BBoxes to Yolo
# Generate annotation file for all images in `images_dir`
# and generate filelist file in `./yolo`.
# Save filelist file `{split}_{version}.txt` into `./yolo/{version}`
python convert_to_yolo.py
```

## Dataset Versions

### V0.1

+ 从 Open Images Dataset V6 中获取所有存在“Door”或“Window”的图片作为原始数据。
+ 根据原始图片，获取所有对应的 `Person, Door, Window` 的标注矿信息作为目标检测任务类别。
+ Train、Val、Test就是根据Open Images Dataset V6的原始比例。
+ 数据量：
  + 图片数量：67918/1031/3182
  + BBoxes 数量：
```
train: 
Person -> 8531
Door -> 19256
Window -> 503467
validation: 
Person -> 375
Door -> 287
Window -> 7583
test: 
Person -> 1137
Door -> 787
Window -> 25557
```
+ 训练结果
  + yolov5s：mAP 0.20
  + yolov5x：mAP 0.24
