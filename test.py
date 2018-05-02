import sensor, time
from threading import Thread
from Queue import Queue, Empty

def update(q):
    s.auto()
    for x in range(0, 100):
        q.put(s.get_status())
        time.sleep(.1)

s = sensor.SensorInput()

q = Queue()

worker = Thread(target=update, args=(q,))
worker.setDaemon(True)
worker.start()

while worker.isAlive():
    try:
        print q.get_nowait()
    except Empty:
        x = 1

#s = sensor.SensorInput()
#s.auto()
#for x in range(0, 100):
#    print s.get_status()
#    if x == 30:
#        s.heat_on()
#    time.sleep(.1)
#s.stop()


