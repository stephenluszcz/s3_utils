# Import tinys3 Library for Python S3 SDK
import tinys3   #s3 client

import os       #used by main
import sys      #used by main
import getopt   #used by main

import shutil   #CopyAndAppendTimeDateToFilename
import time     #CopyAndAppendTimeDateToFilename

# set AWS credentials 
# could also set these as evnironment variables
#    AWS_ACCESS_KEY_ID='...'
#    AWS_SECRET_ACCESS_KEY='...'
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''

# to set font colors for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#///////////////////////////////////////////////////////////////////////
# UploadFileToS3Bucket
# Uploads specified file via SSL to specified bucket 
#///////////////////////////////////////////////////////////////////////
def UploadFileToS3Bucket(my_file, the_bucket):
    # open a connection to S3

    #open connection to S3 and use SSL
    s3_conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True)

    #upload file
    file_d = open(my_file, 'rb')
    print bcolors.HEADER + "Info: " + bcolors.ENDC + "Uploading " + bcolors.WARNING + my_file + bcolors.ENDC + " to S3 bucket " + bcolors.WARNING + the_bucket + bcolors.ENDC + " status: "

    s3_conn.upload(my_file, file_d, bucket=the_bucket)
    print s3_conn.upload(my_file, file_d, bucket=the_bucket)
#END
#///////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////
# create timestamped file
# copy input file to a time/date stamped file 
# Removes the path from the filename and copies the time/date stamped
# file to the current working directory.
# TODO: extend functionality to pass in an output directory path
# 
# returns: copy of input file with time & date stamp appended to filename
#///////////////////////////////////////////////////////////////////////
def CopyAndAppendTimeDateToFilename(filename):
    #save current date / time
    #do no use : in filenames, not allowed in Windows filenames
    current_date_time = time.strftime("%Y-%m-%d_%H%M%S")

    #print "filename (full path): " + filename

    #filename will include path info...we just want the filename
    just_filename = filename

    # need to remove the path info from the filename (for Linux)
    if '/' in just_filename:
        tmp_file = filename.rsplit('/', 1)[1]
        just_filename = tmp_file

    # need to remove the path info from the filename (for Windows)
    # just looking for a single \ but need escape sequence
    if '\\' in filename:
        tmp_file = filename.rsplit('\\', 1)[1]
        just_filename = tmp_file

    #print "filename (path extracted): " + filename

    # if no extension on the filename don't worry about adding it
    if not '.' in just_filename: 
        #create log file based on current date / time
        timedate_log_filename = just_filename + "_" + current_date_time
      
    else:
        #save everything to the left of the last .
        tmp_name = just_filename.rsplit('.', 1)[0]

        #save everything to the right of the last .
        ext = just_filename.rsplit('.', 1)[1]
      
        #create log file based on current date / time and add the file extension
        timedate_log_filename = tmp_name + "_" + current_date_time + "." + ext

    #copy file to time / date stamped file
    #file will be copied to cwd (current working directory)
    shutil.copyfile(filename, timedate_log_filename)

    return timedate_log_filename
#END
#///////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////
# main
#///////////////////////////////////////////////////////////////////////

def main(argv):
    current_py_filename = os.path.basename(__file__) 
    help_text = current_py_filename + ' -i <inputFile> -b <bucketName> -k'
    inputFile = ''
    bucketName = ''
    keep_file = False

    try:
        opts, args = getopt.getopt(argv,"hi:b:k",["ifile=","bname="])
    except getopt.GetoptError:
        print help_text
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_text
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-b", "--bname"):
            bucketName = arg
        elif opt in ("-k:"):
            keep_file = True

    #print 'Input file is:', inputFile
    #print 'Bucket name is:', bucketName
    #print 'Keep is:', keep_file 

    if not (inputFile):
      print "Error: missing required input parameters"
      print help_text
      sys.exit(2)

    if not (bucketName):
      print "Error: missing required input parameters"
      print help_text
      sys.exit(2)

    #///////////////////////////////////////////////////////////////
    #Program start here now that we have our inputs

    #take input file, copy it and append time / date to name
    timedate_logfile = CopyAndAppendTimeDateToFilename(inputFile)

    #upload the file to bucket
    UploadFileToS3Bucket(timedate_logfile, bucketName)

    #user does NOT want to keep the original so delete it
    if not keep_file:
        print bcolors.HEADER + 'Info: ' + bcolors.ENDC + 'Deleting original file ' + bcolors.WARNING + inputFile + bcolors.ENDC
        os.remove(inputFile)

#END

#///////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
   main(sys.argv[1:])
#EOF