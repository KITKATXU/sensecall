import os


cmd = 'python run_classifier.py   --task_name=qgfl   --do_predict=true   --data_dir=$DATA_DIR   --vocab_file=$BERT_BASE_DIR/vocab.txt   --bert_config_file=$BERT_BASE_DIR/bert_config.json   --init_checkpoint=$TRAINED_CLASSIFIER   --max_seq_length=512   --output_dir=./mymodel'
os.system(cmd)
cmd = 'python get_results.py'
os.system(cmd)