import grovepi
import requests
import tkinter
from PIL import Image, ImageTk

#Setup Grove Pins
led = 5
grovepi.pinMode(led, "OUTPUT")

relay = 6
grovepi.pinMode(relay, "OUTPUT")

#Animation variables
fan_on = False
fan_count = 1

#Function Definitions
def classify(text):
    """
    This function will pass your text to the machine learning model and return the top result with the highest confidence
    """
    key = "ce582c70-7c25-11e9-803f-7dddc094c816388cabf8-47c9-4dde-9c57-ee4932edcc72"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

def submitButtonPressed():
    global fan_on

    user_input = textbox.get()
    print(user_input)
    textbox.delete(0, 'end')
    class_request = classify(user_input)

    label = class_request["class_name"]
    confidence = class_request["confidence"]

    print ("result: '%s' with %d%% confidence" % (label, confidence))
    
    if label == 'lamp_on':
        lamp.config(image = lamp_on_pic)
        lamp.image = lamp_on_pic
        grovepi.digitalWrite(led, 1)
    elif label == 'lamp_off':
        lamp.config(image = lamp_off_pic)
        lamp.image = lamp_off_pic
        grovepi.digitalWrite(led, 0)
    elif label == 'fan_on':
        fan_on = True
        grovepi.digitalWrite(relay, 1)
    elif label == 'fan_off':
        fan_on = False
        grovepi.digitalWrite(relay, 0)

def voiceButtonPressed():
    print("Button Pressed")
    print("Feature not yet implemented.")

def fanloop():
    global fan_on
    global fan_count

    if fan_on:
        if fan_count == 1:
            fan_count = 2
            fan.config(image = fan_pic2)
            fan.image = fan_pic2
        elif fan_count == 2:
            fan_count = 3
            fan.config(image = fan_pic3)
            fan.image = fan_pic3
        elif fan_count == 3:
            fan_count = 4
            fan.config(image = fan_pic4)
            fan.image = fan_pic4
        elif fan_count == 4:
            fan_count = 1
            fan.config(image = fan_pic1)
            fan.image = fan_pic1

    root.after(20, fanloop)

#GUI Event Loop Begins
root = tkinter.Tk()
root.title("Smart Classroom")
#root.wm_iconbitmap("ML4K-icon.ico")
root.minsize(width = 700, height = 600)
root.maxsize(width = 700, height = 600)

#Load all pictures
load = Image.open("fan-1.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic1 = ImageTk.PhotoImage(load)

load = Image.open("fan-2.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic2 = ImageTk.PhotoImage(load)

load = Image.open("fan-3.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic3 = ImageTk.PhotoImage(load)

load = Image.open("fan-4.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic4 = ImageTk.PhotoImage(load)

load = Image.open("lamp-off.png")
load = load.resize((400, 300),Image.ANTIALIAS)
lamp_off_pic = ImageTk.PhotoImage(load)

load = Image.open("lamp-on.png")
load = load.resize((400, 300),Image.ANTIALIAS)
lamp_on_pic = ImageTk.PhotoImage(load)

load = Image.open("Circle-icons-mic.png")
load = load.resize((100, 100),Image.ANTIALIAS)
mic_icon = ImageTk.PhotoImage(load)

#Setup GUI Objects
fan = tkinter.Label(root, image = fan_pic1)
fan.image = fan_pic1
fan.grid(row = 0, column = 0)

lamp = tkinter.Label(root, image = lamp_off_pic)
lamp.image = lamp_off_pic
lamp.grid(row = 0, column = 2, sticky = tkinter.S)

shelf = tkinter.Label(root, height = 2, width = 100, bg = "#964B00").grid(row = 1, column = 0, columnspan = 3)

spacer1 = tkinter.Label(root, height = 2).grid(row = 2, column = 0)
spacer2 = tkinter.Label(root, height = 2).grid(row = 5, column = 0)

textbox_frame = tkinter.Frame(root)
textbox_frame.grid(row = 4, column = 0, columnspan = 3)

textbox = tkinter.Entry(textbox_frame, width = 50)
textbox.pack(side = tkinter.LEFT)
textbox.bind("<Return>", (lambda event: submitButtonPressed()))

submit_text_button = tkinter.Button(textbox_frame, text = "Submit", command = submitButtonPressed).pack(side = tkinter.LEFT)

voice_button = tkinter.Button(root, image = mic_icon, command = voiceButtonPressed).grid(row = 6, column = 0, columnspan = 3)

root.after(20, fanloop) #Fan Animation

root.mainloop()

