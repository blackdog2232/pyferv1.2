import customtkinter
from threading import *
import socket
import os 
import sys
from tkinter import filedialog
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("PYFER")
loggername = "pylogger.log"
formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
file_handler = logging.FileHandler(loggername)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("325x570")
app.minsize(325,570)
app.maxsize(325,570)
con_status = 0
send_button_stat = 0
connect_again = 0
complete_label_stat = False
error1_label_stat = False
error2_label_stat = False
sendbutton_checker=False
second_start = False
recfailed_stat = False
reccomplete_stat = False

class connection(Thread):
     def run(self):
          while True:
               try:
                    global s
                    host = user_hostnameinput
                    port = 9999
                    s = socket.socket()
                    s.connect((host, port))
                    print("[+] Connected.")
                    logger.info("Connected")
                    constatus_label.configure(text="Connected",text_color=("#00ff00"))
                    global con_status
                    con_status = 1
                    global connect_again
                    hostbutton_1.configure(state="disabled")
                    hostname_entry.configure(state="disabled")
                    break
               except socket.gaierror as e:
                    print("getaddrinfo failed: [Errno {}] {}".format(e.errno, e.strerror))
                    constatus_label.configure(text=e,text_color=("#ff3333"))
                    logger.warning(e)
                    con_status = 0
                    s.close()
               except ConnectionRefusedError:
                    constatus_label.configure(text="Waiting for Receiver to connect",text_color=("#00ccff"))
                    logger.warning("Receiver Disconnected")
                    con_status = 0
                    s.close()
          
class interface(Thread):
     def run(self):
          app.title("pyFer v1.2")
          global segmented_button_1
          segmented_button_1 = customtkinter.CTkSegmentedButton(master=app, values=["Send file(s)", "Receive file(s)"], command=segmented_button_callback,width=200)
          segmented_button_1.pack(padx=10, anchor="n",pady=6)
          global mainframe_1
          mainframe_1 = customtkinter.CTkFrame(master=app)
          mainframe_1.pack(pady=3, padx=10, fill="both", expand=True)
          global pyferbutton_1
          pyferbutton_1 = customtkinter.CTkButton(master=app,text="Pyfer v1.2",fg_color="transparent",state="disabled",width=250)
          pyferbutton_1.pack(fill="x")
          logger.info("Interface displayed")

def segmented_button_callback(value):
    print("segmented button clicked:", value)
    segmented_button_1.configure(state="disabled")
    if value == "Send file(s)":
         sf()
         logger.info("send file option selected")
    else:
         rf()
         logger.info("Receive option selected")

def sf():
     pyferbutton_1.destroy()
     hostname_frame = customtkinter.CTkFrame(master=mainframe_1)
     hostname_frame.pack()
     global hostname_entry
     hostname_entry = customtkinter.CTkEntry(master=hostname_frame, placeholder_text="Enter hostname of receiver",width=200)
     hostname_entry.pack(side=customtkinter.LEFT,anchor="n",padx=3,pady=6)
     global hostbutton_1
     hostbutton_1 = customtkinter.CTkButton(master=hostname_frame, command=hostname_callback,text="Submit")
     hostbutton_1.pack(side=customtkinter.LEFT,padx=3,anchor="n",pady=6)
     browse_frame = customtkinter.CTkFrame(master=mainframe_1,border_color="black",width=150)
     browse_frame.pack(pady=6, padx=10)
     browse_label = customtkinter.CTkLabel(master=browse_frame,text="Select file",font=("Arial",15))
     browse_label.pack(padx=3,pady=3,side=customtkinter.LEFT)
     global browse_button
     browse_button = customtkinter.CTkButton(browse_frame,text="Browse file", width=20, command=upload_file)
     browse_button.pack(padx=3,pady=3,side=customtkinter.RIGHT)
     global fdetails_frame
     fdetails_frame = customtkinter.CTkFrame(master=mainframe_1)
     fdetails_frame.pack(pady=10,padx=10,anchor="w", fill="both", expand=True)
     namedetails_frame = customtkinter.CTkFrame(master=fdetails_frame,fg_color="transparent")
     namedetails_frame.pack(anchor="w")
     namelabel_1 = customtkinter.CTkLabel(master=namedetails_frame,text="Name:", font=("Bold",20))
     namelabel_1.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global file_label
     file_label = customtkinter.CTkLabel(master=namedetails_frame,text="",font=("Bold",15))
     file_label.pack(after=namelabel_1,side=customtkinter.RIGHT)
     sizedetails_frame = customtkinter.CTkFrame(master=fdetails_frame,fg_color="transparent")
     sizedetails_frame.pack(anchor="w")
     namesizelabel_1 = customtkinter.CTkLabel(master=sizedetails_frame,text="Size:", font=("Bold",20))
     namesizelabel_1.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global size_label
     size_label = customtkinter.CTkLabel(master=sizedetails_frame,text="",font=("Bold",18))
     size_label.pack(side=customtkinter.RIGHT)
     progressdetails_frame = customtkinter.CTkFrame(master=fdetails_frame,fg_color="transparent")
     progressdetails_frame.pack(anchor="w")
     progresslabel_1 = customtkinter.CTkLabel(master=progressdetails_frame,text="Progress:", font=("Bold",20))
     progresslabel_1.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global progress_label_text
     progress_label_text = customtkinter.CTkLabel(master=progressdetails_frame,text="",font=("Bold",18))
     progress_label_text.pack(side=customtkinter.RIGHT)
     constatus_frame = customtkinter.CTkFrame(master=app)
     constatus_frame.pack(fill="both")
     global constatus_label
     constatus_label = customtkinter.CTkLabel(master=constatus_frame,text="Waiting for hostname",font=("Arial",15),text_color="orange")
     constatus_label.pack( padx=10)
     closebutton_1 = customtkinter.CTkButton(master=app,text="Close", command=close_button_callback,fg_color="transparent")
     closebutton_1.pack(fill="x",side=customtkinter.BOTTOM)

def hostname_callback():
     global user_hostnameinput
     user_hostnameinput = hostname_entry.get()
     if user_hostnameinput == "":
          constatus_label.configure(text="Blank input",text_color="white")
     else:
          t1=connection()
          t1.start()
          global connect_again
          connect_again = 0

def upload_file():
     global send_button
     global connect_again
     if connect_again == 0:
          print("no second start")
          cleanup()
          global complete_label_stat
          global error1_label_stat
          global error2_label_stat
          complete_label_stat = False
          error1_label_stat = False
          error2_label_stat = False
     else:
          cleanup()
          t1=connection()
          t1.start()
     try:
          global file
          file = filedialog.askopenfilename(title="Select file")
          connect_again = 0
          if file:
               global sendbutton_checker
               global f_size
               f_size = os.path.getsize(file)
               print(f_size)
               chfsize_mb = int(f_size/1048576)
               fsize_mb = str(int(f_size/1048576))+"mb"
               filename_label = os.path.basename(file)
               file_label.configure(text=filename_label)
               if chfsize_mb <= 0:
                    size_label.configure(text=str(str(f_size)+"bytes"))
               else:
                    size_label.configure(text=str(fsize_mb))
               global send_button_stat
               send_button_stat = 1
               send_button = customtkinter.CTkButton(master=fdetails_frame, command=sendfile_stage,text="Send")
               send_button.pack(pady=10, padx=10)
               logger.info("File selected")
               if sendbutton_checker== True:
                    send_button.destroy()
               sendbutton_checker=True
     except Exception as e:
          print(e)
          logger.warning(e)
def sendfile_stage():
     print("send file stage")
     if con_status ==0:
          constatus_label.configure(text_color="#ff3333",text="Please enter hostname of receiver")
          hostbutton_1.configure(state="normal")
          hostname_entry.configure(state="normal")
          cleanup()
     else:
          SEPARATOR = "<SEPARATOR>"
          BUFFER_SIZE = 4096  # 4KB
          print("i am ready to send")
          filename = os.path.basename(file)
          filename_without_ext, file_extension = os.path.splitext(filename)
          full_filename = filename_without_ext+file_extension
          try:
               browse_button.configure(state="disabled")
               s.send(f"{full_filename}{SEPARATOR}{f_size}".encode())
               global progressbar_1
               progressbar_1 = customtkinter.CTkProgressBar(master=fdetails_frame)
               progressbar_1.pack(pady=10, padx=10,side=customtkinter.BOTTOM)
               bytes_sent = 0
               try:
                    send_button.destroy()
               except Exception as e:
                    print(e)
               with open(file, "rb") as f:
                    while True:
                         bytes_read = f.read(BUFFER_SIZE)
                         if not bytes_read:
                              break
                         s.sendall(bytes_read)
                         # Update the progress bar
                         bytes_sent += len(bytes_read)
                         alltrans_status = (bytes_sent / f_size) * 100
                         decimal = alltrans_status / 100
                         int_alltrans = int(alltrans_status)
                         slider_callback(decimal)
                         progress_label_text.configure(text=str(int_alltrans) +"%" +" of " + str(int(f_size/1048576))+"mb")
                         progress_label_text.update()
               global complete_label
               complete_label = customtkinter.CTkLabel(fdetails_frame, font=("System",20,"bold"), text_color="#00ff00",text="Transfer Completed",padx=20,pady=3)
               complete_label.pack()
               global complete_label_stat
               complete_label_stat = True
               browse_button.configure(state= "normal")
               filename = ""
               filename_without_ext, file_extension = "",""
               full_filename = ""
               s.close() 
               global connect_again
               connect_again = 1
               global sendbutton_checker
               sendbutton_checker = False
               logger.info("File transfer completed")
          except ConnectionResetError:
               logger.warning("Transfer failed: Receiver disconnected")
               global error1_label_stat
               error1_label_stat = True
               global error1_label
               error1_label = customtkinter.CTkLabel(fdetails_frame, font=("System",20,"bold"), text_color="#ff3333",text="Transfer Failed: Receiver disconnected",padx=20,pady=3)
               error1_label.pack()
               browse_button.configure(state="normal")
               sendbutton_checker=False
               s.close()
               t1=connection()
               t1.start()
          except Exception as e:
               print(e)
               logger.critical(e)
               global error2_label_stat
               error2_label_stat = True
               global error2_label
               error2_label = customtkinter.CTkLabel(fdetails_frame, font=("System",20,"bold"), text_color="#ff3333",text="An error occured. Try again",padx=20,pady=3)
               error2_label.pack()
               browse_button.configure(state="normal")
               sendbutton_checker=False
               s.close()
               t1=connection()
               t1.start()

def slider_callback(value):
    progressbar_1.set(value)
def cleanup():
     if complete_label_stat:
          global complete_label
          complete_label.destroy()
          progressbar_1.destroy()
     if error1_label_stat:
          global error1_label
          error1_label.destroy()
          progressbar_1.destroy()
     if error2_label_stat:
          global error2_label
          error2_label.destroy()
          progressbar_1.destroy()
def close_button_callback():
     os.execv(sys.executable, ['python'] + sys.argv)

def rf():
     pyferbutton_1.destroy()
     print("rf")
     closebutton_1 = customtkinter.CTkButton(master=app,text="Close", command=close_button_callback_rec,fg_color="transparent")
     closebutton_1.pack(fill="x",side=customtkinter.BOTTOM)
     userhostname = socket.gethostname()
     hostnameframe_1 = customtkinter.CTkFrame(master=mainframe_1,fg_color="transparent")
     hostnameframe_1.pack(side=customtkinter.TOP,pady=6,padx=6)
     youhostlabel = customtkinter.CTkLabel(master = hostnameframe_1,text="Your hostname: ")
     youhostlabel.pack(side=customtkinter.LEFT)
     gethostname_label = customtkinter.CTkLabel(master=hostnameframe_1,text=userhostname)
     gethostname_label.pack(side=customtkinter.RIGHT)
     rconstatus_frame = customtkinter.CTkFrame(master=app)
     rconstatus_frame.pack(fill="both")
     global rconstatus_label
     rconstatus_label = customtkinter.CTkLabel(master=rconstatus_frame,text="Waiting for hostname",font=("Arial",15),text_color="orange")
     rconstatus_label.pack( padx=10)
     global recfdetails_frame
     recfdetails_frame = customtkinter.CTkFrame(master=mainframe_1)
     recfdetails_frame.pack(pady=3, padx=10, fill="both", expand=True)
     recnamedetails_frame = customtkinter.CTkFrame(master=recfdetails_frame,fg_color="transparent")
     recnamedetails_frame.pack(anchor="w")
     recname_label = customtkinter.CTkLabel(master=recnamedetails_frame, text="Name:", font=("Arial",20, "bold"))
     recname_label.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global recfile_label
     recfile_label = customtkinter.CTkLabel(master=recnamedetails_frame,text="",font=("Bold",15))
     recfile_label.pack(side=customtkinter.RIGHT)
     recsizedetails_frame = customtkinter.CTkFrame(master=recfdetails_frame,fg_color="transparent")
     recsizedetails_frame.pack(anchor="w")
     recnamesizelabel_1 = customtkinter.CTkLabel(master=recsizedetails_frame,text="Size:", font=("Arial",20, "bold"))
     recnamesizelabel_1.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global recsize_label
     recsize_label = customtkinter.CTkLabel(master=recsizedetails_frame,text="",font=("Bold",18))
     recsize_label.pack(side=customtkinter.RIGHT)
     recprogressdetails_frame = customtkinter.CTkFrame(master=recfdetails_frame,fg_color="transparent")
     recprogressdetails_frame.pack(anchor="w")
     recprogresslabel_1 = customtkinter.CTkLabel(master=recprogressdetails_frame,text="Progress:", font=("Bold",20))
     recprogresslabel_1.pack(pady=6, padx=6,anchor="w",side=customtkinter.LEFT)
     global recprogress_label_text
     recprogress_label_text = customtkinter.CTkLabel(master=recprogressdetails_frame,text="",font=("Bold",18))
     recprogress_label_text.pack(side=customtkinter.RIGHT)
     t3=incoming()
     t3.start()
class incoming(Thread):
     def run(self):
          while True:
               try:
                    global s
                    s = socket.socket()
                    host="0.0.0.0"
                    port = 9999
                    s.bind((host, port))
                    s.listen(5)
                    print(f"[+] Listening as {host}:{port}")
                    rconstatus_label.configure(text="Waiting for sender to Connect",text_color="#ff3333")
                    global client_socket,address
                    client_socket, address = s.accept()
                    print(f"[+] {address} is connected.")
                    rconstatus_label.configure(text="Connected: Waiting for sender to send file",text_color="#00ff00")
                    SEPARATOR = "<SEPARATOR>"
                    BUFFER_SIZE = 4096  # 4KB
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    filename, filesize = received.split(SEPARATOR)
                    intfilesize = int(filesize)
                    filename = os.path.basename(filename)
                    fsize_mb = int(intfilesize/1048576)
                    if fsize_mb <= 0:
                         recsize_label.configure(text=str(filesize)+"bytes")
                         matchzero = True 
                    else:
                         recsize_label.configure(text=str(fsize_mb)+"mb")
                         matchzero = False
                    recfile_label.configure(text=filename)
                    rconstatus_label.configure(text="Connected: File transfer in progress",text_color="#ADD8E6")
                    current_dir = os.getcwd()
                    folder_name = "Shared files"
                    shared_folder_path = os.path.join(current_dir, folder_name)
                    file_path = os.path.join(shared_folder_path, filename)
                    if not os.path.exists(shared_folder_path):
                         os.makedirs(shared_folder_path)
                    file_path = os.path.join(shared_folder_path, filename)
                    bytes_received = 0
                    with open(file_path, "wb") as f:
                     while True:
                          bytes_read = client_socket.recv(BUFFER_SIZE)
                          if not bytes_read: 
                               break
                          f.write(bytes_read)
                          bytes_received += len(bytes_read)
                          alltrans_status = (bytes_received / intfilesize) * 100
                          int_alltrans = int(alltrans_status)
                          if matchzero:
                               recprogress_label_text.configure(text=str(int_alltrans) +"%" +" of " + str(filesize)+"bytes")
                               recprogress_label_text.update()
                          else:
                               recprogress_label_text.configure(text=str(int_alltrans) +"%" +" of " + str(fsize_mb)+"mb")
                               recprogress_label_text.update()
                     reccomplete_label = customtkinter.CTkLabel(master=recfdetails_frame, font=("System",20, "bold"), text_color="#00ff00",text="File saved in Shared files folder",padx=20,pady=3)
                     reccomplete_label.pack()
                     client_socket.close()
                     time.sleep(1)
                     reccomplete_label.destroy()
                     logger.info("Transfer completed")

               except Exception as e:
                    print(e)
                    logger.critical(e)
                    recfailed_label = customtkinter.CTkLabel(master=recfdetails_frame, font=("System", 10, "bold"), text_color="#ff3333",text="Transfer Failed",padx=30,pady=5)
                    recfailed_label.pack()
                    time.sleep(1)
                    recfailed_label.destroy()
def close_button_callback_rec():
     s.close()
     os.execv(sys.executable, ['python'] + sys.argv)

t2=interface()
t2.start()

app.mainloop()
