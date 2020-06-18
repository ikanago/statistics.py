# Statistics.py

初歩的な統計的推定・検定を簡単に実行できるツールです．ところで名前が`Statistics`なのは主張が強すぎるかもしれません．

## 機能
### 推定
* 平均値の区間推定(母分散既知)
* 平均値の区間推定(母分散未知)
* 母分散の区間推定

## 使い方
まずCSVファイルに対象となるデータを書き込んでおきます．
```
6.0, 8.5, 4.1, 4.9, 5.2, 7.1
```

### 基本的な統計量(descrive)
データ数・標本平均・標本分散・不偏分散を算出して表示します．
```
$ python main.py desc -f test.csv
データ数: 6
標本平均: 5.966666666666666
標本分散: 2.1522222222222216
不偏分散: 2.582666666666666
```
ファイルを指定しない場合は`data.csv`を読みにいきます．

### 推定(estimate)
なにも指定しなくても推定は3種類同時に行います．
```
$ python main.py est -p 5.0 -c 0.95
母平均の95%信頼区間(母分散既知): [ 4.177472522949508, 7.755860810383823 ]
母平均の95%信頼区間(母分散未知): [ 4.280152521665077, 7.653180811668255 ]
母分散の95%信頼区間          : [ 1.0062989539639977, 15.53555451320764 ]
```
`-p`オプションは既知の母分散を指定します．省略すると母分散既知の母平均推定は行われません．
また，`-c`オプションは信頼係数です．省略すると`0.95`にセットされます．
