import os, json, hashlib
from lib.s3boto import s3_client
from etc.conf import settings
from core.journal import get_journal

class Uploader(object):

    def lazy_upload_recursively(self):
        """
        Uploads files/directories if any change occurs in settings.LOCAL_SYNC_LOCATION
        :return:
        """
        local_journal_file, local_journal = get_journal({}, journal_loc=settings.LOCAL_JOURNAL_LOCATION)
        files_to_be_uploaded = []
        update_journal = False
        for root, dirs, files in os.walk(settings.LOCAL_SYNC_LOCATION):
            for xfile in files:
                files_to_be_uploaded.append(os.path.join(root, xfile))

        for file_to_be_uploaded in files_to_be_uploaded:
            s3_keyname = file_to_be_uploaded[len(settings.LOCAL_SYNC_LOCATION)+1:]
            try:
                local_md5 = hashlib.md5(file(file_to_be_uploaded).read()).hexdigest()
            except IOError:
                pass
            if local_journal.get(file_to_be_uploaded, "") == local_md5:
                pass
                #print "[DEBUG] Skipping, already uploaded %s" % (file_to_be_uploaded)
            else:
                print "[INFO] Uploading... {file_to_be_uploaded} to s3 bucket {s3_bucket} as key {s3_keyname}" \
                    .format(file_to_be_uploaded=file_to_be_uploaded, s3_bucket=settings.S3_BUCKET, s3_keyname=s3_keyname)
                s3_client.upload_file(file_to_be_uploaded, settings.S3_BUCKET, s3_keyname)

                # Update journal object
                local_journal[file_to_be_uploaded] = local_md5
                update_journal = True
        if update_journal:
            #print "[DEBUG] Updating journal..."
            # Write serialized journal object to journal file
            file(local_journal_file, "w").write(json.dumps(local_journal))
