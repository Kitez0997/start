# BERT-BiLSTM-CRF模型

### 输入数据格式请处理成BIO格式，如下：
```
彭	B-name
小	I-name
军	I-name
认	O
为	O
，	O
国	O
内	O
银	O
行	O
现	O
在	O
走	O
的	O
是	O
台	B-address
湾	I-address

温	B-name
格	I-name
的	O
球	O
队	O
终	O
于	O
```

### 运行的环境
```
python == 3.7.4
pytorch == 1.3.1 
pytorch-crf == 0.7.2  
pytorch-transformers == 1.2.0               
```

### 使用方法
```
BERT_BASE_DIR=bert-base-chinese
DATA_DIR=/raid/ypj/openSource/cluener_public/
OUTPUT_DIR=./model/clue_bilstm
export CUDA_VISIBLE_DEVICES=0

python ner.py \
    --model_name_or_path ${BERT_BASE_DIR} \
    --do_train True \
    --do_eval True \
    --do_test True \
    --max_seq_length 256 \
    --train_file ${DATA_DIR}/train.txt \
    --eval_file ${DATA_DIR}/dev.txt \
    --test_file ${DATA_DIR}/test.txt \
    --train_batch_size 32 \
    --eval_batch_size 32 \
    --num_train_epochs 10 \
    --do_lower_case \
    --logging_steps 200 \
    --need_birnn True \
    --rnn_dim 256 \
    --clean True \
    --output_dir $OUTPUT_DIR
```

### 在法律文书数据集上

完整数据集见https://git.ustc.edu.cn/wao/informationextraction/-/tree/Sewell_Leung/Data

### 数据集预处理部分

1.只针对原告被告两种类型进行了处理，每个answer中有四个字段{context,start_pos,end_pos,type},对于type进行判断,DICT = ["纠纷当事人_被告","纠纷当事人_原告"]，（没有对下一级进行判断，也没有对其他的type进行判断）

2.为了制作数据集，不仅需要实体的内容，还需要构造实体内容的上下文。start_pos和end_pos代表实体在文本中的位置，所以根据全文本获取到上下文，考虑使用随机数5~10对文本进行上下文补长

3.data_preprocess过程中把原始数据集处理为统一的可利用格式，用于生成后面的数据集，其中train:dev:test=8:1:1

      训练集，验证集格式如下:{"text": "第271号\n原告:严增路，男，1955", "label": {"plaintiff": {"严增路": [[9, 11]]}}}
      对于测试集，删除了文本中的\n,\t符号，格式：{"id": 0, "text": "4号原告：谢洪梅。委托代理人"}

### 结果
processed 6804 tokens with 386 phrases; found: 430 phrases; correct: 376.
accuracy:  98.05%; precision:  87.44%; recall:  97.41%; FB1:  92.16
        defendant: precision:  79.76%; recall:  94.37%; FB1:  86.45  168
        plaintiff: precision:  92.37%; recall:  99.18%; FB1:  95.65  262


### 在中文CLUENER2020的eval集上的结果
#### 数据集
https://github.com/CLUEbenchmark/CLUENER2020
#### BERT-CRF
```
processed 50260 tokens with 3072 phrases; found: 3363 phrases; correct: 2457.
accuracy:  94.08%; precision:  73.06%; recall:  79.98%; FB1:  76.36
          address: precision:  54.63%; recall:  63.27%; FB1:  58.63  432
             book: precision:  77.02%; recall:  80.52%; FB1:  78.73  161
          company: precision:  72.58%; recall:  81.22%; FB1:  76.65  423
             game: precision:  78.27%; recall:  89.15%; FB1:  83.36  336
       government: precision:  75.36%; recall:  85.43%; FB1:  80.08  280
            movie: precision:  82.19%; recall:  79.47%; FB1:  80.81  146
             name: precision:  84.35%; recall:  89.25%; FB1:  86.73  492
     organization: precision:  71.15%; recall:  79.29%; FB1:  75.00  409
         position: precision:  74.46%; recall:  79.45%; FB1:  76.87  462
            scene: precision:  65.77%; recall:  69.86%; FB1:  67.75  222
```
#### BERT-BiLSTM-CRF
```
processed 50260 tokens with 3072 phrases; found: 3293 phrases; correct: 2463.
accuracy:  94.10%; precision:  74.80%; recall:  80.18%; FB1:  77.39
          address: precision:  55.40%; recall:  63.27%; FB1:  59.07  426
             book: precision:  76.54%; recall:  80.52%; FB1:  78.48  162
          company: precision:  76.05%; recall:  81.48%; FB1:  78.67  405
             game: precision:  77.95%; recall:  87.46%; FB1:  82.43  331
       government: precision:  75.00%; recall:  85.02%; FB1:  79.70  280
            movie: precision:  84.00%; recall:  83.44%; FB1:  83.72  150
             name: precision:  85.29%; recall:  87.31%; FB1:  86.29  476
     organization: precision:  76.76%; recall:  80.11%; FB1:  78.40  383
         position: precision:  75.58%; recall:  82.22%; FB1:  78.76  471
            scene: precision:  69.38%; recall:  69.38%; FB1:  69.38  209

```
### 