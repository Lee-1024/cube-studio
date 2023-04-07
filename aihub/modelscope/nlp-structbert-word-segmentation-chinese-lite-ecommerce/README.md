
# BAStructBERT电商领域中文分词模型介绍

## 模型描述
电商领域的分词模型, 采用无监督统计特征增强的StructBERT-Lite+softmax序列标注模型,序列标注标签体系(B、I、E、S),四个标签分别表示单字处理单词的起始、中间、终止位置或者该单字独立成词; 以StructBERT预训练语言模型为底座的序列标注模型可以参考下面的模型图:

<div align=center><img width="450" height="300" src="resources/ecom-cws-model.png" /></div>

StructBERT预训练语言模型可以参考 [StructBERT: Incorporating Language Structures into Pre-training for Deep Language Understanding](https://arxiv.org/abs/1908.04577)。为了进一步提升中文分词模型的效果，在StructBERT模型基
础上, 通过在预训练过程中增加大规模无监督词汇边界统计信息可以有效提升预训练模型对词汇边界的识别能力。我们实验验证融合词汇边界信息的预训练模型Boundary Aware StructBERT (BAStructBERT)模型在绝大多数中文序列标注任务上有进一步的效果提升。BAStructBERT模型结构和基础的StructBERT模型一致, BAStructBERT模型的预训练流程示意图如下所示, 更加详细的模型结构和实验结果将在后续公开的论文中介绍。

<div align=center><img src="./resources/bastructbert.png" /></div>

电商领域的分词训练数据基于电商搜索Query和标题数据标注得到, 对比通用领域分词模型, 主要提升对电商领域特有的品牌、品类、商品修饰等词汇的切分准确率

```
- 输入: cos风修身吊带针织连衣裙女收腰显瘦小黑裙长裙
- 通用领域分词结果: cos 风 修身 吊带 针织 连衣裙 女 收 腰 显 瘦 小 黑裙 长裙
- 电商领域分词结果: cos风 修身 吊带 针织 连衣裙 女 收腰 显瘦 小黑裙 长裙
```

## 期望模型使用方式以及适用范围
本模型主要用于给输入中文句子产出分词结果。用户可以自行尝试输入中文句子。具体调用方式请参考代码示例。

### 如何使用
在安装ModelScope完成之后即可使用chinese-word-segmentation(中文分词)的能力, 默认单句长度不超过默认单句长度不超过126。如需增加单句的切分长度，可以修改[TokenClassificationTransformersPreprocessor](https://github.com/modelscope/modelscope/blob/master/modelscope/preprocessors/nlp/token_classification_preprocessor.py#L223)中的最大sequence长度。

#### 代码范例
```python
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
# Version less than 1.1 please use TokenClassificationPreprocessor
from modelscope.preprocessors import TokenClassificationTransformersPreprocessor

model_id = 'damo/nlp_structbert_word-segmentation_chinese-lite-ecommerce'
model = Model.from_pretrained(model_id)
tokenizer = TokenClassificationTransformersPreprocessor(model.model_dir)
pipeline_ins = pipeline(task=Tasks.word_segmentation, model=model, preprocessor=tokenizer)
result = pipeline_ins(input="收腰显瘦黑裙长裙")
print (result)
# {'output': '收腰 显瘦 黑裙 长裙'}
```

### 模型局限性以及可能的偏差
本模型基于电商领域分词数据训练，在其它领域中文文本上的分词效果会有降低，请用户自行评测后决定如何使用。

### 训练
模型采用2张NVIDIA V100机器训练, 超参设置如下:

```
train_epochs=10
max_sequence_length=256
batch_size=64
learning_rate=5e-5
optimizer=AdamW
```

### 数据评估及结果

模型在电商标题、Query测试数据评估结果:

| Model | Precision | Recall | F1    |  Inference speed on CPU   |
|-------|-----------|--------|-------| -------| 
|BAStructBERT-Base | 97.89     | 98.20  | 98.04 | 1.0x  |
|BAStructBERT-Lite | 98.55     | 97.48  | 97.69 | 2.91x |

### 模型训练示例代码
如果需要基于自己的数据对分词模型进行二次训练, 建议可以采用ModelScope提供的序列标注理解框架**AdaSeq**进行模型训练, **AdaSeq**是一个基于ModelScope的一站式NLP序列理解开源工具箱，支持高效训练自定义模型，旨在提高开发者和研究者们的开发和创新效率，助力模型快速定制和前沿论文工作>落地。

1. 安装AdaSeq

```shell
pip install adaseq
```

2. 模型微调

准备训练配置，将下面的代码保存为train.yaml。

该配置中的数据集为示例数据集[PKU分词训练数据](https://modelscope.cn/datasets/dingkun/chinese_word_segmentation_pku/summary)，如需使用自定义数据或调整参数，可参考《[AdaSeq模型训练最佳实践](https://github.com/modelscope/AdaSeq/blob/master/docs/tutorials/training_a_model_zh.md)》，准备数据或修改配置文件。AdaSeq中也提供了大量的[模型、论文、比赛复现示例]([https://github.com/modelscope/AdaSeq/tree/master/examples](https://github.com/modelscope/AdaSeq/tree/master/examples))，欢迎大家使用。``yaml``文件示例如下:

```yaml
experiment:
  exp_dir: experiments/
  exp_name: pku_cws
  seed: 42

task: word-segmentation

dataset:
  data_file:
    train: https://modelscope.cn/api/v1/datasets/dingkun/chinese_word_segmentation_pku/repo?Revision=master&FilePath=train.txt
    dev: https://modelscope.cn/api/v1/datasets/dingkun/chinese_word_segmentation_pku/repo?Revision=master&FilePath=dev.txt
    test: https://modelscope.cn/api/v1/datasets/dingkun/chinese_word_segmentation_pku/repo?Revision=master&FilePath=test.txt
  data_type: conll

preprocessor:
  type: sequence-labeling-preprocessor
  max_length: 256
  tag_scheme: BIES

data_collator: SequenceLabelingDataCollatorWithPadding

model:
  type: sequence-labeling-model
  embedder:
    model_name_or_path: damo/nlp_structbert_word-segmentation_chinese-lite-ecommerce
  dropout: 0.1
  use_crf: true

train:
  max_epochs: 30
  dataloader:
    batch_size_per_gpu: 32
  optimizer:
    type: AdamW
    lr: 2.0e-5
    param_groups:
      - regex: crf
        lr: 2.0e-1
  lr_scheduler:
    type: LinearLR
    start_factor: 1.0
    end_factor: 0.0
    total_iters: 30

evaluation:
  dataloader:
    batch_size_per_gpu: 64
  metrics:
    - type: ner-metric
    - type: ner-dumper
      model_type: sequence_labeling
      dump_format: conll
```

运行命令开始训练。在GPU上训练需要至少6G显存，可以根据实际GPU情况调整batch_size等参数。

```shell
adaseq train -c train.yaml
```

3. 模型文件

二进制模型文件和相关配置文件会保存在 `./experiments/pku_cws/${yymmddHHMMSS.ffffff}/output/`

4. 模型推理
需要指出的是, 上面的示例``yaml``配置中采用的crf解码方式, 所以最后训练得到分词模型是BERT-crf结构而非BERT-softmax结果(实测两者的效果很接近)。在推理阶段, 为了能做BERT-crf结构的推理, 我们可以采用ModelScope内置的针对NER任务的pipeline进行推理, 示例代码如下:

```python
from modelscope.utils.constant import Tasks
from modelscope.pipelines import pipeline
# pipeline = pipeline(Tasks.named_entity_recognition, ${model_save_path})
pipeline = pipeline(Tasks.named_entity_recognition, "./experiments/pku_cws/${yymmddHHMMSS.ffffff}/output/")
pipeline('美好世界')
# 输出结果如下:
# {'output': [{'type': 'CWS', 'start': 0, 'end': 2, 'span': '美好'}, {'type': 'CWS', 'start': 2, 'end': 4, 'span': '世界'}]}
```
## 引用
StructBERT模型可以参考论文
```BibTex
@article{wang2019structbert,
  title={Structbert: Incorporating language structures into pre-training for deep language understanding},
  author={Wang, Wei and Bi, Bin and Yan, Ming and Wu, Chen and Bao, Zuyi and Xia, Jiangnan and Peng, Liwei and Si, Luo},
  journal={arXiv preprint arXiv:1908.04577},
  year={2019}
}
```