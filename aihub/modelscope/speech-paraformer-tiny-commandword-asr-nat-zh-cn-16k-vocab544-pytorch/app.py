import base64
import io,sys,os
from cubestudio.aihub.model import Model,Validator,Field_type,Field

import pysnooper
import os

class SPEECH_PARAFORMER_TINY_COMMANDWORD_ASR_NAT_ZH_CN_16K_VOCAB544_PYTORCH_Model(Model):
    # 模型基础信息定义
    name='speech-paraformer-tiny-commandword-asr-nat-zh-cn-16k-vocab544-pytorch'   # 该名称与目录名必须一样，小写
    label='Paraformer语音识别-中文-端上指令词-16k-离线-tiny'
    describe="轻量化小词表Paraformer中文指令词识别模型，参数量控制在5M左右，支持通用智能家居交互等常规指令词，并且使用share embedding策略进一步缩小参数量。"
    field="听觉"    # [机器视觉，听觉，自然语言，多模态，强化学习，图论]
    scenes=""
    status='online'
    version='v20221001'
    pic='example.jpg'  # 离线图片，作为模型的样式图，330*180尺寸比例
    hot = "833"
    frameworks = "pytorch"
    doc = "https://modelscope.cn/models/damo/speech_paraformer-tiny-commandword_asr_nat-zh-cn-16k-vocab544-pytorch/summary"

    # 和train函数的输入参数对应，并且会对接显示到pipeline的模板参数中
    train_inputs = []

    # 和inference函数的输入参数对应，并且会对接显示到web界面上
    inference_inputs = [
        Field(type=Field_type.audio, name='input', label='音频',describe='音频',default='',validators=None)
    ]

    inference_resource = {
        "resource_gpu": "0"
    }
    # 会显示在web界面上，让用户作为示例输入
    web_examples=[
        {
            "label": "示例1",
            "input": {
                "input": "/mnt/workspace/.cache/modelscope/damo/speech_paraformer-tiny-commandword_asr_nat-zh-cn-16k-vocab544-pytorch/example/asr_example.wav"
            }
        }
    ]

    # 训练的入口函数，此函数会自动对接pipeline，将用户在web界面填写的参数传递给该方法
    def train(self,save_model_dir,arg1,arg2, **kwargs):
        pass
        # 训练的逻辑
        # 将模型保存到save_model_dir 指定的目录下


    # 加载模型，所有一次性的初始化工作可以放到该方法下。注意save_model_dir必须和训练函数导出的模型结构对应
    def load_model(self,save_model_dir=None,**kwargs):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        self.p = pipeline('auto-speech-recognition', 'damo/speech_paraformer-tiny-commandword_asr_nat-zh-cn-16k-vocab544-pytorch')

    # web每次用户请求推理，用于对接web界面请求
    @pysnooper.snoop(watch_explode=('result'))
    def inference(self,input,**kwargs):
        result = self.p(input)

        # 将结果保存到result目录下面，gitignore统一进行的忽略。并且在结果中注意添加随机数，避免多人访问时，结果混乱
        # 推理的返回结果只支持image，text，video，audio，html，markdown几种类型
        back = [
            {
                "text": result['text']
            }
        ]
        return back

model=SPEECH_PARAFORMER_TINY_COMMANDWORD_ASR_NAT_ZH_CN_16K_VOCAB544_PYTORCH_Model()


# 容器中调试训练时
# save_model_dir = "result"
# model.train(save_model_dir = save_model_dir,arg1=None,arg2=None)  # 测试

# 容器中运行调试推理时
# model.load_model(save_model_dir=None)
# result = model.inference(input='/mnt/workspace/.cache/modelscope/damo/speech_paraformer-tiny-commandword_asr_nat-zh-cn-16k-vocab544-pytorch/example/asr_example.wav')  # 测试
# print(result)

# 模型启动web时使用
if __name__=='__main__':
    model.run()