import cv2
import numpy as np

def Capture_Event(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(f"({x}, {y})")
		
if __name__=="__main__":
	img = cv2.imread('images.jpeg', 1)
	cv2.imshow('image', img)
	cv2.setMouseCallback('image', Capture_Event)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
