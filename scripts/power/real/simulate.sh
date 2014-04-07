#!/bin/sh

for node in 08 09 10 12 15 16 17 18 19 23 24 25 26 27 28 29 30 31 32 33
do
    case "$node" in
	08) num=1
	    ;;
	09) num=2
	    ;;
	10) num=3
	    ;;
	12) num=4
	    ;;
	15) num=5
	    ;;
	16) num=6
	    ;;
	17) num=7
	    ;;
	18) num=8
	    ;;
	19) num=9
	    ;;
	23) num=10
	    ;;
	24) num=11
	    ;;
	25) num=12
	    ;;
	26) num=13
	    ;;
	27) num=14
	    ;;
	28) num=15
	    ;;
	29) num=16
	    ;;
	30) num=17
	    ;;
	31) num=18
	    ;;
	32) num=19
	    ;;
	33) num=20
	    ;;
    esac
    args=''
    ssh tarekc$node.cs.uiuc.edu "python26 ~/bjorn/simulation/powerReal.py ${num}"
done