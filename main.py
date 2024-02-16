import numpy as np
import cv2 as cv
import pickle
import sys

videPath = "vid/vid.mp4"

def set_color(bg, fg):
    return "\u001b[48;5;%s;38;5;%sm" % (bg, fg)

def main():

    width = 450
    height = 240
    LUT = np.load("LUT.npy")
    LERPED = pickle.load(open("colors.pkl", "rb"))
    BLACK = "\u001b[48;5;16;38;5;16m"

    CHARSET = " ,(S#g@@g#S(, "

    videcCapture = cv.VideoCapture(videPath)
    fps  = videcCapture.get(cv.CAP_PROP_FPS)

    while(videcCapture.isOpened()):
        ret, frame = videcCapture.read()

        frame = cv.resize(frame, (width, height))

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        print(fps)
        if(cv.waitKey(1) & 0xFF == ord('q')):
            break

        img = cv.resize(frame, (width, height))

        lines = []
        
        for row in img:
            line = ""

            for color in row:
                color = np.round(color).astype(int)
                b, g, r = color[0], color[1], color[2]

                idx = LUT[b, g, r]
                bg, fg, lerp, _ = LERPED[idx]

                char = CHARSET[lerp]

                line += "%s%c" % (set_color(bg, fg), char)

                line += BLACK + "\n"  # Add a black background to avoid color fringe
                lines.append(line)

        lines.append("\u001b[%iD\u001b[%iA" % (width, height + 1))


 
            
main()