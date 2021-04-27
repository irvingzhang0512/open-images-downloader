import os
import pandas as pd

version = "v0.1"
images_dir = "./images"
labels_dir = "./labels"
base_annotations_path = "./yolo"
annotations_path = os.path.join(base_annotations_path, version)
if not os.path.exists(annotations_path):
    os.mkdir(annotations_path)
target_class_names = ["Person", "Door", "Window"]
splits = ["train", "validation", "test"]

# class id to name dict
class_names_file = "annotations/class-descriptions-boxable.csv"
with open(class_names_file, "r") as f:
    class_id_to_name = {
        line.split(",")[0]: line.split(",")[1].strip()
        for line in f
    }
class_name_to_id = {v: k for k, v in class_id_to_name.items()}
target_class_ids = [class_name_to_id[name] for name in target_class_names]
print(
    f"Successfully create class id to name dict with {len(class_id_to_name)} keys"
)


def _convert_one_split(image_ids, split):
    label_file_path = f'annotations/{split}-annotations-bbox.csv'
    cur_df = pd.read_csv(label_file_path)
    cur_df = cur_df[cur_df.ImageID.isin(image_ids)]
    cur_df = cur_df[cur_df.LabelName.isin(target_class_ids)]

    annotation_filename = f"{split}_{version}.txt"
    filelist_writer = open(os.path.join(annotations_path, annotation_filename), "w")

    samples_cnt = {k: 0 for k in target_class_names}

    def _group_by(x):
        image_id = x.ImageID.unique()[0]
        img_path = os.path.join(os.path.abspath(images_dir),
                                f'{image_id}.jpg')
        filelist_writer.write(img_path + '\n')
        with open(os.path.join(labels_dir, f'{image_id}.txt'), "w") as label_writer:
            for row in x.iterrows():
                x1, y1, x2, y2 = float(row[1].XMin), float(row[1].YMin), float(
                    row[1].XMax), float(row[1].YMax)
                w, h = x2 - x1, y2 - y1
                cx, cy = x1 + w / 2, y1 + h / 2
                label_id = target_class_names.index(class_id_to_name[row[1].LabelName])
                label_writer.write(f'{label_id} {cx} {cy} {w} {h}\n')
                samples_cnt[class_id_to_name[row[1].LabelName]] += 1

    cur_df.groupby("ImageID").apply(_group_by)
    filelist_writer.close()
    print(f'{split}: ')
    for key in samples_cnt:
        print(f"{key} -> {samples_cnt[key]}")

if __name__ == '__main__':
    # exsiting image ids
    image_ids = [filename.split(".")[0] for filename in os.listdir(images_dir)]
    for split in splits:
        _convert_one_split(image_ids, split)
