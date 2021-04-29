## 基本信息

+ 数据保存在 56 服务器的 `/ssd01/data/open-images-v6` 中。
  + `images`：保存原始图片。
  + `annotations`：保存原始标签文件。
  + `labels`：对应的 yolo 格式标签
+ 对应数据处理脚本可以参考[这里](https://github.com/irvingzhang0512/open-images-downloader)

## v0.1

+ 通过 [Open Images Dataset V6](https://blog.csdn.net/irving512/article/details/116180438) 构建基础数据集。
+ 获取所有存在“Door”或“Window”的图片作为原始数据。
+ 根据原始图片，获取所有对应的 `Person, Door, Window` 的标注矿信息作为目标检测任务类别。
+ Train、Val、Test就是根据Open Images Dataset V6的原始比例。
+ 数据量：
  + 图片数量：67918/1031/3182
  + BBoxes 数量如下

```shell
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

+ 训练结果（没有调参）
  + yolov5s：mAP 0.20
  + yolov5x：mAP 0.24
