#!/usr/bin/env python3

import argparse
import cv2
from . import Transformer

def get_args():
    p = argparse.ArgumentParser(description="Create exposure lapses")
    p.add_argument("file", metavar="input")
    p.add_argument("-o", "--output", required=True, metavar="output", help="Output file")
    p.add_argument("-w", "--weight", metavar="weight")
    args = p.parse_args()
    return args

def main():
    args = get_args()

    ## Set up cv2 file reader and writer
    cap = cv2.VideoCapture(args.file)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # cap.get(cv2.CAP_PROP_FOURCC)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    def get_frames():
        while 1:
            has_frame, frame = cap.read()
            if not has_frame:
                break
            yield frame

    transformer = Transformer()
    transformer.source(get_frames)

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    for i,frame in enumerate(transformer):
        print("%s%% done (frame %s)." % (round(100 * (i+1) / frame_count), i+1))
        writer.write(frame)

    cap.release()
    writer.release()

if __name__ == "__main__":
    main()
