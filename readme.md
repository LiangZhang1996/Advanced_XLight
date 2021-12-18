## 1 Introduction

Code for article "Expression is enough: Improving traﬀic signal control with advanced traﬀic state representation".

The code structure is based on  [Efficient_XLight](https://github.com/LiangZhang1996/Efficient_XLight.git).

## 2 Requirements
`python3.6`,`tensorflow=2.4`, `cityflow`, `pandas`, `numpy`

[`cityflow`](https://github.com/cityflow-project/CityFlow.git) needs a linux environment, and we run the code on Manjaro Linux.

## 3 Usage

Parameters are well-prepared, and you can run the code directly.

Our proposed method:
- For `Advanced-MPLight`, run:
```shell
python run_advanced_mplight.py
```
- For `Advanced-CoLight`, run:
```shell
python run_advanced_colight.py
```

- For `Advanced-MP`, run:
```shell
python run_advanced_maxpressure.py
```


For the baseline methods:

- Efficient-PressLight
```shell
python run_efficient_presslight.py
```
- Efficient-CoLight
```shell
python run_efficient_colight.py
```
- Efficient-MPLight`
```shell
python run_efficient_mplight.py
```
- Fixed-Time
```shell
python run_fixedtime.py
```
- Max-Pressure
```shell
python run_maxpressure.py
```
- PressLight
```shell
python run_presslight.py
```
- MPLight
```shell
python run_mplight.py
```
- Colight
```shell
python run_colight.py
```
## 4、Code details
### 4.1、structure
- `models`: contains all the models used in our article.
- `utils`: contains all the methods to simulate and train the models.

### 4.2、Reference

The code is modified from [Efficient_XLight](https://github.com/LiangZhang1996/Efficient_XLight.git).
The `Max-Pressure` is created by ourselves, based on [MaxPressure](https://www.sciencedirect.com/science/article/pii/S0968090X13001782) .
- `PressLight`: Bsed on `LIT` model, which comes from [Colight](https://github.com/wingsweihua/colight.git).
- `Colight` : Based on [Colight](https://github.com/wingsweihua/colight.git).
- `Fixed-Time`: From [MPLight](https://github.com/Chacha-Chen/MPLight.git).
- `MPLight`: From [MPLight](https://github.com/Chacha-Chen/MPLight.git).

If you use our method, please cite our article.
