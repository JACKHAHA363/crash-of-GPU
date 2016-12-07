import smtplib
import subprocess 
from subprocess import Popen
import time

free_threshold = 200
sending_flag = [True]*8

def check_usage():
    available = []
    for gpu_index in range(8):
        p1 = Popen(["nvidia-smi", "-i",str(gpu_index)], stdout=subprocess.PIPE)
        p2 = Popen(["grep", "Default"], stdout=subprocess.PIPE, stdin=p1.stdout)  
        info = p2.stdout.readlines()[0].split()
        used_memory = info[8][0:-3]
        if int(used_memory) < free_threshold:
            available.append(gpu_index)
        else:
            sending_flag[gpu_index] = True
    return available

def send_msg(email, msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("jackhaha363@gmail.com", "a62863062")
    server.sendmail("jackhaha363@gmail.com", email, msg)
    server.quit()

# check GPU status every 300 second
while True:
    time.sleep(300)
    gpu_status = check_usage()
    for gpu_idx in gpu_status:
        if sending_flag[gpu_idx] == True:
            msg = "GPU {} is available now!!!!".format(gpu_idx)
            print(msg)
            send_msg("luyuchen.paul@gmail.com", msg)
            sending_flag[gpu_idx] = False
