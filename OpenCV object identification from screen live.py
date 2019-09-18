#hello git
import numpy as np
from PIL import ImageGrab
import cv2
import time
import ctypes

# just some simple C structure redefinitions 
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouse", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class Input_I(ctypes.Union):
    _fields_ = [("keyIn", KeyBdInput),
                 ("mouseIn", MouseInput),
                 ("hardIn", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("inI", Input_I)]

# you will use only this two functions
# to access keyboard input on low level
# it should work in any environment
# first press key, then use time.sleep(how long sec) command
# and release key

# you can find key codes here:
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
SendInput = ctypes.windll.user32.SendInput
def PressKey(hexKeyCode):
	"""input key code you want to press"""
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
	"""input key code you want to release"""
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# create template
# you need to input template path
template = cv2.imread('your_template_path', cv2.IMREAD_GRAYSCALE)
wid, heit = template.shape[::-1]

last_time = time.time() # create timestamp
while True:
	# take screenshot of bbox area, then convert it to uint8 np.array
	# note, that it's crucial to use uint8, because of its range (0 to 255)
	img_rgb = np.array(ImageGrab.grab(bbox=(0,40,800,640)), dtype=np.uint8)
	
	# create grayscale image for better recognition
	gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	# match gray image with template using TM_CCOEFF_NORMED
	res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
	# find mathes
	# play with template matching accuracy using res
	loc = np.where(res >= 0.5)
	
	# I implemented flag here, so you can use it after in development
	# if you find matches, flag will be True
	flag = False
	# pt will contain x,y coordinates of all the matched objects
	for pt in zip(*loc[::-1]):
		#draw rectangle(image, coordinates of image and rectangle, rectangle color + thickness)
		cv2.rectangle(img_rgb, pt, (pt[0] + wid, pt[1] + heit), (255, 0, 0), 2) 
		flag = True
		if flag:
			print(pt)
	
	# show live image
	cv2.imshow('window', cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB))
	
	# print how long it took
	print(f'loop took {time.time()-last_time} seconds, flag =', flag)
	
	# for exit press q
	last_time = time.time()
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break



