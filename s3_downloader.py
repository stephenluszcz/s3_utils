# Import Boto Library for Python S3 SDK
import boto  #s3 library
import subprocess #bash commands

import os       #used by main
import sys      #used by main
import getopt   #used by main

#///////////////////////////////////////////////////////////////////////
# DownloadFileFromS3Bucket
# Downloads specified file via SSL from specified bucket 
#///////////////////////////////////////////////////////////////////////
def DownloadFileFromS3Bucket(filename, the_bucket):

    # boto is using creds set from ~/.aws/credentials
    # to use a certain profile add parameter profile_name="" 
    s3_conn = boto.connect_s3()

    bucket_name = the_bucket

    #get a connection to a bucket
    bucket = s3_conn.create_bucket(bucket_name)

    #get list of keys in the bucket
    #bucket_list = bucket.list()

    #download_file = "test_script_download.sh"
    download_file = filename

    #download the file, we know it's there
    the_script = bucket.get_key(download_file)

    print "Downloading file: " + the_script.name
    the_script.get_contents_to_filename(the_script.name)
#END
#///////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////
# MakeFileExecutable
# sets file permissions to make file executable
#///////////////////////////////////////////////////////////////////////
def MakeFileExecutable(filename):
    
    #set permissions to make it executable
    print "Set file permissions to make script executable"
    subprocess.call("ls -la " + filename, shell=True)
    subprocess.call("chmod a+x " + filename, shell=True)
    subprocess.call("ls -la " + filename, shell=True)
#END
#///////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////
# main
#///////////////////////////////////////////////////////////////////////

def main(argv):
    current_py_filename = os.path.basename(__file__) 
    help_text = current_py_filename + ' -d <downloadFile> -b <bucketName>'
    downloadFile = ''
    bucketName = ''
    try:
        opts, args = getopt.getopt(argv,"hd:b:",["dfile=","bname="])
    except getopt.GetoptError:
        print help_text
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_text
            sys.exit()
        elif opt in ("-d", "--dfile"):
            downloadFile = arg
        elif opt in ("-b", "--bname"):
            bucketName = arg
    
    #print 'Download file is:', downloadFile
    #print 'Bucket name is:', bucketName

    if not (downloadFile):
      print "Error: missing required input parameters"
      print help_text
      sys.exit(2)

    if not (bucketName):
      print "Error: missing required input parameters"
      print help_text
      sys.exit(2)

    #///////////////////////////////////////////////////////////////
    #Program start here now that we have our inputs

    #download specified file from S3 bucket
    DownloadFileFromS3Bucket(downloadFile, bucketName)
    
    #set file permissions to executable
    MakeFileExecutable(downloadFile)

#END

#///////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
   main(sys.argv[1:])
#EOF

