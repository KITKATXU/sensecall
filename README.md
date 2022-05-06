# sensecall
```

# Setup

All code were developed and tested on pycharm with Python 3.10, and were implemented by tensorflow 2.8.0

You can create a conda environment and set up SenseCall like this:

```
conda create -n sensecall python=3.10 scipy pyyaml jupyter matplotlib
source activate sensecall
conda install tensorflow=2.8.0
git clone git@github.com:KITKATXU/sensecall.git
cd sensecall
git checkout sensecall # switch your branch from 'master' to the 'sensecall'
git submodule init
git submodule update
```


# Training, Testing

| Model                | example of config file              | training & testing          | 
| ---                  | ---                                 | ---                         | 
| qgfl_model           | model.ckpt-0.data-00000-of-00001    | run_classifier.py           |  



## Training
```
python run_classifier.py --task_name=qgfl --do_train=true --do_eval=true --do_predict=false --data_dir=../toutiao-text-classfication-dataset-master  --task_name=qgfl  --vocab_file=../chinese_L-12_H-768_A-12/vocab.txt  --bert_config_file=../chinese_L-12_H-768_A-12\bert_config.json  --output_dir=qgfl_model  --do_train=true  --do_eval=true  --init_checkpoint=../chinese_L-12_H-768_A-12/bert_model.ckpt  --max_seq_length=150  --train_batch_size=32  --learning_rate=5e-5  --num_train_epochs=1
```
Training information and learned parameters will be stored in `qgfl_model/${TASKDESCRIPTOR}`.

## Testing
```
python run_classifier.py   --task_name=qgfl   --do_predict=true   --data_dir=$DATA_DIR   --vocab_file=$BERT_BASE_DIR/vocab.tx
t   --bert_config_file=$BERT_BASE_DIR/bert_config.json   --init_checkpoint=$TRAINED_CLASSIFIER   --max_seq_length=512   --output_dir=./mymodel
```
Then the testing results will be stored in `mymodel/pre_sample.csv`. 

## Show Results
Set your TASKDESCRIPTOR in `run_classifier.py` and run.


[Download pretrained models](https://gitlab.com/ZichaoLong/PDE-Net-Checkpoints) and make your working directory like this:
```
PDE-Net/
  aTEAM/
  figures/
  learn_variantcoelinear2d.py
  linpdetest.py
  ...
  checkpoint/
      linpde5x5frozen4order0.015dt0.015noise-double/
      linpde5x5moment4order0.015dt0.015noise-double/
      linpde7x7frozen4order0.015dt0.015noise-double/
      linpde7x7moment4order0.015dt0.015noise-double/
      nonlinpde7x7frozen2order-double/
      nonlinpde7x7moment2order-double/
```

