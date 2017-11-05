# file-sync
File sync(Similar to Google drive, Dropbox) using AWS S3

# Requirements
python 2.x, pip, AWS account (for S3)

# How to run?
1. Put S3 credentials under ```etc/conf/settings.py```. Other configurations can also be changed but they are optional.
2. Go to project root and install requirements/dependencies as - ```pip install -r requirements.txt```
3. Then run sync.py as - ```python tests/sync.py```
