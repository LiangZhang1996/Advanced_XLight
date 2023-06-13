## 1 Introduction

Official code for article "Expression might be enough: representing pressure and demand for reinforcement learning based traffic signal control".

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
### 3.1 Newly added baseline
We newly added two methods(AttendLight and PRGLight) as the basline.
#### PRGLight
The official code is avaliable at https://github.com/guang0123/PRGLight.git.
#### AttendLight
- For AttendLight, the officical code is not avaliable and we realized it according to their article. But, our-realized is not exactly the same as article described. We would like to run AttendLight in a DQN approach, but it is designed for Actor-Critic framework and cannot coverge under DQN framework. 
- Through analysis, we find that the action-attention block cannot work well in DQN framework. Finally, we adopt the idea of AttentionLight(https://github.com/LiangZhang1996/AttentionLight.git)  and use self-attention to replace the action-attention block.
- Our-realized AttenLight can converge and work well under all the datasets. It still retains the property as a universal model for any intersections. 
- For fair comparison, AttendLight uses the same hyper-parameters with other methods.


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
```latex
@InProceedings{pmlr-v162-zhang22ah,
  title = 	 {Expression might be enough: representing pressure and demand for reinforcement learning based traffic signal control},
  author =       {Zhang, Liang and Wu, Qiang and Shen, Jun and L{\"u}, Linyuan and Du, Bo and Wu, Jianqing},
  booktitle = 	 {Proceedings of the 39th International Conference on Machine Learning},
  pages = 	 {26645--26654},
  year = 	 {2022},
  editor = 	 {Chaudhuri, Kamalika and Jegelka, Stefanie and Song, Le and Szepesvari, Csaba and Niu, Gang and Sabato, Sivan},
  volume = 	 {162},
  series = 	 {Proceedings of Machine Learning Research},
  month = 	 {17--23 Jul},
  publisher =    {PMLR},
  pdf = 	 {https://proceedings.mlr.press/v162/zhang22ah/zhang22ah.pdf},
  url = 	 {https://proceedings.mlr.press/v162/zhang22ah.html},
  abstract = 	 {Many studies confirmed that a proper traffic state representation is more important than complex algorithms for the classical traffic signal control (TSC) problem. In this paper, we (1) present a novel, flexible and efficient method, namely advanced max pressure (Advanced-MP), taking both running and queuing vehicles into consideration to decide whether to change current signal phase; (2) inventively design the traffic movement representation with the efficient pressure and effective running vehicles from Advanced-MP, namely advanced traffic state (ATS); and (3) develop a reinforcement learning (RL) based algorithm template, called Advanced-XLight, by combining ATS with the latest RL approaches, and generate two RL algorithms, namely "Advanced-MPLight" and "Advanced-CoLight" from Advanced-XLight. Comprehensive experiments on multiple real-world datasets show that: (1) the Advanced-MP outperforms baseline methods, and it is also efficient and reliable for deployment; and (2) Advanced-MPLight and Advanced-CoLight can achieve the state-of-the-art.}
}


```
