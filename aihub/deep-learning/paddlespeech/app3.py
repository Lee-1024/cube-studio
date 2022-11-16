import base64
import io, sys, os
from cubestudio.aihub.model import Model
from cubestudio.aihub.docker import Docker
from cubestudio.aihub.web.server import Server, Field, Field_type
import pysnooper
from paddlespeech.cli.cls.infer import CLSExecutor


class Speech_Cls_Model(Model):
    # 模型基础信息定义
    name = 'paddle-speech'
    label = '语音场景分类'
    describe = "涵盖功能有语音转文字，文字转语音，语音翻译，语音场景识别"
    field = "智能识别"
    scenes = "语音处理"
    status = 'online'
    version = 'v20221114'
    doc = 'https://github.com/PaddlePaddle/PaddleSpeech'  # 'https://帮助文档的链接地址'
    # pic = 'https://images.nightcafe.studio//assets/stable-tile.jpg'  # https://应用描述的缩略图/可以直接使用应用内的图片文件地址

    inference_resource = {
        "resource_gpu": "1"
    }

    inference_inputs = [
        Field(type=Field_type.audio, name='voice_file_path', label='语音文件',
              describe='上传一个语音文件吧~'),
    ]
    web_examples = [
        {
            "label": "示例1",
            "input": {
                "voice_file_path": "a.wav"
            }
        }
    ]

    def __init__(self):
        self.cls = None

    # 加载模型
    # @pysnooper.snoop()
    def load_model(self):
        self.cls = CLSExecutor()  # 语音分类

    # 推理
    @pysnooper.snoop()
    def inference(self, voice_file_path):
        cls = self.cls
        result = '语音分类结果： '
        an_result = cls(audio_file=voice_file_path)
        result += an_result.split(' ')[0] + '  ' + '置信度：' + an_result.split(' ')[1]
        back = [
            {
                'text': result
            }
        ]
        return back


model = Speech_Cls_Model()
#model.load_model()
#result = model.inference('zh.wav')  # 测试
#print(result)

# 启动服务
server = Server(model=model)
server.server(port=8080)
