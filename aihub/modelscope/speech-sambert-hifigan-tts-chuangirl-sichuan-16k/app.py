import base64
import io,sys,os
from cubestudio.aihub.model import Model,Validator,Field_type,Field

import pysnooper
import os

class SPEECH_SAMBERT_HIFIGAN_TTS_CHUANGIRL_SICHUAN_16K_Model(Model):
    # 模型基础信息定义
    name='speech-sambert-hifigan-tts-chuangirl-sichuan-16k'   # 该名称与目录名必须一样，小写
    label='语音合成-四川话-通用领域-16k-发音人chuangirl'
    describe="四川话语音合成女声16k模型，本模型使用Sambert-hifigan网络结构。其中后端声学模型的SAM-BERT,将时长模型和声学模型联合进行建模。声码器在HIFI-GAN开源工作的基础上，我们针对16k, 48k采样率下的模型结构进行了调优设计，并提供了基于因果卷积的低时延流式生成和chunk流式生成机制，可与声学模型配合支持CPU、GPU等硬件条件下的实时流式合成。"
    field="听觉"    # [机器视觉，听觉，自然语言，多模态，强化学习，图论]
    scenes=""
    status='online'
    version='v20221001'
    pic='example.jpg'  # 离线图片，作为模型的样式图，330*180尺寸比例
    hot = "1688"
    frameworks = "pytorch"
    doc = "https://modelscope.cn/models/speech_tts/speech_sambert-hifigan_tts_chuangirl_Sichuan_16k/summary"

    # 和train函数的输入参数对应，并且会对接显示到pipeline的模板参数中
    train_inputs = []

    # 和inference函数的输入参数对应，并且会对接显示到web界面上
    inference_inputs = [
        Field(type=Field_type.text, name='input', label='文本',describe='文本',default='',validators=Validator(max=300))
    ]

    inference_resource = {
        "resource_gpu": "1"
    }
    # 会显示在web界面上，让用户作为示例输入
    web_examples=[
        {
            "label": "示例1",
            "input": {
                "input": "北京今天天气怎么样"
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
        
        self.p = pipeline('text-to-speech', 'speech_tts/speech_sambert-hifigan_tts_chuangirl_Sichuan_16k')

    # rtsp流的推理,输入为cv2 img,输出也为处理后的cv2 img
    def rtsp_inference(self,img:numpy.ndarray,**kwargs)->numpy.ndarray:
        return img

    # web每次用户请求推理，用于对接web界面请求
    @pysnooper.snoop(watch_explode=('result'))
    def inference(self,input,**kwargs):
        result = self.p(input)

        # 将结果保存到result目录下面，gitignore统一进行的忽略。并且在结果中注意添加随机数，避免多人访问时，结果混乱
        # 推理的返回结果只支持image，text，video，audio，html，markdown几种类型
        back=[
            {
                "image": 'result/aa.jpg',
                "text": '结果文本',
                "video": 'result/aa.mp4',
                "audio": 'result/aa.mp3',
                "markdown":''
            }
        ]
        return back

model=SPEECH_SAMBERT_HIFIGAN_TTS_CHUANGIRL_SICHUAN_16K_Model()


# 容器中调试训练时
# save_model_dir = "result"
# model.train(save_model_dir = save_model_dir,arg1=None,arg2=None)  # 测试

# 容器中运行调试推理时
model.load_model(save_model_dir=None)
result = model.inference(input='北京今天天气怎么样')  # 测试
print(result)

# # 模型启动web时使用
# if __name__=='__main__':
#     model.run()