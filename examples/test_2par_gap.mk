all: target1 target2


target1: target3
	sleep 1

target2: 
	sleep 1

target3: 
	sleep 2
