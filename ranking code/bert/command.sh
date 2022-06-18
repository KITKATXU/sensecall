export BERT_BASE_DIR=./chinese_L-12_H-768_A-12#这里是存放中文模型的路径
export DATA_DIR=../toutiao-text-classfication-dataset-master  #这里是存放数据的路径
 
python run_classifier.py --task_name=my --do_train=true --do_eval=true --do_predict=false --data_dir=$DATA_DIR  --vocab_file=$BERT_BASE_DIR/vocab.txt --bert_config_file=$BERT_BASE_DIR/bert_config.json --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt  --max_seq_length=512 --train_batch_size=4 --learning_rate=2e-5 --num_train_epochs=15 --output_dir=./mymodel 

python run_classifier.py   --task_name=qgfl   --do_predict=true   --data_dir=$DATA_DIR   --vocab_file=$BERT_BASE_DIR/vocab.txt   --bert_config_file=$BERT_BASE_DIR/bert_config.json   --init_checkpoint=$TRAINED_CLASSIFIER   --max_seq_length=512   --output_dir=./mymodel



