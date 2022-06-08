#!/bin/bash
set -ex

docker build -t ccr.ccs.tencentyun.com/cube-studio/tf2.3_model_template_mmoe:latest -f job/model_template/tf/mmoe/Dockerfile .
docker push ccr.ccs.tencentyun.com/cube-studio/tf2.3_model_template_mmoe:latest
