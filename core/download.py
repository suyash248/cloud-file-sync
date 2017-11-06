import os
import json
import threading
from lib.s3boto import s3_client, resource
from etc.conf import settings
from core.journal import get_journal
from copy import deepcopy
from core.delete import delete_from_local

remote_file_complete_paths = {}
class Downloader(object):

    @classmethod
    def download_and_sync(self):
        threading.Timer(20.0, Downloader.download_and_sync).start()  # called every 20 sec
        Downloader().lazy_download_recursively()
        global remote_file_complete_paths
        remote_file_complete_paths = {}
        Downloader().check_and_delete()

    def check_and_delete(self):
        """
        Checks if a file is deleted remotely then we must delete it from local system.
        :return:
        """
        local_journal_file, local_journal = get_journal({}, journal_loc=settings.LOCAL_JOURNAL_LOCATION)
        s3_file_paths_journal_file, s3_file_paths_journal = get_journal({}, journal_loc=settings.S3_FILE_NAMES_JOURNAL_LOCATION)
        update_journal = False

        local_file_complete_paths = set(deepcopy(local_journal.keys()))
        s3_file_paths = s3_file_paths_journal.keys()
        for local_file_comp_path in local_file_complete_paths:
            if local_file_comp_path not in s3_file_paths:
                popped_file = local_journal.pop(local_file_comp_path, None)
                if popped_file:
                    update_journal = True
                    print "[WARN] Deleting... %s" % local_file_comp_path
                    s3_keyname = local_file_comp_path[len(settings.LOCAL_SYNC_LOCATION) + 1:]
                    try:
                        s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=s3_keyname)
                        delete_from_local(local_file_comp_path)
                    except:
                        pass

        if update_journal:
            #print "[DEBUG] Updating journal..."
            file(local_journal_file, "w").write(json.dumps(local_journal))

    def write_and_flush(self, file_path, data):
        """
        Writes serialized data to journal file.
        :param file_path:
        :param data:
        :return:
        """
        xfile = os.path.expanduser(file_path)
        s3_journal_xfile = file(xfile, "w")
        s3_journal_xfile.write(data)
        s3_journal_xfile.truncate()
        s3_journal_xfile.close()

    def lazy_download_recursively(self, dist=''):
        """
        Recursively downloads, if necessary, remote files also creates directories, if required
        :param dist:
        :return:
        """
        global remote_file_complete_paths
        local_journal_file, local_journal = get_journal({}, journal_loc=settings.LOCAL_JOURNAL_LOCATION)
        update_journal = False
        paginator = s3_client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=settings.S3_BUCKET, Delimiter='/', Prefix=dist):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    self.lazy_download_recursively(subdir.get('Prefix'))

            xfiles = result.get('Contents') or []
            for xfile in xfiles:
                s3_key = xfile.get('Key')
                local_file_path = os.path.join(settings.LOCAL_SYNC_LOCATION, s3_key)
                try:
                    head_obj = s3_client.head_object(Bucket=settings.S3_BUCKET, Key=s3_key)
                    remote_md5 = head_obj.get('ETag', '').replace('"', '')
                except:
                    remote_md5 = ''
                local_md5 = local_journal.get(local_file_path, '')

                remote_file_complete_paths[local_file_path] = remote_md5
                if remote_md5 == local_md5:
                    #print "[DEBUG] Skipping... {local_file_path} is already up-to-date".format(local_file_path=local_file_path)
                    continue

                print "[INFO] Downloading... {xfile} to {local_path}".format(xfile=s3_key, local_path=settings.LOCAL_SYNC_LOCATION)
                if not os.path.exists(os.path.dirname(local_file_path)):
                    print "[INFO] Creating... new directory {dir_name}".format(dir_name=local_file_path)
                    os.makedirs(os.path.dirname(local_file_path))

                try:
                    resource.meta.client.download_file(settings.S3_BUCKET, s3_key, local_file_path)
                except:
                    print "[ERROR] Couldn't download s3 object", s3_key
                local_journal[local_file_path] = remote_md5
                update_journal = True

        self.write_and_flush(settings.S3_FILE_NAMES_JOURNAL_LOCATION, json.dumps(remote_file_complete_paths))

        if update_journal:
            #print "[DEBUG] Updating journal..."
            self.write_and_flush(settings.LOCAL_JOURNAL_LOCATION, json.dumps(local_journal))
