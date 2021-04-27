import os
import cv2
import pandas as pd


def darknet_draw_bbox(img,
                      bboxes,
                      labels,
                      scores=None,
                      bboxes_color=(0, 255, 0),
                      bboxes_thickness=1,
                      text_color=(0, 255, 0),
                      text_thickness=2,
                      text_front_scale=0.5):
    """
    bbox的形式是 xyxy，取值范围是像素的值
    labels是标签名称
    scores是置信度，[0, 1]的浮点数
    """
    for idx, (bbox, label) in enumerate(zip(bboxes, labels)):
        xmin, ymin, xmax, ymax = bbox
        pt1 = (int(xmin), int(ymin))  # 左下
        pt2 = (int(xmax), int(ymax))  # 右上

        # 画bbox
        cv2.rectangle(img, pt1, pt2, bboxes_color, bboxes_thickness)

        # 写上对应的文字
        cur_label = label
        if scores is not None:
            cur_label += " [" + str(round(scores[idx] * 100, 2)) + "]"
        cv2.putText(
            img=img,
            text=cur_label,
            org=(pt1[0], pt1[1] - 5),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=.5,
            color=(0, 255, 0),
            thickness=2,
        )
    return img


if __name__ == '__main__':
    splits = ["train", "validation", "test"]
    class_names_file = "annotations/class-descriptions-boxable.csv"
    images_dir = "./images"

    # class id to name dict
    with open(class_names_file, "r") as f:
        class_id_to_name = {
            line.split(",")[0]: line.split(",")[1].strip()
            for line in f
        }
    print(f"Successfully create class id to name dict with {len(class_id_to_name)} keys")
    # exsiting image ids
    image_ids = [filename.split(".")[0] for filename in os.listdir(images_dir)]
    print(f"Successfully create image_ids with {len(image_ids)} elements")

    # 构建 df
    df = None
    for split in splits:
        label_file_path = f'annotations/{split}-annotations-bbox.csv'
        cur_df = pd.read_csv(label_file_path)
        cur_df = cur_df[cur_df.ImageID.isin(image_ids)]
        if len(cur_df) > 0:
            if df is None:
                df = cur_df
            else:
                df = pd.concat([df, cur_df])
        print(f"Successfully create {split} df with {len(cur_df)} elements")


    # 通过 df 获取 bboxes 信息
    image_id_to_bboxes = {}

    def _group_by(x):
        image_id = x.ImageID.unique()[0]
        bbox_list = []
        label_list = []
        for row in x.iterrows():
            bbox = (row[1].XMin, row[1].YMin, row[1].XMax, row[1].YMax)
            bbox = [float(b) for b in bbox]
            label = class_id_to_name[row[1].LabelName]
            bbox_list.append(bbox)
            label_list.append(label)
        image_id_to_bboxes[image_id] = (bbox_list, label_list)

    df.groupby("ImageID").apply(_group_by)
    print(f"Successfully create image_id_to_bboxes with {len(image_id_to_bboxes)} elements")

    for image_id in image_id_to_bboxes.keys():
        bbox_list, label_list = image_id_to_bboxes[image_id]
        img = cv2.imread(os.path.join(images_dir, f'{image_id}.jpg'))
        h, w, _ = img.shape
        bbox_list = [(bbox[0] * w, bbox[1] * h, bbox[2] * w, bbox[3] * h)
                     for bbox in bbox_list]
        img = darknet_draw_bbox(img, bbox_list, label_list)
        cv2.imshow("demo", img)
        cv2.waitKey(0)
