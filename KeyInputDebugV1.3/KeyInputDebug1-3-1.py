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

    StartMousePrint = False

    LogListAppend = False

    StartKeyPrintInTerm = False

    StartClickPOSPrint = False

    ClickShot = True
    # Variables 👆

    # 👇 cool little gui so you know when code will start
    root = tk.Tk()

    root.title("Menu")

    root.geometry("290x450")

    root.config(bg="DeepSkyBlue4")

    def stopcode():
        sys.exit()

    def StartMousePOS():
        global StartMousePrint
        StartMousePrint = True
        MousePOSPrint.config(text="Disable MousePOS Print", font=("Calibri", 10), width=25, height=1, command=StopMousePOS)

    def StopMousePOS():
        global StartMousePrint
        StartMousePrint = False
        MousePOSPrint.config(text="Enable MousePOS Print", font=("Calibri", 10), width=25, height=1, command=StartMousePOS)

    def EnableRelease():
        global LogListAppend
        LogListAppend = True
        ReleaseAppend.config(text="Disable Release Append", font=("Calibri",10), width=25, height=1, command=DisableRelease)

    def DisableRelease():
        global LogListAppend
        LogListAppend = False
        ReleaseAppend.config(text="Enable Release Append", font=("Calibri",10), width=25, height=1, command=EnableRelease)

    def StartKeyPrint():
        global StartKeyPrintInTerm
        StartKeyPrintInTerm = True
        KeyPrintInTerm.config(text="Disable Key Input Print", font=("Calibri",10), width=25, height=1, command=StopKeyPrint)

    def StopKeyPrint():
        global StartKeyPrintInTerm
        StartKeyPrintInTerm = False
        KeyPrintInTerm.config(text="Enable Key Input Print", font=("Calibri",10), width=25, height=1, command=StartKeyPrint)

    def StartClickPrint():
        global StartClickPOSPrint
        StartClickPOSPrint = True
        ClickPosPrintButton.config(text="Disable ClickPOS Print", font=("Calibri",10), width=25, height=1, command=StopClickPrint)

    def StopClickPrint():
        global StartClickPOSPrint
        StartClickPOSPrint = False
        ClickPosPrintButton.config(text="Enable ClickPOS Print", font=("Calibri",10), width=25, height=1, command=StartClickPrint)

    def TakeClickSS():
        global ClickShot
        ClickShot = True
        ClickShotsButton.config(text="Disable Click ScreenShots", font=("Calibri",10), width=25, height=1, command=DontTakeClickSS)

    def DontTakeClickSS():
        global ClickShot
        ClickShot = False
        ClickShotsButton.config(text="Enable Click ScreenShots", font=("Calibri",10), width=25, height=1, command=TakeClickSS)


    EndLabel = tk.Label(root, text="(Press 'end' key to stop code once running)", font=("Calibri", 8), width=35, height=1, bg="DeepSkyBlue4")
    EndLabel.grid(row=0, column=0, padx=2, pady=2)

    buttonframe = tk.Frame(root, bg="black", bd=1)
    buttonframe.grid(row=1, column=0, padx=2, pady=2)

    ReleaseAppend = tk.Button(buttonframe, text="Enable Released Append", font=("Calibri", 10), width=25, height=1, command=EnableRelease)
    ReleaseAppend.grid(row=1, column=0, padx=2, pady=2)

    KeyPrintInTerm = tk.Button(buttonframe, text="Enable Key Input Print", font=("Calibri", 10), width=25, height=1, command=StartKeyPrint)
    KeyPrintInTerm.grid(row=2, column=0, padx=2, pady=2)

    MousePOSPrint = tk.Button(buttonframe, text="Enable MousePOS Print", font=("Calibri", 10), width=25, height=1, command=StartMousePOS)
    MousePOSPrint.grid(row=3, column=0, padx=2, pady=2)

    ClickPosPrintButton = tk.Button(buttonframe, text="Enable ClickPOS Print", font=("Calibri", 10), width=25, height=1, command=StartClickPrint)
    ClickPosPrintButton.grid(row=4, column=0, padx=2, pady=2)

    ClickShotsButton = tk.Button(buttonframe, text="Disable Click ScreenShots", font=("Calibri", 10), width=25, height=1, command=DontTakeClickSS)
    ClickShotsButton.grid(row=5, column=0, padx=2, pady=2)

    startbutton = tk.Button(buttonframe, text="Begin", font=("Calibri", 18), width=14, height=1, command=root.destroy)
    startbutton.grid(row=6, column=0, padx=2, pady=2)

    StopCodebutton = tk.Button(buttonframe, text="Cancel", font=("Calibri", 18), width=14, height=1,  command=stopcode)
    StopCodebutton.grid(row=7, column=0, padx=2, pady=2)

    root.resizable(False, False)

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
            if StartKeyPrintInTerm == True:
                print('{0}'.format(key.char)) # dectects key presses
            LogList.append('{0}'.format(key.char)) # adds pressed keys into a list

            if key == keyboard.Key.end:
                LogList.append('Log exit initiated.')
                loop.call_soon_threadsafe(stop_event.set)

        except AttributeError:
            if StartKeyPrintInTerm == True:
                print(f'{str(key)[4:]}')# detects pressed special keys
            LogList.append(f'{str(key)[4:]}') # adds pressed keys into a list

            if key == keyboard.Key.end:
                LogList.append('Log exit initiated.')
                loop.call_soon_threadsafe(stop_event.set)

    def key_release(key):
        try:
            if StartKeyPrintInTerm == True:
                print('{0} released'.format(key.char))# detects when key is released
            if LogListAppend == True:
                LogList.append('{0}~'.format(key.char)) # adds released key to list
            else:
                pass
        except AttributeError:
            if StartKeyPrintInTerm == True:
                print(f'{str(key)[4:]} released')# detects when key is released
            if LogListAppend == True:
                LogList.append(f'{str(key)[4:]}')

            # end key calls stop_event as to stop the asyncio loop
    # Keyboard debug 👆

    # Mouse debug 👇
    def Mouse_move(x,y):
        if StartMousePrint == True:
            print('Mouse moved to {}'.format((x,y))) # detects when mouse is being moved
        else:
            pass

    def Mouse_click(x, y, button, pressed):
        if StartClickPOSPrint == True:
            print('{} at {}, it was a {}'.format('Pressed' if pressed else 'Released', (x, y), button)) # detects when mouse is clicked and where it is

        MouseLogList.append('{} at {}'.format('Pressed' if pressed else 'Released', (x,y))) # adds the position of click and type of click to a list that will be added to a file later
        if ClickShot == True:
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
