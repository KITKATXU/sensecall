export BERT_BASE_DIR=./chinese_L-12_H-768_A-12
export DATA_DIR=./mymodel
export ./mymodel
# TRAINED_CLASSIFIER为刚刚训练的输出目录，无需在进一步指定模型名称，否则分类结果会不对
 
python3 run_classifier.py \
  --task_name=chi \
  --do_predict=true \
  --data_dir=$DATA_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$TRAINED_CLASSIFIER \
  --max_seq_length=512 \
  --output_dir=./mymodel
