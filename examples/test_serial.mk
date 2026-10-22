all: target1


target1: target2
	sleep 1

target2: target3
	sleep 1

target3: target4
	sleep 1

target4: 
	sleep 1
