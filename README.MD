# Tornado Madness Bot
This is a an automated bot for playing a game titled 'Tornado Madness' utilizing object detection via machine learning. The original implementation was performed over at ClarityCoders on Youtube, as well as source code: https://github.com/ClarityCoders/TornadoBot

This project aims to expand the original object classes during detection so that an improved bot can be implemented by learning optimal techniques and game strategies for progression. Ideally via machine learning a bot can be produced that learns gameplay optimizations without manually coding actions/instructions.

Steps:
 - -> __Introduce 'computer vision', enabling the bot to identify important objects on screen__
 - Optimize computer vision. Faster object detection, with high accuracy will greatly improve the bot as quicker decisions and their associated actions will directly translate to faster game progression.
 - Train bot decisions along with actions, in conjunction with previously optimized vision
    - This may require rewriting a smaller,faster variant of the original game for training purposes. Leveraging the original game for train would be highly dis-optimal as it requires significant computation resources given what it actually does. There are many reason for this, #1 being in browser, #2 being javascript (v8).
    - When train the bot many many instances will need to be running in parallel, otherwise the bot will fail make significant progress except in the span of months to years, where is might only require days to weeks on the same hardware.
    - As a shortcut to running the computer vision object detection while training, direct object locations might be supplied instead to speed up training
 - Develop bot that can adapt quickly (without 100's of rounds of training) to changed game rules. So if the game mechanics change or the way the game renders changes, or various icons and textures change the bot can recognize the change and still play effectively without intensive parallel retraining every time the game changes or is updated.


#### List of Identified Optimizations:
Human identified:
 - Spamming collisions by hitting an object such as a tree with the tornado, moving away just enough to register as 'non-collided', and then moving the tornado to collide with the same object. Repeat quickly until object destroyed.
    - This enables the tornado to destroy an object incredibly fast because the game does not track if an object has already been collided with within xx time period.
    - Normally the tornado will 'tick' damage against an object over a ~1 second interval, but with this technique any object can be destroyed rapidly.
    - Medium difficulty to pull off because it requires moving the mouse in an erratic manner and very quickly but easy for a bot which can merely instruct the OS to move the mouse pointer to x,y position.
 - Increasing tornado damage over any other stat
    - should allow for faster progression
 - Colliding with more than one object at a time
 - Conserving gas. Waiting up until the last few seconds to reach a known gas source to refuel the tornado.
 - When enough money for a specific upgrade is reached, run out of fuel so the shop can be reached faster, buy the upgrade, and progress faster.
 - Target clusters of objects over single or sparse objects
 - Target buildings over trees
 - Reach berserk by destroying objects in quick succession.
 - Don't click the 'Refuel' button, but instead click 'No Thanks' As soon as possible.
 - Waiting for building dense areas to use meteor skil
 - Using lightning skill only when close enough to objects

Bot identified:
*requires learning integration, not yet written*


### Running the bot
``` python
python.exe bot.py
```

Controls:
 - `q` to exit the program
 - `w` to stop the bot from performing actions
 - `s` to start the bot to move the mouse and type keys

### Training the bot
Take advantage of python notebooks inside Jupyter Hub/Lab/Notebooks or even inside your IDE for better visualization and management of the training process and results.

Make sure Jupyter Labs is installed. Run while inside this project's directory.
```
jupyter lab
```

If using Jupyter notebooks, make sure it is installed and start it up inside this project's directory

#### Roboform annotations
If using roboform to annotate images, Open up the `train yolov8 roboform.ipynb` python notebook file and run through each step. You'll need to replace the "API_KEY" with your Roboform account's key.

#### Custom annotations
If using assets originating elsewhere, first download them and extract (unzip/untar) to tornado_madness-X, where X is the training version. Modify `train yolov8 local.ipynb` in the step before training to point to `{project}-{version}` to match the folder the training data was placed. The training program will ultimately need to be provided a path to `data.yml`

``` python
project = "tornado_madness"
version = 6
```

### Install dependencies
_Its best practice to create a virtual python environment (aka venv) before performing installing any packages (Instructions/commands not included here). This way the versions of packages being utilized remains consistent for this project._

When only running the bot:
```
pip install -r bot-requirements.txt
```
When training:
```
pip install -r training-requirements.txt
```

#### Install pytorch for GTX 1650, Windows
**Note: make sure to utilize a gpu when training and when running the bot:**

Because `utralytics` `yolov8` is designed to work out of the box it will attempt to use the cpu if no gpu can be used. Under the hood it uses `pytorch` as the backend for communicating gpu work, so for the fastest training/inference first install the version of `pytorch` that can full make use of the gpu.

For Nvidia, CUDA is an important feature for training/inference and often simply just installing the latest CUDA along with the latest pytorch won't enable use of CUDA. This is due to #1, the package maintainers not ensuring full backwards compatible support (there are good reasons for this!), and #2 not including a fool-proof way of detecting older gpus and then installing the most appropriate torch and/or specifing that the end user might want to install x.x.x version of CUDA from Nvidia. A primary effect for those using older gpus is that you'll likely want to go out and navigate through this complexity so that the inference/training/detection will be much much faster for you...

* https://stackoverflow.com/a/64474501
* https://pytorch.org/get-started/previous-versions/
* https://en.wikipedia.org/wiki/CUDA#GPUs_supported

#### GTX 1650 - specific example
- aka CUDA 7.5
- aka CUDA SDK 10.2

Note: there were no precompiled wheels for python 3.10+ on windows for 'torch', so python version 3.9 should be used as well as an older version of the torch package. __There is likely some way to compile the latest version of torch for the specified version of python and the appropriate version of CUDA SDK.__ 

#### Using windows, python 3.9, cu102 (cuda sdk 10.2):
```
pip install torch==1.10.2+cu102 --extra-index-url https://download.pytorch.org/whl/cu102
pip install torchvision==0.11.3+cu102 --extra-index-url https://download.pytorch.org/whl/cu102
pip install torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu102
```
#### for Nvidia hardware
After all the torch installation shenanigans double check torch's ability to utilize CUDA. **The output for '.is_available()' should be true!**
- command
    ``` commandline
    python -c 'import torch; print(str(torch.cuda.is_available()))'
    ```
- python
    ``` python
    import torch
    print("cuda is_available:" + str(torch.cuda.is_available()))
    print("cuda device_count:" + str(torch.cuda.device_count()))
    print("cuda current_device:" + str(torch.cuda.current_device()))
    print("cuda device:" + str(torch.cuda.device(0)))
    print("cuda get_device_name:" + str(torch.cuda.get_device_name(0)))
    ```

Then, check ultralytics ability to leverage `pytorch` _(entering the cusp of dependency hell)_:
- command
    ``` commandline
    python -c 'import ultralytics; ultralytics.checks()'
    ```
- python
    ``` python
    import ultralytics
    ultralytics.checks()
    ```

Lastly, if you're unsure if pytorch is utilizing the gpu during training/predicting, run this command and check the output before and after running a machine learning job. If the gpu wasn't using (hardly any) memory but is now using 1+ GB, then the gpu is being used. This is a more reliable indicator as GPU processing utilization % (as can be found in Task Manager) may be bottlenecked presumably by hard drive transfer speeds and or gpu memory capacity, appearing as 0%-10%

_Note there is a caveat that sometimes, despite not actively training/predicting on the gpu, memory will remain allocated. This appeared while running a train job in `jupyter labs`, and possibly only after crashing._
``` command
nvidia-smi
```
output after machine learning job:
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI XXX.XX                 Driver Version: XXX.XX         CUDA Version: XX.X     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                     TCC/WDDM  | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce GTX 1650 ...  WDDM  |   00000000:02:00.0 Off |                  N/A |
| N/A   53C    P8              5W /   35W |    1450MiB /   4096MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A     14904      C   C:\Program Files\Python39\python.exe        N/A      |
+-----------------------------------------------------------------------------------------+
```

### Creating requirements.txt
Due to this error, exclude any non python files 
 - `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb1 in position 81: invalid start byte`

bot requirements:
```
pipreqs --ignore bin,etc,include,lib,lib64,.ipynb_checkpoints,tornado_madness-6,runs,weights,yolov8n.pt,yolov8s.pt,.venv --force 
--encoding=utf-8
```
training requirements:
```
pipreqsnb '.\train yolov8 roboform.ipynb'
```

