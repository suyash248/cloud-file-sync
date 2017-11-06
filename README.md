# file-sync
File sync(Similar to Google drive, Dropbox) using AWS S3
Note: S3 bucket must be created beforehand. 

# Requirements
python 2.x, pip, AWS account (for S3)

# How to run?
1. Put S3 credentials under ```etc/conf/settings.py```. Other configurations can also be changed but they are optional.
2. Create virual environment and activate it as


```sh
$ virtualenv .environment
$ source .environment/bin/activate
```


3. Add project to PYTHONPATH as 

```sh 
export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

3. Go to project root and install requirements/dependencies as - ```pip install -r requirements.txt```
4. Then run sync.py as - ```python tests/sync.py```
