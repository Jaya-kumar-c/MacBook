from tkinter import *
from tkinter import ttk
from tkinter import ttk,messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil

#brightness
import screen_brightness_control as pct

#audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

#clock
from time import strftime

#calendar
from tkcalendar import*

#open google
import pyautogui 
import subprocess
import webbrowser as wb
import random


root=Tk()
root.title('Mac Window')
root.geometry("850x500+300+170")
root.resizable(False,False)
root.configure(bg='#181b1b')

#----------------------------------------------------------------------------------
#icon

image_icon=PhotoImage(file="image/monitor.png")
root.iconphoto(False,image_icon)
body=Frame(root,width=900,height=600,bg='#cce6ff')
body.pack(pady=20,padx=20)

#------------------------------------------------------------------------------------

LHS=Frame(body,width=310,height=435,bg='#ffffff',highlightbackground='#adacb1',highlightthickness=1)
LHS.place(x=10,y=10)

#-----------------------------------------------------------------------------------------
#Logo

photo=PhotoImage(file="image/Laptop.png")
myimage=Label(LHS,image=photo,background='#ffffff')
myimage.place(x=2,y=3)

my_system=platform.uname()

l1=Label(LHS,text=my_system.node,bg='#ffffff',font=("Acumin Variable Concept",15,'bold'),justify="center")
l1.place(x=20,y=205)

l2=Label(LHS,text=f"Version:{my_system.version}",bg='#ffffff',font=("Acumin Variable Concept",8,'bold'),justify="center")
l2.place(x=22,y=230)

l3=Label(LHS,text=f"System:{my_system.system}",bg='#ffffff',font=("Acumin Variable Concept",15,'bold'),justify="center")
l3.place(x=20,y=265)

l4=Label(LHS,text=f"Machine:{my_system.machine}",bg='#ffffff',font=("Acumin Variable Concept",15,'bold'),justify="center")
l4.place(x=20,y=290)

l5=Label(LHS,text=f"Total RAM installed:{round(psutil.virtual_memory().total/1000000000,2)} GB",bg='#ffffff',font=("Acumin Variable Concept",15,'bold'),justify="center")
l5.place(x=20,y=315)

l6=Label(LHS, text=f"Processor: {my_system.processor}\n{my_system.version}",
         bg='#ffffff', font=("Acumin Variable Concept",7,'bold'), justify="left", wraplength=280)
l6.place(x=22, y=345)

#--------------------------------------------------------------------------------------------

RHS=Frame(body,width=470,height=230,bg='#ffffff',highlightbackground='#adacb1',highlightthickness=1)
RHS.place(x=330,y=10)

system=Label(RHS,text='System',font=('Acumin Variable Concept',15),bg='#ffffff')
system.place(x=10,y=10)

#------------------------Battery-----------------------------

def convertTime(seconds):
    minutes,seconds=divmod(seconds,60)
    hours,minutes=divmod(minutes,60)
    return"%d:%02d:%02d:"% (hours,minutes,seconds)

def none():
    global battery_png
    global battery_lable
    battery=psutil.sensors_battery()
    percent=battery.percent
    time=convertTime(battery.secsleft)
    
    lbl.config(text=f"{percent}%")
    lbl_plug.config(text=f'Plug in:{str(battery.power_plugged)}')
    lbl_time.config(text=f'{time} remaining')
    
    battery_lable=Label(RHS,background='#ffffff')
    battery_lable.place(x=15,y=50)
    
    lbl.after(1000,none)
    
    if battery.power_plugged==True:
        battery_png=PhotoImage(file="image/charging.png")
        battery_lable.config(image=battery_png)
        
    else:
        battery_png=PhotoImage(file='image/battery.png')
        battery_lable.config(image=battery_png)
    

lbl=Label(RHS,font=('Acumin Variable Concept',40,'bold'),bg='#ffffff')
lbl.place(x=200,y=40)

lbl_plug=Label(RHS,font=('Acumin Variable Concept',10,'bold'),bg='#ffffff')
lbl_plug.place(x=20,y=100)

lbl_time=Label(RHS,font=('Acumin Variable Concept',15,'bold'),bg='#ffffff')
lbl_time.place(x=200,y=100)

none()

#------------------------------------Speaker-------------------------------------------

lbl_speaker=Label(RHS,text="Speaker:",font=('arial',10,'bold'),bg='#ffffff')
lbl_speaker.place(x=200,y=140)
volume_value=tk.DoubleVar()

def get_current_volume_value():
    return'{:.2f}'.format(volume_value.get())


def volume_changed(event):
    device=AudioUtilities.GetSpeakers()
    interface=device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume=cast(interface,POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()),None)
    
style=ttk.Style()
style.configure('TScale',background='#ffffff')

volume=ttk.Scale(RHS,from_=60,to=0,orient="horizontal",
                 command=volume_changed,variable=volume_value)

volume.place(x=290,y=140)
volume.set(20)

#---------------------------------------Brightness-------------------------------------

lbl_brightness=Label(RHS,text='Brightness:',font=('arial',10,'bold'),bg="#ffffff")
lbl_brightness.place(x=200,y=180)

current_value=tk.DoubleVar()

def get_current_value():
    return'{:.2f}'.format(current_value.get())

def brightness_changed(event):
    pct.set_brightness(get_current_value())
    
brightness=ttk.Scale(RHS,from_=0,to=100,orient='horizontal',
                     command=brightness_changed,variable=current_value)
brightness.place(x=290,y=180)

#-----------------------------------------Apps-----------------------------------------------

#----------------------------------------weather---------------------------------------------

def weather():
    app1=Toplevel()
    app1.geometry('850x500+300+170')
    app1.title('Weather')
    app1.configure(bg='#ffffff')
    app1.resizable(False,False)
    
    #icon
    image_icon=PhotoImage(file='image/logo.png')
    app1.iconphoto(False,image_icon)
    
    def getWeather():
        try:
            city=textfield.get()
            
            geolocator=Nominatim(user_agent="geoapiExercises")
            location=geolocator.geocode(city)
            obj= TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude,lat=location.latitude)
            
            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")
            
            
            # API key (replace with your own key)
            api_key = "c347cfab612069ce133f34e7be0aa01a"
            api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
            
            # Get weather data
            json_data = requests.get(api_url).json()

            if "current" in json_data:
                # Convert temperature to Celsius
                temperature = json_data['current']['temperature']
                weather_desc = json_data['current']['weather_descriptions'][0]
                wind_speed = json_data['current']['wind_speed']
                humidity = json_data['current']['humidity']
                pressure = json_data['current']['pressure']
                description = json_data['current']['weather_descriptions'][0]

                # Update the labels
                t.config(text=f"{temperature} °C")
                c.config(text=weather_desc)
                w.config(text=f"{wind_speed} km/h")
                h.config(text=f"{humidity} %")
                d.config(text=description)
                p.config(text=f"{pressure} hPa")
            else:
                messagebox.showerror("Weather App", "Invalid city name or API request failed!")

          
        except Exception as e:
            messagebox.showerror("Weather App","Invalid Entry!")
    
    #search box
    search_image=PhotoImage(file="image/search.png")
    myimage=Label(app1,image=search_image,bg='#ffffff')
    myimage.place(x=20,y=20)
    
    textfield=tk.Entry(app1,justify="center",width=17,font=("poppins",25,"bold"),bg="#404040",border=0,fg="white")
    textfield.place(x=50,y=40)
    textfield.focus()

    search_icon=PhotoImage(file="image/search icon.png")
    myimage=Button(app1,image=search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
    myimage.place(x=400,y=34)
    
    #logo
    logo_image=PhotoImage(file='image/logo.png')
    logo=Label(app1,image=logo_image,bg='#ffffff')
    logo.place(x=150,y=100)
    
    #bottom box
    Frame_image=PhotoImage(file='image/box.png')
    frame_myimage=Label(app1,image=Frame_image,bg='#ffffff')
    frame_myimage.pack(padx=5,pady=5,side=BOTTOM)
    
    #time
    name=Label(app1,font=("arial",15,'bold'),bg='#ffffff')
    name.place(x=30,y=100)
    clock=Label(app1,font=('Helvetica',20),bg='#ffffff')
    clock.place(x=30,y=130)
    
    #label
    label1=Label(app1,text="WIND",font=("Helvatice",15,'bold'),fg='white',bg="#1ab5ef")
    label1.place(x=120,y=400)
    
    label2=Label(app1,text="HUMIDITY",font=("Helvatice",15,'bold'),fg='white',bg="#1ab5ef")
    label2.place(x=250,y=400)
    
    label3=Label(app1,text="DESCRIPTION",font=("Helvatice",15,'bold'),fg='white',bg="#1ab5ef")
    label3.place(x=430,y=400)
    
    label4=Label(app1,text="PRESSURE",font=("Helvatice",15,'bold'),fg='white',bg="#1ab5ef")
    label4.place(x=650,y=400)
    
    t=Label(app1,font=('arial',70,'bold'),fg='#ee666d',bg='#ffffff')
    t.place(x=400,y=150)
    c=Label(app1,font=('arial',70,'bold'),bg='#ffffff')
    c.place(x=400,y=250)
    
    w=Label(app1,text="...",font=('arial',20,'bold'),bg='#1ab5ef')
    w.place(x=120,y=430)
    h=Label(app1,text="...",font=('arial',20,'bold'),bg='#1ab5ef')
    h.place(x=280,y=430)
    d=Label(app1,text="...",font=('arial',20,'bold'),bg='#1ab5ef')
    d.place(x=450,y=430)
    p=Label(app1,text="...",font=('arial',20,'bold'),bg='#1ab5ef')
    p.place(x=670,y=430)
    
    app1.mainloop()
#-----------------------------------------Clock-------------------------------------

def clock():
    app2=Toplevel()
    app2.geometry("850x110+300+10")
    app2.title('Clock')
    app2.configure(bg='#181b1b')
    app2.resizable(False,False)
    
    
    #icon
    image_icon=PhotoImage(file="image/app2.png")
    app2.iconphoto(False,image_icon)

    def clock():
        text=strftime('%H:%M:%S %p')
        lbl.config(text=text)
        lbl.after(1000,clock)
        
    lbl=Label(app2,font=('digital-7',50,'bold'),width=20,bg='#ffffff',fg='#181b1b')
    lbl.pack(anchor='center',pady=20)
    clock()    
        
    app2.mainloop()

#---------------------------------------------------Calendar---------------------------

def calendar():
    app3=Toplevel()
    app3.geometry('300x300+-10+10')
    app3.title('Calendar')
    app3.configure(bg='#181b1b')
    app3.resizable(False,False)
    
    #icon
    image_icon=PhotoImage(file='image/app3.png')
    app3.iconphoto(False,image_icon)
    
    mycal=Calendar(app3,setmode='day',date_pattern='d/m/yy')
    mycal.pack(padx=15,pady=35)
    
    app3.mainloop()

#------------------------------------------mode-------------------------------------------------------------

button_mode=True

def mode():
    global button_mode
    if button_mode:
        LHS.config(bg='#181b1b')
        myimage.config(bg='#181b1b')
        l1.config(bg='#181b1b',fg="#cce6ff")
        l2.config(bg='#181b1b',fg="#cce6ff")
        l3.config(bg='#181b1b',fg="#cce6ff")
        l4.config(bg='#181b1b',fg="#cce6ff")
        l5.config(bg='#181b1b',fg="#cce6ff")
        l6.config(bg='#181b1b',fg="#cce6ff")
        
        RHB.config(bg='#181b1b')
        app1.config(bg='#181b1b')
        app2.config(bg='#181b1b')
        app3.config(bg='#181b1b')
        app4.config(bg='#181b1b')
        app5.config(bg='#181b1b')
        app6.config(bg='#181b1b')
        app7.config(bg='#181b1b')
        app8.config(bg='#181b1b')
        app9.config(bg='#181b1b')
        app10.config(bg='#181b1b')
        apps.config(bg='#181b1b',fg='#cce6ff')
                
        button_mode=False
        
    else:
        LHS.config(bg='#ffffff')
        myimage.config(bg='#ffffff')
        l1.config(bg='#ffffff',fg='#181b1b')
        l2.config(bg='#ffffff',fg='#181b1b')
        l3.config(bg='#ffffff',fg='#181b1b')
        l4.config(bg='#ffffff',fg='#181b1b')
        l5.config(bg='#ffffff',fg='#181b1b')
        l6.config(bg='#ffffff',fg='#181b1b')
        
        RHB.config(bg="#ffffff")
        app1.config(bg='#ffffff')
        app2.config(bg='#ffffff')
        app3.config(bg='#ffffff')
        app4.config(bg='#ffffff')
        app5.config(bg='#ffffff')
        app6.config(bg='#ffffff')
        app7.config(bg='#ffffff')
        app8.config(bg='#ffffff')
        app9.config(bg='#ffffff')
        app10.config(bg='#ffffff')
        apps.config(bg='#ffffff',fg='#181b1b')        
        button_mode=True

#----------------------------------------game---------------------------------------------------------

def game():
    app9=Toplevel()
    app9.geometry("300x500+1170+170")
    app9.title('Ludo')
    app9.configure(bg='#ffffff')
    app9.resizable(False,False)
    
    #icon
    image_icon=PhotoImage(file='image/app9.png')
    app9.iconphoto(False,image_icon)
    
    ludo_image=PhotoImage(file='image/ludo back.png')
    Label(app9,image=ludo_image).pack()
    
    label=Label(app9,text='',font=('times',150))
    
    def roll():
        dice=['\u2680','\u2681','\u2683','\u2684','\u2685']
        label.configure(text=f'{random.choice(dice)}{random.choice(dice)}',fg="#181b1b")
        label.pack()
    
    btn_image=PhotoImage(file='image/ludo button.png')
    btn=Button(app9,image=btn_image,bd=0,relief='flat',highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=roll)
    btn.pack(padx=10,pady=10)
     
    app9.mainloop()

#---------------------------------------------screenshot-------------------------------------------

def screenshot():
    root.iconify()
    
    myscreenshot=pyautogui.screenshot()
    file_path=filedialog.asksaveasfilename(defaultextension='.png')
    myscreenshot.save(file_path)

#------------------------------------------------file-------------------------------------------

def file():
    subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
    
def chrome():
    wb.register('chrome',None)
    wb.open('https://www.google.com/')

def youtube():
    wb.register('youtube',None)
    wb.open('https://www.youtube.com/')

def googlemap():
    wb.register('googlemap',None)
    wb.open('https://www.google.com/maps')

#------------------------------------------------------------------------------------------------------

RHB=Frame(body,width=470,height=190,bg='#ffffff',highlightbackground='#adacb1',highlightthickness=1)
RHB.place(x=330,y=255)

apps=Label(RHB,text="Apps",font=('Acumin Variable Concept',15),bg='#ffffff')
apps.place(x=10,y=10)

app1_image = PhotoImage(file='image/app1.png')
app1=Button(RHB,image=app1_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff', command=weather)
app1.place(x=15, y=50)

app2_image=PhotoImage(file='image/app2.png')
app2=Button(RHB,image=app2_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=clock)
app2.place(x=100,y=50)

app3_image=PhotoImage(file='image/app3.png')
app3=Button(RHB,image=app3_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=calendar)
app3.place(x=185,y=50)

app4_image=PhotoImage(file='image/app4.png')
app4=Button(RHB,image=app4_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=screenshot)
app4.place(x=270,y=50)

app5_image=PhotoImage(file='image/app5.png')
app5=Button(RHB,image=app5_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=mode)
app5.place(x=355,y=50)

app6_image=PhotoImage(file='image/app6.png')
app6=Button(RHB,image=app6_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=file)
app6.place(x=15,y=120)

app7_image=PhotoImage(file='image/app7.png')
app7=Button(RHB,image=app7_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=chrome)
app7.place(x=100,y=120)

app8_image=PhotoImage(file='image/app8.png')
app8=Button(RHB,image=app8_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=youtube)
app8.place(x=185,y=120)

app9_image=PhotoImage(file='image/app9.png')
app9=Button(RHB,image=app9_image,bd=0,relief='flat', highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=game)
app9.place(x=270,y=122)

app10_image=PhotoImage(file='image/app10.png')
app10=Button(RHB,image=app10_image,bd=0,relief='flat',highlightthickness=0, bg='#ffffff', activebackground='#ffffff',command=googlemap)
app10.place(x=355,y=120)

root.mainloop()