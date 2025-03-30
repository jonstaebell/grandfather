import os, socket, sys, pathlib
def get_filename():
    return "15"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
print (os.getcwd())
print ('http://' + s.getsockname()[0] + ':8000' + os.getcwd() + "/bong" + "15"  + ".wav")
print (os.path.dirname(__file__)) # TODO replace os.getcwd()
#location = 'http://' + s.getsockname()[0] + ':8000' + pathlib.Path( os.path.abspath(__file__)).parent + "/bong" + "15"  + ".wav"
#file = "/bong" + "15"  + ".wav"
#print (location)
parentdir = str(pathlib.Path( os.path.abspath(__file__)).parent)
media = 'http://' + s.getsockname()[0] + ':8000' + parentdir + "/bong" + get_filename()  + ".wav"
print (media)

