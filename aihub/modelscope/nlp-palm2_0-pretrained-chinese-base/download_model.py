

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline('text-generation', 'damo/nlp_palm2.0_pretrained_chinese-base')