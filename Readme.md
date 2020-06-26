# Statistics.py

![Unit test](https://github.com/ikanago/statistics.py/workflows/Unit%20test/badge.svg)

初歩的な統計的推定・検定を簡単に実行できるツール．

## 機能
### 推定
* 平均値の区間推定(母分散既知)
* 平均値の区間推定(母分散未知)
* 母分散の区間推定

### 検定
* 平均
* 平均の差
* 分散
* 分散比

## 使い方
まずCSVファイルに対象となる標本を書き込んでおく(検定を行う場合で，必要な統計量が既知の場合は不要)．
```
6.0, 8.5, 4.1, 4.9, 5.2, 7.1
```

### 基本的な統計量(descrive)
標本数・標本平均・標本分散・不偏分散を算出して表示する．
```
$ python main.py desc -f test.csv
系列1
標本数: 6
標本平均: 5.966666666666666
標本分散: 2.1522222222222216
不偏分散: 2.582666666666666
```
ファイルを指定しない場合は`data.csv`を読みにいく．

CSVファイルに複数行に分けて標本を記録すると，各行ごとに計算を行う．
```
$ python describe.py -f test.csv
系列1
標本数: 6
標本平均: 5.966666666666666
標本分散: 2.1522222222222216
不偏分散: 2.582666666666666

系列2
標本数: 8
標本平均: 4.2
標本分散: 2.8125
不偏分散: 3.2142857142857144
```

### 推定
なにも指定しなくても推定は3種類同時に行われる．
```
python estimation.py --help
Usage: estimation.py [OPTIONS]

Options:
  -f, --file PATH
  -p, --pop_variance FLOAT  既知の母分散
  -c, --confidence FLOAT    信頼係数(default: 0.95)
  --help                    Show this message and exit.
```
```
$ python estimation.py -p 5.0 -c 0.95
系列1
母平均の95%信頼区間(母分散既知): [ 4.177472522949508, 7.755860810383823 ]
母平均の95%信頼区間(母分散未知): [ 4.280152521665077, 7.653180811668255 ]
母分散の95%信頼区間          : [ 1.0062989539639977, 15.53555451320764 ]
```
`-p`を省略すると母分散既知の母平均推定は行われない．
```
$ python estimation.py -c 0.95
系列1
母平均の95%信頼区間(母分散未知): [ 4.280152521665077, 7.653180811668255 ]
母分散の95%信頼区間          : [ 1.0062989539639977, 15.53555451320764 ]
```

### 検定
#### 平均の検定
帰無仮説 H_0: `μ = μ_0`の検定を行う．  
```
python stats_test_mean.py --help
Usage: stats_test_mean.py [OPTIONS]

Options:
  -z, --z_test                    既知の母分散を使うかどうか
  -n INTEGER                      標本の大きさ
  -h, --hypothesis FLOAT          帰無仮説で等しいと仮定する平均
  -m, --mean FLOAT                標本平均
  -vr, --variance FLOAT           既知の母分散/標本分散
  -sd, --stdev FLOAT              既知の母標準偏差/標本標準偏差
  -l, --level FLOAT               有意水準(default: 0.05)
  -s, --side [double|left|right]  検定方法(両側，左片側，右片側)
  --help                          Show this message and exit.
```
`-vr`と`-sd`はどちらか一方を指定すればよい．  
母分散既知の場合は正規分布を使用する．オプションとして`-z`をつけて実行する:
```
$ python stats_test_mean.py -z -n 30 -h 60 -m 56.75 -sd 15
実現値: -1.18673220792786
帰無仮説 μ = 60.0 は採択されました
```
母分散未知の場合はt分布を使用する:
```
$ python stats_test_mean.py -n 10 -h 12 -m 12.36 -vr 0.910
実現値: 1.13214762365967
帰無仮説 μ = 12.0 は採択されました
```

### 平均の差の検定
帰無仮説 H_0: `μ_1 = μ_2`の検定を行う．
```
$ python stats_test_mean_diff.py --help
Usage: stats_test_mean_diff.py [OPTIONS]

Options:
  -z, --z_test             既知の母分散を使うかどうか
  -b, --big_sample         サンプル数が十分大きいとみなして正規分布を使うかどうか
  -n1 INTEGER              1つめの標本の標本の大きさ
  -m1, --mean1 FLOAT       1つめの標本の標本平均
  -vr1, --variance1 FLOAT  1つめの標本の既知の母分散/標本分散
  -sd1, --stdev1 FLOAT     1つめの標本の既知の母標準偏差/標本標準偏差
  -n2 INTEGER              2つめの標本の標本の大きさ
  -m2, --mean2 FLOAT       2つめの標本の標本平均
  -vr2, --variance2 FLOAT  2つめの標本の既知の母分散/標本分散
  -sd2, --stdev2 FLOAT     2つめの標本の既知の母標準偏差/標本標準偏差
  -l, --level FLOAT        有意水準(default: 0.05)
  --help                   Show this message and exit.
```
標準偏差と分散のオプションはどちらか一方を指定すればよい．  
母分散既知の場合は正規分布を使用する．オプションとして`-z`をつけて実行する:
```
$ python stats_test_mean_diff.py -z -n1 40 -m1 103 -sd1 15 -n2 35 -m2 101 -sd2 15
実現値: 0.5760658398584765
帰無仮説 μ1 = μ2 は採択されました
```
母分散未知で分散が等しいとみなせる場合はt分布を使用する:
```
$ python stats_test_mean_diff.py -n1 15 -m1 68.4 -sd1 10.2 -n2 21 -m2 64.3 -sd2 9.3
実現値: 1.2169392110479802
帰無仮説 μ1 = μ2 は採択されました
```
母分散未知でサンプル数が十分に大きい場合は正規分布を使用する．オプションとして`-b`をつけて実行する:
```
$ python stats_test_mean_diff.py -b -n1 120 -m1 83.2 -sd1 16.8 -n2 90 -m2 74.5 -sd2 12.5
実現値: 4.282347279436892
帰無仮説 μ1 = μ2 は棄却されました
```

### 分散の検定
帰無仮説 H_0: `σ^2 = σ_0^2`の検定を行う．
```
$ python stats_test_var.py --help
Usage: stats_test_var.py [OPTIONS]

Options:
  -n INTEGER              標本の大きさ
  -h, --hypothesis FLOAT  帰無仮説で等しいと仮定する分散
  -vr, --variance FLOAT   標本分散
  -sd, --stdev FLOAT      標本標準偏差
  -l, --level FLOAT       有意水準(default: 0.05)
  --help                  Show this message and exit.
```
標準偏差と分散のオプションはどちらか一方を指定すればよい．  
カイ二乗分布を使用する:
```
$ python stats_test_var.py -n 10 -h 0.09 -vr 0.108 
実現値: 12.000000000000002
帰無仮説 σ = 0.09 は採択されました
```

### 分散比の検定
帰無仮説 H_0: `σ_1^2 = σ_2^2`の検定を行う．
```
$ python stats_test_var_ratio.py --help 
Usage: stats_test_var_ratio.py [OPTIONS]

Options:
  -n1 INTEGER              1つめの標本の標本の大きさ
  -vr1, --variance1 FLOAT  1つめの標本の標本分散
  -sd1, --stdev1 FLOAT     1つめの標本の標本標準偏差
  -n2 INTEGER              2つめの標本の標本の大きさ
  -vr2, --variance2 FLOAT  2つめの標本の標本分散
  -sd2, --stdev2 FLOAT     2つめの標本の標本標準偏差
  -l, --level FLOAT        有意水準(default: 0.05)
  --help                   Show this message and exit.
```
標準偏差と分散のオプションはどちらか一方を指定すればよい．  
F分布を使用する:
```
python stats_test_var_ratio.py -n1 10 -vr1 8.8 -n2 8 -vr2 10.1 -l 0.10
実現値: 0.8470847084708472
帰無仮説 σ1 = σ2 は採択されました
```

### 相関係数の検定
帰無仮説 H_0: `ρ = ρ_0`の検定を行う．
```
$ python stats_test_correl.py --help
Usage: stats_test_correl.py [OPTIONS]

Options:
  -n INTEGER              標本の大きさ
  -h, --hypothesis FLOAT  帰無仮説で等しいと仮定する相関係数
  -r FLOAT                標本相関係数
  -l, --level FLOAT       有意水準(default: 0.05)
  --help                  Show this message and exit.
```
正規分布を使用する．
```
$ python stats_test_correl.py -n 48 -h 0.7 -r 0.648
実現値: -0.640346768650969
帰無仮説 r = 0.7 は採択されました
```
`-h`を指定しない，あるいは0を指定した場合は無相関の検定を行う:
```
python stats_test_correl.py -n 25 -r 0.352
実現値: 1.8035605728697404
帰無仮説 r = 0.0 は採択されました
```

### 相関係数の差の検定
帰無仮説 H_0: `ρ_1 = ρ_2`の検定を行う．
```
$ python stats_test_correl_diff.py --help
Usage: stats_test_correl_diff.py [OPTIONS]

Options:
  -n1 INTEGER        1つめの標本の大きさ
  -n2 INTEGER        2つめの標本の大きさ
  -r1 FLOAT          1つめの標本の標本相関係数
  -r2 FLOAT          2つめの標本の標本相関係数
  -l, --level FLOAT  有意水準(default: 0.05)
  --help             Show this message and exit.
```
正規分布を使用する．
```
$ python stats_test_correl_diff.py -n1 80 -n2 65 -r1 0.538 -r2 0.743
実現値: -2.08520190531367
帰無仮説 r1 = r2 は棄却されました
```
