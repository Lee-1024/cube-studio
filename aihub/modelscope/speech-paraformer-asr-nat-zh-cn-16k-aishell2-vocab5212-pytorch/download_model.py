

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline('auto-speech-recognition', 'damo/speech_paraformer_asr_nat-zh-cn-16k-aishell2-vocab5212-pytorch')