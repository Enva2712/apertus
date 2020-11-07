import argparse
import cv2

def get_args():
    p = argparse.ArgumentParser(description='Process some integers.')
    p.add_argument("file")
    p.add_argument("-o", "--output", default="-", metavar="output", help="Output file")
    args = p.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    cap = cv2.VideoCapture(args.file)
    while(1):
        ret, frame = cap.read()
        if(cv2.waitKey(1) & 0xFF == ord('q') or ret == False):
            cap.release()
            cv2.destroyAllWindows()
            break
        cv2.imshow('frame', frame)
