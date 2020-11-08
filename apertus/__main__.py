#!/usr/bin/env python3

import argparse
import cv2
import numpy

def get_args():
    p = argparse.ArgumentParser(description="Create exposure lapses")
    p.add_argument("file", metavar="input")
    p.add_argument("-o", "--output", required=True, metavar="output", help="Output file")
    p.add_argument("-w", "--weight", metavar="weight")
    args = p.parse_args()
    return args

def average_frames(current, last, weight=1):
    next = numpy.copy(current)
    for row_index in range(len(next)):
        for col_index in range(len(next[row_index])):
            for chan_index in range(len(next[row_index, col_index])):
                color = next[row_index, col_index, chan_index]
                last_color = last[row_index, col_index, chan_index]
                next[row_index, col_index, chan_index] = round((color + last_color * weight) / (weight + 1))
    return next

if __name__ == "__main__":
    args = get_args()

    # Set up video capture and video writer
    cap = cv2.VideoCapture(args.file)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # cap.get(cv2.CAP_PROP_FOURCC)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    last_frame = None
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(1, frame_count):
        got_frame, frame = cap.read()

        if not got_frame:
            # End of video capture
            break

        if last_frame is None:
            # First frame is just copied over
            next_frame = frame
        else:
            # All other frames are the weighted average of themselves with the previous frame
            next_frame = average_frames(frame, last_frame, weight=(i-1))
        print("%s%% done (frame %s)" % (round(100 * i/frame_count), i))
        writer.write(next_frame)
        last_frame = next_frame

    # Clean up
    cap.release()
    writer.release()
