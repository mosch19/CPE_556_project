from threading import Thread
from Queue import Queue, Empty
from Tkinter import *
import time
import tkMessageBox
import sensor

class App(Frame):
    def __init__(root, master):
        Frame.__init__(root, master)
        master.geometry('{}x{}'.format(400, 280))
        master.resizable(width=True, height=True)
        master.minsize(width=375, height=300)
        master.maxsize(width=375, height=300)
        root.pack(expand=Y, fill=BOTH)
        
        root.create_widgets()
        root.s = sensor.SensorInput()
        root.sensorUpdate = True
        root.stopped = False

    def create_widgets(root):
        frame = Frame(root, name="main")
        frame.pack(side=TOP, fill=BOTH, expand=Y)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        w = 10
        h = 5
        root.colors = ['IndianRed2', 'SpringGreen3', 'CadetBlue3', 'Gray66', 'Yellow2', 'Coral']

        legend = LabelFrame(frame, text="Legend")

        legendLabel0 = Label(legend, text="Heat", fg="red").pack(side=LEFT, expand=True, anchor="n")
        legendLabel1 = Label(legend, text="AC", fg="blue").pack(side=LEFT, expand=True, anchor="n")
        legendLabel2 = Label(legend, text="Light on", fg="yellow").pack(side=RIGHT, expand=True, anchor="n")
         
        legend.pack(fill=X, anchor="nw", padx=5)

        controlFrame = Frame(frame)
        controlFrame.grid_columnconfigure(0, weight=1)
        controlFrame.grid_columnconfigure(1, weight=1)

        root.ac_status = Button(controlFrame, width = w, height = h, state="disabled", bg=root.colors[3])
        root.ac_status.grid(row=0, column=0)
        root.light_status = Button(controlFrame, width = w, height = h, state = "disabled", bg=root.colors[3])
        root.light_status.grid(row = 0, column=1)

        Label(controlFrame, text="AC Status").grid(row=1, column=0)
        Label(controlFrame, text="Room Light").grid(row=1, column=1)

        Button(controlFrame, text="Room Light On", command=root.light_on, bg=root.colors[4]).grid(row=2, column=0, padx=5, pady=10)
        Button(controlFrame, text="Room Light Off", command=root.light_off, bg=root.colors[3]).grid(row=2, column=1, padx=5, pady=10)

        Button(controlFrame, text="AC On", command=root.air_on, bg=root.colors[2]).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=10)
        Button(controlFrame, text="Temp Off", command=root.ac_off, bg=root.colors[3]).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        Button(controlFrame, text="Heat On", command=root.heat_on, bg=root.colors[0]).grid(row=3, column=0, columnspan=2, sticky="e", padx=5, pady=10)

        Button(controlFrame, text="Auto", command=root.start, bg=root.colors[3]).grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=10)
        Button(controlFrame, text="Help", command=root.help, bg=root.colors[1]).grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        Button(controlFrame, text="Stop", command=root.stop, bg=root.colors[0]).grid(row=4, column=0, columnspan=2, sticky="e", padx=5, pady=10)
        
        controlFrame.pack(expand=True, fill=BOTH, pady=10)

    def sensor_update(root, q):
        root.s.auto()
        while root.sensorUpdate:
            q.put(root.s.get_status())
            time.sleep(.1)

    def start(root):
        # It fails if you start auto then stop then start again. The queue outpus nothing
        if root.stopped:
            root.s.restart()
            root.sensorUpdate = True
            root.stopped = False
        q = Queue()
        thread = Thread(target=root.sensor_update, args=(q,))
        thread.setDaemon(True)
        thread.start()
        while thread.isAlive():
            root.update()
            try:
                line = q.get_nowait()
                root.light_status.configure(bg=root.colors[4]) if line[0] else root.light_status.configure(bg=root.colors[3])
                if line[1]:
                    root.ac_status.configure(bg=root.colors[0])
                elif line[2]:
                    root.ac_status.configure(bg=root.colors[2])
                else:
                    root.ac_status.configure(bg=root.colors[3])
            except Empty:
                pass

    def stop(root):
        root.stopped = True
        root.sensorUpdate = False
        root.s.stop()

    def light_on(root):
        if root.stopped:
            root.s.restart()
            root.stopped = False
            root.sensorUpdate = True
        root.s.light_on()

    def light_off(root):
        if not root.stopped:
            root.s.light_off()

    def air_on(root):
        if root.stopped:
            root.s.restart()
            root.stopped = False
            root.sensorUpdate = True
        root.s.air_on()

    def heat_on(root):
        if root.stopped:
            root.s.restart()
            root.stopped = False
            root.sensorUpdate = True
        root.s.heat_on()

    def ac_off(root):
        if not root.stopped:
            root.s.ac_off()

    def help(root):
        tkMessageBox.showinfo("Help",
        "Auto mode will adjust your temp/lights based on movement & measured temp.\n\n"
        + "The AC/lights can also be manually changed with the buttons")

    def run(root):
        root.mainloop()

root = Tk()
root.title("Home Manager")
app = App(root)
app.run()
