import argparse
import pandas as pd

def generate_classes_ids(selected_classes):
    class_name_file_path = "annotations/class-descriptions-boxable.csv"
    class_name_to_id = {}
    with open(class_name_file_path, "r") as f:
        lines = [line.strip() for line in f]
        for line in lines:
            row = line.split(",")
            class_name_to_id[row[1]] = row[0]
    assert set(selected_classes) <= set(class_name_to_id.keys())
    return [class_name_to_id[name] for name in selected_classes]

def handle_one_split(split, file_list_path, selected_classes_ids):
    assert split in ["train", "validation", "test"]
    label_file_path = f'annotations/{split}-annotations-bbox.csv'
    df = pd.read_csv(label_file_path)
    # 根据类别过滤，获取不同的image id
    df = df[df.LabelName.isin(selected_classes_ids)]
    image_ids = df.ImageID.unique()

    with open(file_list_path, "a") as f:
        lines = [f'{split}/{id}\n' for id in image_ids]
        f.writelines(lines)
    print(f"{split} {len(lines)}")


def main(args):
    selected_classes_ids = generate_classes_ids(args.selected_classes)

    if args.splits is None:
        args.splits = ["train", "validation", "test"]
    for split in args.splits:
        handle_one_split(split, args.filelist, selected_classes_ids)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("selected_classes", nargs='+', type=str)
    parser.add_argument("--filelist", type=str, default="filelist.txt")
    parser.add_argument("--splits", nargs="+", type=str, default=None)
    
    main(parser.parse_args())
