

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline('image-segmentation', 'damo/cv_segformer-b1_image_semantic-segmentation_coco-stuff164k')