source /local/env/envpython-2.7.sh
source /local/env/envR-3.0.1.sh
export PYTHONPATH=~flegeai/local/CPAT/local/python/2.7/lib/python2.7/site-packages/:$PYTHONPATH
export PATH=~flegeai/local/CPAT/local/bin:$PATH
~flegeai/local/CPAT/local/python/2.7/bin/cpat.py -g $1 -x $2 -d $3 -o $4
