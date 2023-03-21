# OFA预训练模型
## News
- 2023年1月：
  - 优化了finetune流程，支持参数更新、自定义数据及脚本分布式训练等，见finetune示例。
- 2022年11月：
  - 发布ModelScope 1.0版本，以下能力请使用1.0.2及以上版本。
  - 新增[OFA Tutorial](https://modelscope.cn/docs/OFA_Tutorial#1.4%20%E5%A6%82%E4%BD%95%E8%AE%AD%E7%BB%83)。

OFA预训练模型是OFA在8个预训练任务（具体参见论文）上得到ckpt，是finetune下游任务的基础。


## 如何使用OFA预训练模型

### Finetune
模型细节参考文档：[OFA Tutorial](https://modelscope.cn/docs/OFA_Tutorial#1.4%20%E5%A6%82%E4%BD%95%E8%AE%AD%E7%BB%83) 1.4节。

这里直接使用预训练模型在caption任务上进行实例演示，要求 ModelScope Library >= 1.2.0

```python
import tempfile
from modelscope.msdatasets import MsDataset
from modelscope.metainfo import Trainers
from modelscope.trainers import build_trainer
from modelscope.utils.constant import DownloadMode
from modelscope.utils.hub import snapshot_download


train_dataset = MsDataset(
    MsDataset.load(
        "coco_2014_caption", 
        namespace="modelscope", 
        split="train[:100]",
        download_mode=DownloadMode.REUSE_DATASET_IF_EXISTS).remap_columns({
        'image': 'image',
        'caption': 'text'
    }))
test_dataset = MsDataset(
    MsDataset.load(
        "coco_2014_caption", 
        namespace="modelscope", 
        split="validation[:20]",
        download_mode=DownloadMode.REUSE_DATASET_IF_EXISTS).remap_columns({
        'image': 'image',
        'caption': 'text'
    }))


def cfg_modify_fn(cfg):
    cfg.train.hooks = [{
        'type': 'CheckpointHook',
        'interval': 2
    }, {
        'type': 'TextLoggerHook',
        'interval': 1
    }, {
        'type': 'IterTimerHook'
    }]
    cfg.train.max_epochs=2
    return cfg

pretrained_model = 'damo/ofa_pretrain_base_zh'
pretrain_path = snapshot_download(pretrained_model, revision='v1.0.2')

args = dict(
    model=pretrain_path,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    cfg_modify_fn=cfg_modify_fn,
    work_dir = tempfile.TemporaryDirectory().name)
trainer = build_trainer(name=Trainers.ofa, default_args=args)
trainer.train()
```


### ZeroShot
OFA预训练模型可以通过以下代码进行下载：
注：modelscope V1.0.0开始使用tag进行兼容性管理，目前策略是不指定tag的情况下使用modelscope版本发布前的最近的tag。因为预训练模型在modelscope==1.0.2版本后发布的，所以使用1.0.2版本的同学需要加上revision信息。
```python
from modelscope.utils.hub import snapshot_download
pretrained_model = 'damo/ofa_pretrain_base_zh'
pretrain_path = snapshot_download(pretrained_model, revision='v1.0.2')
```
有了预训练模型，可以OFA自身的能力特点（One For All）利用预训练模型测试其在下游任务的效果，替换configuration文件示例：

```python
import os
import shutil
from modelscope.utils.hub import snapshot_download
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from modelscope.utils.constant import ModelFile

pretrained_model = 'damo/ofa_pretrain_base_zh'
pretrain_path = snapshot_download(pretrained_model, revision='v1.0.2')
task_model = 'damo/ofa_image-caption_muge_base_zh'
task_path = snapshot_download(task_model)

shutil.copy(os.path.join(task_path, ModelFile.CONFIGURATION), # 将任务的配置覆盖预训练模型的配置
            os.path.join(pretrain_path, ModelFile.CONFIGURATION))

ofa_pipe = pipeline(Tasks.image_captioning, model=pretrain_path)
result = ofa_pipe('https://shuangqing-public.oss-cn-zhangjiakou.aliyuncs.com/donuts.jpg')
print(result[OutputKeys.CAPTION]) 
```


## OFA是什么？
OFA(One-For-All)是通用多模态预训练模型，使用简单的序列到序列的学习框架统一模态（跨模态、视觉、语言等模态）和任务（如图片生成、视觉定位、图片描述、图片分类、文本生成等），详见我们发表于ICML 2022的论文：[OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence Learning Framework](https://arxiv.org/abs/2202.03052)，以及我们的官方Github仓库[https://github.com/OFA-Sys/OFA](https://github.com/OFA-Sys/OFA)。

<p align="center">
    <br>
    <img src="resources/OFA_logo_tp_path.svg" width="150" />
    <br>
<p>
<br>

<p align="center">
        <a href="https://github.com/OFA-Sys/OFA">Github</a>&nbsp ｜ &nbsp<a href="https://arxiv.org/abs/2202.03052">Paper </a>&nbsp ｜ &nbspBlog
</p>

<p align="center">
    <br>
        <video src="https://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/resources/modelscope_web/demo.mp4" loop="loop" autoplay="autoplay" muted width="100%"></video>
    <br>
</p>

## OFA模型规模

<table border="1" width="100%">
    <tr align="center">
        <th>Model</th><th>Params-en</th><th>Params-zh</th><th>Backbone</th><th>Hidden size</th><th>Intermediate size</th><th>Num. of heads</th><th>Enc layers</th><th>Dec layers</th>
    </tr>
    <tr align="center">
        <td>OFA<sub>Tiny</sub></td><td>33M</td><td>-</td><td>ResNet50</td><td>256</td><td>1024</td><td>4</td><td>4</td><td>4</td>
    </tr>
    <tr align="center">
        <td>OFA<sub>Medium</sub></td><td>93M</td><td>-</td><td>ResNet101</td><td>512</td></td><td>2048</td><td>8</td><td>4</td><td>4</td>
    </tr>
    <tr align="center">
        <td>OFA<sub>Base</sub></td><td>180M</td><td>160M</td><td>ResNet101</td><td>768</td></td><td>3072</td><td>12</td><td>6</td><td>6</td>
    </tr>
    <tr align="center">
        <td>OFA<sub>Large</sub></td><td>470M</td><td>440M</td><td>ResNet152</td><td>1024</td></td><td>4096</td><td>16</td><td>12</td><td>12</td>
    </tr>
    <tr align="center">
        <td>OFA<sub>Huge</sub></td><td>930M</td><td>-</td><td>ResNet152</td><td>1280</td></td><td>5120</td><td>16</td><td>24</td><td>12</td>
    </tr>
</table>
<br>

## OFA 模型任务矩阵
目前ModelScope上面所有已经上传的模型和任务可以在下面导航表格看到，点击链接可以跳转到相应modelcard。

| 模型规模 | 预训练 | 图像描述 | 视觉问答 | 视觉定位 | 视觉蕴含 | 文生图 | 图像分类 | 文字识别 | 文本摘要 | 文本分类 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFA<sub>Tiny</sub> | [英文](https://modelscope.cn/models/damo/ofa_pretrain_tiny_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_image-caption_coco_distilled_en/summary) | - | [英文](https://modelscope.cn/models/damo/ofa_visual-grounding_refcoco_distilled_en) | [英文](https://modelscope.cn/models/damo/ofa_visual-entailment_snli-ve_distilled_v2_en/summary) | - | - | - | - | - |
| OFA<sub>Medium</sub> | [英文](https://modelscope.cn/models/damo/ofa_pretrain_medium_en/summary)  | - | - | - | - | - | - | - | - | - |
| OFA<sub>Base</sub> | [中文](https://modelscope.cn/models/damo/ofa_pretrain_base_zh/summary)/[英文](https://modelscope.cn/models/damo/ofa_pretrain_base_en/summary) | [中文电商](https://modelscope.cn/models/damo/ofa_image-caption_muge_base_zh/summary) | - | - | - | - | - | [场景中文](https://modelscope.cn/models/damo/ofa_ocr-recognition_scene_base_zh/summary) | - | - |
| OFA<sub>Large</sub> | [中文](https://modelscope.cn/models/damo/ofa_pretrain_large_zh/summary)/[英文](https://modelscope.cn/models/damo/ofa_pretrain_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_image-caption_coco_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_visual-question-answering_pretrain_large_en/summary) | [中文](https://modelscope.cn/models/damo/ofa_visual-grounding_refcoco_large_zh/summary)/[英文](https://modelscope.cn/models/damo/ofa_visual-grounding_refcoco_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_visual-entailment_snli-ve_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_text-to-image-synthesis_coco_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_image-classification_imagenet_large_en/summary) | - | [英文](https://modelscope.cn/models/damo/ofa_summarization_gigaword_large_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_text-classification_mnli_large_en/summary) |
| OFA<sub>Huge</sub> | [英文](https://modelscope.cn/models/damo/ofa_pretrain_huge_en/summary)  | [英文](https://modelscope.cn/models/damo/ofa_image-caption_coco_huge_en/summary) | [英文](https://modelscope.cn/models/damo/ofa_visual-question-answering_pretrain_huge_en/summary) | - | - | - | - | - | - | - |
| OFA<sub>6B</sub> | - | [英文](https://modelscope.cn/models/damo/ofa_image-caption_coco_6b_en/summary) | - | - | - | - | - | - | - | - |


## 相关论文以及引用
如果你觉得OFA好用，喜欢我们的工作，欢迎引用：
```
@article{wang2022ofa,
  author    = {Peng Wang and
               An Yang and
               Rui Men and
               Junyang Lin and
               Shuai Bai and
               Zhikang Li and
               Jianxin Ma and
               Chang Zhou and
               Jingren Zhou and
               Hongxia Yang},
  title     = {OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence
               Learning Framework},
  journal   = {CoRR},
  volume    = {abs/2202.03052},
  year      = {2022}
}
```