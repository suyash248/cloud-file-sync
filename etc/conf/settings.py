# S3 specific settings
S3_ACCESSKEY = "your_s3_access_key"
S3_SECRETKEY = "your_s3_secret_key"

# We assume that S3_BUCKET already exists.
S3_BUCKET = "your_s3_bucket"  

# In order to avoid duplicate uploads, we maintain journals of previously downloaded files along with their md5 hash
LOCAL_JOURNAL_LOCATION = "~/.s3filesync.txt"

# This file is a journal containing latest files along with their md5 hash, if a file is deleted remotely then we must
# delete it from local system.
S3_FILE_NAMES_JOURNAL_LOCATION = "~/.s3filesync_filenames.txt"

# Location where remote files are downloaded, any modification in this directory(including sub directories) will trigger
# upload process
LOCAL_SYNC_LOCATION = '/Users/suyash/sync_loc'
