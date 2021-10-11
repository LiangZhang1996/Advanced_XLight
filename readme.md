## Introduction

Code for article "Pressure  is enough for traffic light control".

The code structure is based on  [MPLight](https://github.com/Chacha-Chen/MPLight.git).

### Quick start

For the method in our article, run:
```shell
python run_allpressure.py
```

For the baseline methods,
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
## Rquirements
`tensorflow=2.4`

## Code explaination
### structure
- `models`: contains all the models used in our article.
- `utils`: contains all the methods to simulate and train the network.

### quto
The `Max-Pressure` is created by ourselves, based on [MaxPressure](https://www.sciencedirect.com/science/article/pii/S0968090X13001782) .
- `PressLight`: Bsed on `LIT` model, which comes from [Colight](https://github.com/wingsweihua/colight.git).
- `Colight` : Based on [Colight](https://github.com/wingsweihua/colight.git).
- `Fixed-Time`: From [MPLight](https://github.com/Chacha-Chen/MPLight.git).
- `MPLight`: From [MPLight](https://github.com/Chacha-Chen/MPLight.git).

If you use our method, please cite our article.
