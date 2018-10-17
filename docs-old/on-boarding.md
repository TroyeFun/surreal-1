# Onboarding installation guide for new Surreal Team members
This guide helps you setup surreal and run experiments, both locally and remotely. This guide should work on Mac or a linux machine. If you meet problems, you can ask Jim (jimfanspire@gmail.com) or Jiren (jirenz@stanford.edu).

## Setup python env
* Depending on your preference, setup a python 3 (3.5/3.6) environment, say named `<surreal_venv>`
* We will assume that `<surreal_venv>` is activated in this guide
* It is highly recommended that you use conda, `conda create -n <surreal_venv> python=3.6`
* Our own tradition is `<surreal_venv> = surreal`
* The remainder of the installation should be done within the virtualenv, using `source activate <surreal_venv>`

## Surreal and Tensorplex 
We will install necessary libraries so we can start an experiment locally. The installation below requires make and a C++ compiler installed.
* Clone these repos [Surreal](https://github.com/SurrealAI/Surreal), [Tensorplex](https://github.com/SurrealAI/Tensorplex), [TorchX](https://github.com/SurrealAI/TorchX) and [Symphony](https://github.com/SurrealAI/symphony). We will refer to their path as `<surreal_path>`, `<tensorplex_path>`, `<torchx_path>`, and `<symphony_path>`. We will need these paths later
* Install some dependencies. Go to `<surreal_path>`, run
```bash
pip install -e .
pip install -r container/requirements.txt
```
* Install pytorch: our computation backend. 
```bash
conda install pytorch torchvision -c pytorch # or refer to http://pytorch.org
```
* [Mujoco](http://www.mujoco.org) is a physical simulator. We need to set it up for use
```bash
mkdir ~/.mujoco
cd ~/.mujoco
wget https://www.roboti.us/download/mjpro150_linux.zip
unzip mjpro150_linux.zip
rm mjpro150_linux.zip
wget https://www.roboti.us/download/mjpro131_linux.zip
unzip mjpro131_linux.zip
rm mjpro131_linux.zip
```
* Also, you need to put the liscense file `mjkey.txt` into `~/.mujoco`. Ask Jim or Jiren (or anyone you know working on surreal) if you don't have it.
* Install [dm_control](https://github.com/deepmind/dm_control), a set of benchmarking enviroments. Besides running the following command, check [dm_control's](https://github.com/deepmind/dm_control) readme.md 
```bash
pip install git+git://github.com/deepmind/dm_control.git
```
* Install the tensorplex library (later we will make it pip install-able). Go to `<tensorplex_path>`, run
```bash
pip install -e .
```
* Install the torchx library (later we will make it pip install-able). Go to `<torchx_path>`, run
```bash
pip install -e .
```
* Install the symphony library (later we will make it pip install-able). Go to `<symphony_path>`, run
```bash
pip install -e .
```

## Jupyter
To run an experiment locally, we use jupyter notebook to manage the processes. Here is a short guide for setup.
* If you don't have jupyter-notebook, install jupyter-notebook.
```bash
pip install jupyter
```
* Register ipython kernel for `<surreal_venv>`. So that we can run experiments locally. Refer to [this doc](http://ipython.readthedocs.io/en/stable/install/kernel_install.html) for registering ipython kernel
```bash
pip install ipykernel
python -m ipykernel install --user --name surreal
```
* You can open the jupyter notebook `cluster_dashboard_symphony.ipynb` to run an experiment using the tmux backend. All processes in tmux mode will be run in tmux windows on the same machine. Navigate to `<surreal_path>/surreal/main/` and `jupyter notebook`.
* If using a remote machine, you can use ssh forwarding to access its jupyter notebook, `ssh -N -f -L localhost:8888:localhost:8888 remote_machine_hostname`.  Then, navigate to `localhost:8888`.

## Docker - Kubernetes - Google Cloud
To run an experiment remotely, we deploy the framework into docker containers. Here are the setup guides
* Ask Jim to add you to the his google cloud project.
* Install [docker](https://www.docker.com)
* Goto `<surreal_repo>/container` and do `make pull-all`. This fetches all the base images that you will build from. Note: This will take 30G of disk space.
* Install [google cloud commandline tools](https://cloud.google.com/sdk/). 
* To talk to kubernetes, we have a commandline wrapper `kurreal` that orchestrates experiments. `kurreal` requires some configs.
* Copy `<surreal_repo>/container/sample.surreal.yml` to `~/.surreal.yml`. 
* IMPORTANT!!!: Update your `~/.surreal.yml` following the comments in the file.
* Install `kubectl`. This is the commandline tool to talk to a kubernetes cluster. You can use [the official guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/) or do `gcloud components install kubectl`
* Now we need to configure google cloud config to our project/cluster/zone. Do the following
```bash
gcloud config set project jimfan2018-208323
gcloud config set container/cluster kurreal
gcloud config set compute/zone us-west1-b
gcloud container clusters get-credentials kurreal
```

# Run an experiment on the cloud
Here we are going to create a default experiment (using DDPG by default) on dm_control cheetah with 4 agents using k80 GPU:  
* !! Important: kurreal's git snapshot functionality is non-atomic  
* !! when kurreal is doing git operatoins for you, don't ctrl-C 
```bash
kurreal create-dev [experiment-name] 4 --gpu
```
* If everything runs fine, you will see an experiment running. We can inspect the actor/leaners (named pods in kubernetes's terminology) by using `kurreal p` (p is for pods)
* Use `kurreal tb` to open the tensorboard for an experiment.
* Use `kurreal logs [learner/agent-0/eval-1/replay/ps...]` to see the logs of respective processes.
* Each experiment is under a specific namespace. 
* `kurreal ns` tells you what is your current namespace.
* `kurreal ls` lists all namespaces.
* `kurreal ns [namespace_name]` swtiches your current namespace
* Use `kurreal delete` to delete an experiment

