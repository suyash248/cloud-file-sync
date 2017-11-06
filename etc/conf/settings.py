# S3 specific settings
S3_ACCESSKEY = "AKIAIAX7NRWZBVWJQYTA"
S3_SECRETKEY = "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"
S3_BUCKET = "wigzoextra"

# In order to avoid duplicate uploads, we maintain journals of previously downloaded files along with their md5 hash
LOCAL_JOURNAL_LOCATION = "~/.s3filesync.txt"

# This file is a journal containing latest files along with their md5 hash, if a file is deleted remotely then we must
# delete it from local system.
S3_FILE_NAMES_JOURNAL_LOCATION = "~/.s3filesync_filenames.txt"

# Location where remote files are downloaded, any modification in this directory(including sub directories) will trigger
# upload process
LOCAL_SYNC_LOCATION = '/home/wigzo/sync_loc'