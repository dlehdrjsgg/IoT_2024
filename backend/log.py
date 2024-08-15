import time

def Errorlog(message):
    with open('var/error.log', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + message + '\n')
        
def Debuglog(message):
    with open('var/debug.log', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + message + '\n')

def Infolog(message):
    with open('var/info.log', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + message + '\n')