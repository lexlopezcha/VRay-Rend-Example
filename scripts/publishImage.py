#!/usr/bin/env python
import argparse
import sys
import string
import os
import subprocess
import uuid
import boto3
import smtplib
from datetime import datetime
from botocore.exceptions import NoCredentialsError
from PIL import Image, ImageColor
import webcolors

# website_url = ' '
# output_dir = '/tmp/'

ACCESS_KEY = ' '
SECRET_KEY = ' '

# path = 'C:/Users/vr/Desktop/VrayRendering/VRayRenderingPreview/images/image_10008.jpg'

# # Upload usdz file to s3

def push_to_cloud(output_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(output_file, bucket, s3_file,
                       ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
    except Exception as e:
        print(e)
        exit(1)


def average_image_color(filename):
    i = Image.open(filename)
    h = i.histogram()
    # print(h)
    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    curr_r = sum(i*w for i, w in enumerate(r)) / sum(r)
    curr_g = sum(i*w for i, w in enumerate(g)) / sum(g)
    curr_b = sum(i*w for i, w in enumerate(b)) / sum(b)

    curr_col = [curr_r, curr_g, curr_b]

    return curr_col


def main():
    if len(sys.argv) < 2:
        raise Exception('No argument provided')

    discard_threshold = 40
    discard_img = [discard_threshold, discard_threshold, discard_threshold]
 
    start = datetime.now()
    ac = average_image_color(sys.argv[1])[:]
    print(ac)
    if ac < discard_img[:]:
        print('discard')
    else:
        print('keep')
        push_to_cloud(
            sys.argv[1],
            'ios-data-capture',
            'maya/render.jpg'
        )
    end = datetime.now() - start
    print(end)
if __name__ == '__main__':
    main()
