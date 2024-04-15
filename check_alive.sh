#!/bin/sh


#	Output Both Normal output & Normal err
#	./check_alive.sh >> & check_alive.log	


CHECK(){
	local H=$1 ; shift
	local N=$1 ; shift
#	echo host = $H  N = $N
	for i in `seq 1 $N`
	do
#		ssh xfelopr@$H arv-tool-0.6 -a 192.168.$i.1
		ssh xfelopr@$H arv-tool-0.6 -a 192.168.$i.1 2>&1		# Normal err -> Normal output
	done
}




	while :
	do
		now_date=`date  +"%Y%m%d-%H%M"`	#"%Y%m%d-%H%M%S"`
		echo "date = 	[${now_date}]"

		ans0=`CHECK scimg-s-bc1-01 7`
		ans1=`CHECK scimg-s-cb2-1-01 7`
		ans2=`CHECK scimg-bl1-01 8`

#		echo "- - - ANS - - - - - - "
		echo $ans0
		echo $ans1
		echo $ans2

		sleep 600	#60	#sec
	done











