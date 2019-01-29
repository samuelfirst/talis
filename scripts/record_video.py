#!/usr/bin/env python3
import logging
import sys
import streamlink
import os.path
import time

try:
    import cv2
except ImportError:
    sys.stderr.write("This example requires opencv-python is installed")
    raise

log = logging.getLogger(__name__)
GREEN = (0, 255, 0)

def stream_to_url(url, quality='best'):
    streams = streamlink.streams(url)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No steams were available")


def detect_faces(cascade, frame, scale_factor=1.1, min_neighbors=5):
    frame_copy = frame.copy()
    frame_gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(frame_gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)

    for (x, y, w, h) in faces:
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame_copy,'FACE',(x,y), font, .8,(255,255,255),2,cv2.LINE_AA)
        cv2.rectangle(frame_copy, (x, y), (x + w, y + h), GREEN, 1)

    return frame_copy


def main(url, channel, quality='best', fps=30.0, seconds=10):

    stream_url = stream_to_url(url, quality)
    log.info("Loading stream {0}".format(stream_url))
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    cap = cv2.VideoCapture(stream_url)

    width = cap.get(3)  # float
    height = cap.get(4) # float

    video  = cv2.VideoWriter("{0}-{1}.mp4".format(channel, time.time()), fourcc, fps, (int(width), int(height)));

    diff = 0

    end = 0
    start = time.time()

    while diff <= seconds:
       f,img = cap.read()
       key = cv2.waitKey(33) & 0xFF
       video.write(img)
       end = time.time()
       diff = end - start
       print(diff)
       if key==27:
           break;
    video.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Face detection on streams via Streamlink")
    parser.add_argument("url", help="Stream to play")
    parser.add_argument("channel", help="Stream to play")
    parser.add_argument("--stream-quality", help="Requested stream quality [default=best]",
                        default="best", dest="quality")
    parser.add_argument("--fps", help="Play back FPS for opencv [default=30]",
                        default=30.0, type=float)

    opts = parser.parse_args()

    main(opts.url, opts.channel, opts.quality, opts.fps)
