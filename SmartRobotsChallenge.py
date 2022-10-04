from tkinter import *
from tkinter import filedialog

from PIL import Image
from PIL import ImageTk

import cv2
import imutils

from keras.models import load_model

import numpy as np

import time
import serial.tools.list_ports

class App:
    def __init__(self):
        self.cap = None
        self.model = None
        self.class_names = None
        self.arduino = None
        self.connected = False
        self.move = None
        self.stop = False
        self.root = Tk()

    def start(self):
        self.widgets()
        self.root.title("Smart Robots Challenge")
        self.root.iconphoto(False, PhotoImage(file='icon.png'))
        self.root.mainloop()

    def widgets(self):
        self.btnLabels = Button(self.root, text="Elegir archivo de clases", command=self.readLabels)
        self.btnLabels.grid(column=0, row=0, padx=5, pady=5, columnspan=2)

        self.lblLabels = Label(self.root, text="Clases:")
        self.lblLabels.grid(column=2, row=0)

        self.lblLabelsPath = Label(self.root, text="Aún no se ha seleccionado archivo")
        self.lblLabelsPath.grid(column=3, row=0, columnspan=3)

        self.btnModel = Button(self.root, text="Elegir archivo de modelo", command=self.readModel)
        self.btnModel.grid(column=0, row=1, padx=5, pady=5, columnspan=2)

        self.lblModel = Label(self.root, text="Modelo:")
        self.lblModel.grid(column=2, row=1)

        self.lblModelPath = Label(self.root, text="Aún no se ha seleccionado archivo")
        self.lblModelPath.grid(column=3, row=1, columnspan=3)

        self.btnStart = Button(self.root, text="Encender video", width=45, command=self.startVideo)
        self.btnStart.grid(column=0, row=2, padx=5, pady=5, columnspan=3)

        self.btnFinish = Button(self.root, text="Apagar video", width=45, command=self.finishVideo)
        self.btnFinish.grid(column=3, row=2, padx=5, pady=5, columnspan=3)

        self.lblVideo = Label(self.root)
        self.lblVideo.grid(column=0, row=3, columnspan=3, rowspan=4)

        self.lblClassName_ = Label(self.root, text="Predicción")
        self.lblClassName_.grid(column=3, row=3, rowspan=1, sticky=S)

        self.lblClassName = Label(self.root, text="-",)
        self.lblClassName.grid(column=3, row=4, rowspan=1, sticky=N)

        self.lblClassPercentage_ = Label(self.root, text="Porcentaje")
        self.lblClassPercentage_.grid(column=3, row=5, rowspan=1, sticky=S)

        self.lblClassPercentage = Label(self.root, text="-")
        self.lblClassPercentage.grid(column=3, row=6, rowspan=1, sticky=N)

        self.lblTolerance = Label(self.root, text="Tolerancia")
        self.lblTolerance.grid(column=4, row=3, sticky=S)

        self.tolerance = DoubleVar(value=0.75)
        self.sliderTolerance = Scale(self.root, from_=0.5, to=1, resolution=0.05, variable=self.tolerance, length=300)
        self.sliderTolerance.grid(column=4, row=4, rowspan=3)

        self.btnRefresh = Button(self.root, text="Refrescar", command=self.refresh)
        self.btnRefresh.grid(column=5, row=3, padx=5, pady=5)

        self.btnConnect = Button(self.root, text="Conectar", command=self.connect)
        self.btnConnect.grid(column=5, row=4, padx=5, pady=5)

        self.listPorts = Listbox(self.root)
        self.listPorts.grid(column=5, row=5)

        self.lblPortConnection = Label(self.root, text="Sin conexión")
        self.lblPortConnection.grid(column=5, row=6)

    def readLabels(self):
        labels_path = filedialog.askopenfilename(filetypes=[("txt files", "*.txt")])
        
        if len(labels_path) > 0:
            with open(labels_path) as f:
                self.class_names = f.readlines()
            self.class_names = [line[2:-1] for line in self.class_names]
            self.lblLabelsPath.configure(text=" - ".join(self.class_names))

        else:
            self.lblLabelsPath.configure(text="Aún no se ha seleccionado archivo")
            self.class_names = None

    def readModel(self):
        model_path = filedialog.askopenfilename(filetypes=[("model files", "*.h5")])
        
        if len(model_path) > 0:
            self.model = load_model(model_path)
            model_path_txt = model_path.split("/")[-1]
            self.lblModelPath.configure(text=model_path_txt)

        else:
            self.lblModelPath.configure(text="Aún no se ha seleccionado archivo")
            self.model = None

    def startVideo(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.visualize()

    def finishVideo(self):
        self.cap.release()
        self.lblClassName.configure(fg="black")
        self.lblClassName.configure(text="-")
        self.lblClassPercentage.configure(text="-")

    def refresh(self):
        self.listPorts.delete(0, END)
        ports = [comport.device for comport in serial.tools.list_ports.comports()]
        for i, port in enumerate(ports):
            self.listPorts.insert(i, port)

    def connect(self):
        if self.connected:
            self.arduino.close()
            self.arduino = None
            self.connected = False
            self.btnConnect.configure(text="Conectar")
            self.lblPortConnection.configure(text="Sin conexión")
            return
            
        if len(self.listPorts.curselection())!=0:
            self.port = self.listPorts.get(self.listPorts.curselection()[0])
            try:
                self.arduino = serial.Serial(self.port, 9600)
                self.arduino.timeout=0
                self.arduino.write_timeout=0.01
                time.sleep(2)
                self.lblPortConnection.configure(text="Conectado a " + self.port)
                self.btnConnect.configure(text="Desconectar")
                self.connected = True
            except:
                self.lblPortConnection.configure(text="Conexión Fallida")
                return

    def visualize(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                h, w, c = frame.shape
                frame = frame[:,int((w-h)/2):int((w+h)/2),:]
                frame = imutils.resize(frame, width=360)

                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.lblVideo.configure(image=img)
                self.lblVideo.image = img

                if self.class_names is not None and self.model is not None:
                    frame = cv2.resize(frame, (224,224), interpolation = cv2.INTER_AREA)
                    img = frame.copy()
                    img.resize(1,224,224,3)
                    img = img / 255.
                    predictions = self.model.predict(img, verbose=0)
                    y_pred = np.argmax(predictions, axis=-1)
                    lab = y_pred[0]

                    if predictions[0][y_pred][0] >= self.tolerance.get():
                        self.lblClassName.configure(fg="green")
                        if (self.move != y_pred[0] or self.stop) and self.arduino is not None:
                            try:
                                self.arduino.write(str(y_pred[0]).encode())
                            except:
                                self.connect()
                                self.refresh()
                        self.move = y_pred[0]
                        self.stop = False
                    else:
                        self.lblClassName.configure(fg="red")
                        if self.arduino is not None:
                            if self.port not in [comport.device for comport in serial.tools.list_ports.comports()]:
                                self.connect()
                                self.refresh()
                            elif not self.stop:
                                self.stop = True
                                try:
                                    self.arduino.write(str(9).encode()) 
                                except:
                                    self.connect()
                                    self.refresh()
                                if self.arduino is not None:
                                    self.arduino.reset_input_buffer()
                                    self.arduino.reset_output_buffer()


                    self.lblClassName.configure(text=self.class_names[lab])
                    self.lblClassPercentage.configure(text="{:.2f}".format(predictions[0][y_pred][0]))
                else:
                    self.lblClassName.configure(fg="black")
                    self.lblClassName.configure(text="-")
                    self.lblClassPercentage.configure(text="-")

                self.lblVideo.after(10, self.visualize)

            else:
                self.lblVideo.image = ""
                self.cap.release()
        
    def __del__(self):
        if self.cap is not None:
            self.cap.release()
        if self.arduino is not None:
            self.arduino.close()


if __name__ == '__main__':
    app = App()
    app.start()