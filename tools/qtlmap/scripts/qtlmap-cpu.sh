#!/bin/bash
source `dirname $0`/genocluster-env.sh
stats_qgp_start "QTLMap-CPU"

html=$1
shift
nsim=$1
shift

current_file=`grep paramsimul $1 | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`

echo "############################################################"
cat $current_file

#decalage des arguments pour obtenir seulement les arguments de qtlmap
# Premiere execution pour obtenir les seuils de l'analyse
echo "I) Simulation"
echo

PANALYSE_SIM=/tmp/p_analyse_$$
FILE_SIM=/tmp/res_$$
cp $1 ${PANALYSE_SIM}
echo "">>${PANALYSE_SIM}
echo "out_output=${FILE_SIM}" >> ${PANALYSE_SIM}

ARGS_ANALYSE="$*" 
PANALYSE=$1
shift
#simulation
qtlmap ${PANALYSE_SIM} $* --nsim=$nsim | grep -v $DATABASE_GALAXY

# Deuxieme execution pour obtenir l'analyse

echo "II) Analysis"
echo
echo "out_output=${FILE_ANALYSE}" >> $1
#analyse
qtlmap $ARGS_ANALYSE | grep -v $DATABASE_GALAXY

FILE_ANALYSE=`grep out_output $PANALYSE | head -n1 | awk 'BEGIN {FS="="}{print $2}'`
#on concatene l'information des seuils à l analyse
cat ${FILE_SIM} >> ${FILE_ANALYSE}

rm -rf ${FILE_SIM}
rm -rf ${PANALYSE_SIM}

#
#
# Affichage dans un fichier Resultats HTML
#
qgp_header_html $html "* QTLMap - CPU *"

output_html_qtlmap $PANALYSE $html 
#$html_path

qgp_end_html $html
echo $11
stats_qgp_end $?



