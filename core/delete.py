import json
import os
import shutil
from lib.s3boto import s3_client
from etc.conf import settings
from core.journal import get_journal

def delete_file(file_to_be_deleted):
    """
    Deletes file from S3
    :param file_to_be_deleted: Absolute file path
    :return:
    """
    local_journal_file, local_journal = get_journal({}, journal_loc=settings.LOCAL_JOURNAL_LOCATION)
    s3_keyname = file_to_be_deleted[len(settings.LOCAL_SYNC_LOCATION) + 1:]
    try:
        print "[WARN] Deleting... %s" %file_to_be_deleted
        s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=s3_keyname)
    except:
        print "[ERROR] Couldn't delete s3 object", s3_keyname
    popped_file_to_be_deleted_key = local_journal.pop(file_to_be_deleted, None)
    if popped_file_to_be_deleted_key:
        #print "[DEBUG] Updating journal..."
        file(local_journal_file, "w").write(json.dumps(local_journal))

def delete_from_local(local_file_comp_path):
    """
    Deletes file from local system
    :param local_file_comp_path: Absolute file path
    :return:
    """
    if os.path.exists(local_file_comp_path):
        if os.path.isdir(local_file_comp_path):
            shutil.rmtree(local_file_comp_path)
        else:
            os.remove(local_file_comp_path)
            parent_dir = os.path.abspath(os.path.join(local_file_comp_path, os.pardir))
            if not os.listdir(parent_dir):
                print "[WARN] Deleting empty directory... %s" %parent_dir
                os.rmdir(parent_dir)
