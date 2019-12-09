#!/usr/bin/env python3
# Test S3 code

import os
import sys
import warnings

sys.path.append( os.path.join( os.path.dirname(__file__), "../..") )

import ctools.s3 as s3

## Find a S3 bucket for testing. This is either TEST_S3ROOT or DAS_S3ROOT
if "TEST_S3ROOT" in os.environ:
    TEST_S3ROOT = os.environ['TEST_S3ROOT']
elif "DAS_S3ROOT" in os.environ:
    TEST_S3ROOT = os.environ['DAS_S3ROOT']
else:
    TEST_S3ROOT = None



TEST_STRING = "As it is written " + str(os.getpid()) + "\n"
MOTD = 'etc/motd'

def test_s3open():
    if "EC2_HOME" not in os.environ:
        warnings.warn("test_s3open only runs on AWS EC2 computers")
        return

    if TEST_S3ROOT is None:
        warnings.warn("no TEST_S3ROOT is defined.")
        return

    # Make sure attempt to read a file that doesn't exist gives a FileNotFound error
    got_exception = True
    try:
        f = s3.s3open("bad path")
        got_exception = False
    except ValueError as e:
        pass
    if got_exception==False:
        raise RuntimeError("should have gotten exception for bad path")

    path = os.path.join( TEST_S3ROOT, MOTD)

    print("path:",path)

    # Make sure s3open works in a variety of approaches

    for line in s3.s3open(path,"r"):
        print("> ",line)

    f = s3.s3open(path,"r")
    print("motd: ",f.read())

    with s3.s3open(path,"r") as f:
        print("motd: ",f.read())


def test_s3open_write_fsync():
    """See if we s3open with the fsync option works"""
    if "EC2_HOME" not in os.environ:
        warnings.warn("s3open only runs on AWS EC2 computers")
        return

    if TEST_S3ROOT is None:
        warnings.warn("no TEST_S3ROOT is defined.")
        return


    path = os.path.join( DAS_S3ROOT, f"tmp/tmp.{os.getpid()}")
    with s3.s3open(path,"w", fsync=True) as f:
        f.write( TEST_STRING)
    with s3.s3open(path,"r") as f:
        buf = f.read()
        print("Wanted: ",TEST_STRING)
        print("Got:: ",buf)
        assert buf==TEST_STRING

    s3.s3rm(path)


def test_s3open_iter():
    if "EC2_HOME" not in os.environ:
        warnings.warn("s3open only runs on AWS EC2 computers")
        return


    if TEST_S3ROOT is None:
        warnings.warn("no TEST_S3ROOT is defined.")
        return



    path = os.path.join(DAS_S3ROOT, f"tmp/tmp.{os.getpid()}")
    with s3.s3open(path,"w", fsync=True) as f:
        for i in range(10):
            f.write( TEST_STRING[:-1] + str(i) + "\n")

    with s3.s3open(path, "r") as f:
        fl = [l for l in f]
        for i, l in enumerate(fl):
            assert l == TEST_STRING[:-1]  + str(i) + "\n"

    f = s3.s3open(path, "r")
    fl = [l for l in f]
    for i, l in enumerate(fl):
        assert l == TEST_STRING[:-1] + str(i) + "\n"

    s3.s3rm(path)

    
if __name__=="__main__":
    test_s3open()
    test_s3open_write_fsync()
