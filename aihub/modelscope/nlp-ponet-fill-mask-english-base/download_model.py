

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline('fill-mask', 'damo/nlp_ponet_fill-mask_english-base')