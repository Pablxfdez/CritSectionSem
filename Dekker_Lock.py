from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Lock
import time
import random
N = 8
def is_anybody_inside(critical, tid):
	found = False
	i = 0
	while i<len(critical) and not found:
		found = tid!=i and critical[i]==1
		i += 1
	return found
def task(common, tid, mutex):
	for i in range(80):
		print(f'{tid}−{i}: Non−critical Section', flush = True )
		time.sleep(random.random())
		print(f'{tid}−{i}: End of non−critical Section', flush = True)
		mutex.acquire()
		print(f'{tid}−{i}: Critical section')
		v = common.value + 1
		print(f'{tid}−{i}: Inside critical section', flush = True)
		time.sleep(random.random())
		common.value = v
		print(f'{tid}−{i}: End of critical section', flush = True)
		mutex.release()

def main():
	lp = []
	mutex = Lock()
	common = Value('i', 0)
	for tid in range(N):
		lp.append(Process(target=task, args=(common, tid, mutex)))
	print (f"Valor inicial del contador {common.value}")
	for p in lp:
		p.start()
	for p in lp:
		p.join()
	print (f"Valor final del contador {common.value}")
	print ("fin")
if __name__ == "__main__":
	main()