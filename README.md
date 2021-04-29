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
