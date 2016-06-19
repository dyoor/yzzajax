#!/bin/bash
p1=`ps -ef | grep yzz_ajax | grep py | awk '{print $2}'`
kill $p1
python yzz_ajax_p8899.py &
ps -ef | grep yzz_ajax | grep py
