

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline('face-detection', 'damo/cv_manual_face-detection_tinymog')