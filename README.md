# File-sync
File sync(Similar to Google drive, Dropbox) using AWS S3.

> Note: S3 bucket must be created beforehand. 

#### Requirements
Python 2.x, pip, AWS account (for S3)

#### How to run?
1. Put S3 credentials under ```etc/conf/settings.py```. Other configurations can also be changed but they are optional.
2. Move to ```<project-dir>```, create virual environment and then activate it as


```sh
$ cd <project-dir>
$ virtualenv .environment
$ source .environment/bin/activate
```


3. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

3. Go to project root and install requirements/dependencies as 

```sh 
$ pip install -r requirements.txt
```

4. Then run sync.py as  

```sh
$ python tests/sync.py
```
