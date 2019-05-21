# Using OpenCV to identify objects from screen live

This is basic functionality for reading from your screen with OpenCV. 

Personally, I've used it for web scraping with BeautifulSoup and to build game bots. I've added low level input for keyboard, because many games weren't respond to higher level input like pyautogui.

Basically, we are taking screenshots from screen, then adding it to OpenCV and operating with OpenCV output.

You will have a live window which shows OpenCV vision of your screen.

Notice, that you should provide template image for code to work.
For pressing keys use pressKey(hexKeyCode), then use time.sleep(how long sec) command and releaseKey(hexKeyCode).
You can find hex keys here: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

For template recognition accuracy play with res parameter in loc = np.where(res >= 0.5). Higher the value, more accurate output will be.
Sometimes, I placed it right on 0.5 (minimum value for correct template recognition) and it works fine, but if I placed it higher it won't. So try different values.
