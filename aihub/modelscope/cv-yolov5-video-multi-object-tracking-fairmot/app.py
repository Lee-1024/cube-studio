import base64
import io,sys,os
from cubestudio.aihub.model import Model,Validator,Field_type,Field
import numpy
import pysnooper
import random
import os
from modelscope.utils.constant import Tasks
from modelscope.models.cv.video_multi_object_tracking.utils.visualization import show_multi_object_tracking_result
from modelscope.outputs import OutputKeys

class CV_YOLOV5_VIDEO_MULTI_OBJECT_TRACKING_FAIRMOT_Model(Model):
    # 模型基础信息定义
    name='cv-yolov5-video-multi-object-tracking-fairmot'   # 该名称与目录名必须一样，小写
    label='视频多目标跟踪-行人'
    describe="该模型采用基于FairMOT的方案，输入待跟踪视频，可端对端推理得到视频中的所有行人的运动轨迹。"
    field="机器视觉"    # [机器视觉，听觉，自然语言，多模态，强化学习，图论]
    scenes=""
    status='online'
    version='v20221001'
    pic='example.png'  # 离线图片，作为模型的样式图，330*180尺寸比例
    hot = "518"
    frameworks = "pytorch"
    doc = "https://modelscope.cn/models/damo/cv_yolov5_video-multi-object-tracking_fairmot/summary"

    # 和train函数的输入参数对应，并且会对接显示到pipeline的模板参数中
    train_inputs = []

    # 和inference函数的输入参数对应，并且会对接显示到web界面上
    inference_inputs = [
        Field(type=Field_type.video, name='video', label='',describe='',default='',validators=None)
    ]

    inference_resource = {
        "resource_gpu": "0"
    }
    # 会显示在web界面上，让用户作为示例输入
    web_examples=[
        {
            "label": "示例0",
            "input": {
                "video": "http://dmshared.oss-cn-hangzhou.aliyuncs.com/ljp/maas/mot_demo_resource/MOT17-03-partial.mp4?OSSAccessKeyId=LTAI5tC7NViXtQKpxFUpxd3a&Expires=2032715547&Signature=ROPQRkeOJqE3j8cBC0PEtkgdlzs%3D"
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
        
        self.p = pipeline('video-multi-object-tracking', 'damo/cv_yolov5_video-multi-object-tracking_fairmot')

    # rtsp流的推理,输入为cv2 img,输出也为处理后的cv2 img
    def rtsp_inference(self,img:numpy.ndarray,**kwargs)->numpy.ndarray:
        return img

    # web每次用户请求推理，用于对接web界面请求
    @pysnooper.snoop(watch_explode=('result'))
    def inference(self,video,**kwargs):
        result = self.p(video)
        save_path = f'result/result{random.randint(1, 1000)}.mp4'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if os.path.exists(save_path):
            os.remove(save_path)
        show_multi_object_tracking_result(video, result[OutputKeys.BOXES], result[OutputKeys.LABELS], save_path)
        back=[
            {
                #"text": str(result),
                "video": save_path,
            }
        ]
        return back

model=CV_YOLOV5_VIDEO_MULTI_OBJECT_TRACKING_FAIRMOT_Model()


# 容器中调试训练时
# save_model_dir = "result"
# model.train(save_model_dir = save_model_dir,arg1=None,arg2=None)  # 测试

# 容器中运行调试推理时
# model.load_model(save_model_dir=None)
# result = model.inference(video='http://dmshared.oss-cn-hangzhou.aliyuncs.com/ljp/maas/mot_demo_resource/MOT17-03-partial.mp4?OSSAccessKeyId=LTAI5tC7NViXtQKpxFUpxd3a&Expires=2032715547&Signature=ROPQRkeOJqE3j8cBC0PEtkgdlzs%3D')  # 测试
# print(result)

# # 模型启动web时使用
if __name__=='__main__':
    model.run()

# 模型大小：160MB
# 模型效果：近距离识别率较高
# 推理性能: 4s以内
# 模型占用内存/推理服务占用内存/gpu占用显存：10MB/2.5G/1.4GB
# 巧妙使用方法：第一次调用后，后面推理速度会加快