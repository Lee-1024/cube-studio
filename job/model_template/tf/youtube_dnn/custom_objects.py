# coding=utf-8
# @Time     : 2021/1/25 18:50
# @Auther   : lionpeng@tencent.com
from abc import ABC

from job.pkgs.tf.extend_layers import *
from job.pkgs.tf.feature_util import *
from job.model_template.tf.youtube_dnn.model import YoutubeDNNModel


class SampledSoftmaxLoss(tf.keras.losses.Loss, ABC):
    def __init__(self, model: YoutubeDNNModel, num_samples, num_classes, sample_algo=None,
                 sample_algo_params=None, name="sampled_softmax_loss"):
        super(SampledSoftmaxLoss, self).__init__(name=name)
        self.model = model
        self.num_samples = num_samples
        self.num_classes = num_classes
        self.biases = tf.zeros([num_classes])
        self.sampler_func_args = {}
        if isinstance(sample_algo, str) and sample_algo.strip():
            sample_algo = sample_algo.strip().lower()
            if sample_algo == 'uniform':
                self.sampler_func = tf.random.uniform_candidate_sampler
            elif sample_algo == 'log_uniform':
                self.sampler_func = tf.random.log_uniform_candidate_sampler
            elif sample_algo == 'learned':
                self.sampler_func = tf.random.learned_unigram_candidate_sampler
            elif sample_algo == 'fixed':
                self.sampler_func = tf.random.fixed_unigram_candidate_sampler
                if not isinstance(sample_algo_params, dict) or not sample_algo_params or \
                        ('vocab_file' not in sample_algo_params and 'unigrams' not in sample_algo_params):
                    raise RuntimeError("must provide args for 'fixed' sample algorithm, mandatory args: "
                                       "'vocab_file'(or 'unigrams'), optional args: 'distortion', 'num_reserved_ids'")
                if 'unigrams' in sample_algo_params:
                    unigrams = sample_algo_params['unigrams']
                    if not isinstance(unigrams, list) or not all([isinstance(i, (int, float)) for i in unigrams]):
                        raise RuntimeError("'unigrams' should be of list of int/float, got '{}': {}"
                                           .format(type(unigrams), unigrams))
                    self.sampler_func_args.update({"unigrams": unigrams})
                else:
                    vocab_file = sample_algo_params['vocab_file']
                    if not isinstance(vocab_file, str) or not vocab_file.strip():
                        raise RuntimeError("'vocab_file' should be a non-empty file path, got '{}': {}"
                                           .format(type(vocab_file), vocab_file))
                    if not os.path.isfile(vocab_file):
                        raise RuntimeError("'vocab_file' '{}' is not a valid file".format(vocab_file))
                    self.sampler_func_args.update({"vocab_file": vocab_file})
                if 'distortion' in sample_algo_params and isinstance(sample_algo_params['distortion'], (int, float)):
                    self.sampler_func_args.update({"distortion": sample_algo_params['distortion']})
                if 'num_reserved_ids' in sample_algo_params and isinstance(sample_algo_params['num_reserved_ids'], int):
                    self.sampler_func_args.update({"num_reserved_ids": sample_algo_params['num_reserved_ids']})
            else:
                raise RuntimeError("unknown sampler algorithm '{}', supported are: 'uniform', 'log_uniform',"
                                   " 'learned', 'fixed'".format(sample_algo))
        else:
            self.sampler_func = tf.random.learned_unigram_candidate_sampler

        print("sampler_func: {}".format(self.sampler_func))
        print("sampler_func_args: {}".format(self.sampler_func_args))

    @tf.function
    def call(self, y_true, y_pred):
        weights = self.model.get_item_embedding_weights()
        y_true_indices = self.model.lookup_item_index(y_true)
        sampled_values = self.sampler_func(y_true_indices, 1, self.num_samples, True, self.num_classes,
                                           **self.sampler_func_args)
        loss = tf.nn.sampled_softmax_loss(weights=weights,
                                          biases=self.biases, labels=y_true_indices, inputs=y_pred,
                                          num_sampled=self.num_samples, num_classes=self.num_classes,
                                          sampled_values=sampled_values)
        return tf.reduce_mean(loss)


class TopKHitrate(tf.keras.metrics.SparseTopKCategoricalAccuracy):
    def __init__(self, model: YoutubeDNNModel, num_classes, k, name="topk_hitrate", dtype=None):
        super(TopKHitrate, self).__init__(k, name=name, dtype=dtype)
        self.model = model
        self.num_classes = num_classes

    @tf.function
    def update_state(self, y_true, y_pred, sample_weight=None):
        # [batch, 1]
        y_true_indices = self.model.lookup_item_index(y_true)
        # [num_classes, dim]
        weights = self.model.get_item_embedding_weights()

        # [batch, num_classes]
        pred_classes = tf.matmul(y_pred, weights, transpose_b=True, name=self.name+'_yp_matmul_iw')
        return super(TopKHitrate, self).update_state(y_true_indices, pred_classes, sample_weight)

    def reset_states(self):
        self.count.assign(0)
        self.total.assign(0)

    def get_config(self):
        config = super(TopKHitrate, self).get_config()
        config.update({
            'model': None,
            'num_classes': self.num_classes
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


custom_objects = {
    'tf': tf,
    'InputDesc': InputDesc,
    'FeatureProcessDesc': FeatureProcessDesc,
    'ModelInputConfig': ModelInputConfig,
    'VocabLookupLayer': VocabLookupLayer,
    'PoolingEmbeddingLayer': PoolingEmbeddingLayer,
    'VocabEmbeddingLayer': VocabEmbeddingLayer,
    'VocabMultiHotLayer': VocabMultiHotLayer,
    'ModelInputLayer': ModelInputLayer,
    'DNNLayer': DNNLayer,
    'BucktizeLayer': BucktizeLayer,
    'SampledSoftmaxLoss': SampledSoftmaxLoss,
    'TopKCategoricalAccuracy': tf.keras.metrics.TopKCategoricalAccuracy,
    'TopKHitrate': TopKHitrate,
    'YoutubeDNNModel': YoutubeDNNModel
}
