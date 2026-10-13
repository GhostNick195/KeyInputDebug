
try: # check to see if you have all Modules

    # Modules 👇
    from pynput import keyboard
    from pynput import mouse
    import pyautogui
    from PIL import Image
    from PIL import ImageDraw
    import asyncio
    import time
    from pathlib import Path
    import tkinter as tk
    import sys
    # Modules 👆

    # Variables 👇
    stop_event = None

    loop = None

    LogList = []

    MouseLogList = []

    Click = 0

    Press = None

    r = 12

    StopMousePrint = 0

    LogListAppend = 0
    # Variables 👆

    # 👇 cool little gui so you know when code will start
    root = tk.Tk()

    root.title("Debug Menu")

    root.geometry("600x400")

    def stopcode():
        sys.exit()

    def StartMousePOS():
        global StopMousePrint
        StopMousePrint = 1
        MousePOSPrint.config(text="Disable MousePOS Print", font=("Calibri", 15), command=StopMousePOS)

    def StopMousePOS():
        global StopMousePrint
        StopMousePrint = 0
        MousePOSPrint.config(text="Enable MousePOS Print", font=("Calibri", 15), command=StartMousePOS)

    def EnableRelease():
        global LogListAppend
        LogListAppend = 1
        ReleaseAppend.config(text="Disable Release Key Append", font=("Calibri",15), command=DisableRelease)

    def DisableRelease():
        global LogListAppend
        LogListAppend = 0
        ReleaseAppend.config(text="Enable Release Key Append", font=("Calibri",15), command=EnableRelease)

    EndLabel = tk.Label(root, text="(Press 'end' key to stop code once running)", font=("Arial", 8))
    EndLabel.pack(pady=10)

    ReleaseAppend = tk.Button(root, text="Enable Released Key Append", font=("Calibri", 15), command=EnableRelease)

    ReleaseAppend.pack()

    MousePOSPrint = tk.Button(root, text="Enable MousePOS Print", font=("Calibri", 15), command=StartMousePOS)
    MousePOSPrint.pack()

    startbutton = tk.Button(root, text="Begin", font=("Calibri", 25), command=root.destroy)
    startbutton.pack()

    StopCodebutton = tk.Button(root, text="Cancel", font=("Calibri", 25), command=stopcode)
    StopCodebutton.pack()

    root.mainloop()
    # 👆 cool little gui so you know when code will start

    # 👇 for finding where the python file is saved on the device, will add a folder for all data being recorded. folder will be two text files and another folder for screenshots.
    scriptpath = Path(__file__).resolve().parent

    filepathforLogged = scriptpath / "Logged"

    filepathforLogged.mkdir(parents=True, exist_ok=True)

    filepathforSS = scriptpath / "Logged" / "MousePOSScreenshots"

    filepathforSS.mkdir(parents=True, exist_ok=True)

    filepath2 = scriptpath / "Logged" / "LoggedKeysForDebug.txt"

    filepath3 = scriptpath / "Logged" / "LoggedMouseInputForDebug.txt"
    # 👆 for finding where the python file is saved on the device, will add a folder for all data being recorded. folder will be two text files and another folder for screenshots.

    for file in filepathforSS.glob("*.png"): # checks you MousePOSScreenshots folder for any .png files, then deletes them

        file.unlink() # deletes the .png files

    # Keyboard debug 👇
    def key_press(key):
        try:
            print('{0}'.format(key)) # dectects key presses
            LogList.append('{0}'.format(key)) # adds pressed keys into a list
        except AttributeError:
            print('{0}'.format(key))# detects pressed special keys
            LogList.append('{0}'.format(key)) # adds pressed keys into a list


    def key_release(key):
        print('{0} released'.format(key))# detects when key is released
        if LogListAppend == 1:
            LogList.append('{0}~'.format(key)) # adds released key to list
        else:
            pass

        if key == keyboard.Key.end:
            LogList.append('Log exit initiated.')
            loop.call_soon_threadsafe(stop_event.set)
            # end key calls stop_event as to stop the asyncio loop
    # Keyboard debug 👆

    # Mouse debug 👇
    def Mouse_move(x,y):
        if StopMousePrint == 1:
            print('Mouse moved to {}'.format((x,y))) # detects when mouse is being moved
        else:
            pass

    def Mouse_click(x, y, button, pressed):
        print('{} at {}, it was a {}'.format('Pressed' if pressed else 'Released', (x, y), button)) # detects when mouse is clicked and where it is

        MouseLogList.append('{} at {}'.format('Pressed' if pressed else 'Released', (x,y))) # adds the position of click and type of click to a list that will be added to a file later
        global Press
        if pressed == True:
            Press = 'Pressed'
        else:
            Press = 'Released'
        global Click
        if button == button.left or button.right:

           x, y = pyautogui.position() # gets mouse position

           Screenshot = pyautogui.screenshot() # takes a screenshot of the screen

           convert_to_BW = Screenshot.convert("L") # converts the screenshot to Black and White

           draw = ImageDraw.Draw(convert_to_BW)

           draw.ellipse([x - r, y - r, x + r, y + r], outline='yellow', width=2) # draws a yellow circle around where the mouse would be in the screenshot

           convert_to_BW.save(filepathforSS / f"{Press}{Click}.png") # saves the screenshot to a folder on my computer

           Click = Click + 1 # for changing the name of screenshot in file

    # Mouse Debug 👆

    # Main function 👇
    async def Main():
        global stop_event, loop

        stop_event = asyncio.Event() # creates an event to be later used to exit asyncio loop

        loop = asyncio.get_running_loop() # used to call stop_event later

        await stop_event.wait() #awaits stop_event to be called to exit the loop

        print('Exiting Logger...')

        listener.stop()

        Mlistener.stop()

        await asyncio.sleep(0.5) #sleeps for 0.5 seconds before exiting the program
    #Main function 👆

# Main function runner i guess 👇
    while True:
        listener = keyboard.Listener(
            on_press=key_press,
            on_release=key_release) # defines the keyboard inputs as a variable for keyboard.listener
        listener.start() #starts the keyboard listener

        Mlistener = mouse.Listener(
            on_move=Mouse_move,
            on_click=Mouse_click) # defines the mouse inputs as a variable for mouse.listener
        Mlistener.start() # starts mouse listener

        try:
            asyncio.run(Main()) # runs the input detection loop
            #if delete key is pressed, function finishes loop, stops listener, and breaks the while loop.
            listener.stop()
            Mlistener.stop()
            break
        except KeyboardInterrupt:
            print('Failed to raise KeyboardInterrupt exception. Continuing.') #prevents KeyboardInterrupt exception
            listener.stop()
            time.sleep(0.01)
# Main function runner i guess 👆


# .txt file saver 👇
    with open(filepath2, "w") as file:
            file.write(f'{", ".join(LogList)}') # creates/overwrites a file named Logged.txt in folder named Logged wherever you saved the python file

    with open(filepath3, "w") as file:
        file.write(f'{", ".join(MouseLogList)}') # creates/overwrites a file named Logged.txt in folder named Logged wherever you saved the python file
# .txt file saver 👆

# Module detector 👇
except ModuleNotFoundError as MissingModule:
    print(f'{MissingModule}. Please install the missing module with "pip install {str(MissingModule)[17:-1]}"')
# Module detector 👆

# playback feature?
# better format on tkinter?
