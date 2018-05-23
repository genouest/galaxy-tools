#!/bin/bash
## ATTENTION Ce script a ete repris de celui émis par Olivier Filangi pour faire tourner qtlmap sous galaxy sur la plateforme QGP.
# 
# 
# 
# 
# - Recensement de toute les applications genetiques
# - Initilisation des variables lie Ã  openmp
# - Initialisation d'un indice de carte GPU pour attribuer un ID unique Ã  chaque application
#     ID_QGP_GPU. 
#   Si une appli utilise plus de 1 GPU, cet idientifiant est l'ID de la premiere carte
#   ID_QGP_GPU.+1 => 2 eme carte,etc...
# - Definition de functions pour avoir des statistiques de base sur l'execution des applis QGP
#   Cette fonction doit etre appele en fin de script du programme 
#   - stats_qgp_start <NOM_PROGAMME>
#   - stats_qgp_end <CODE_RETOUR>
#
#
# auteur : olivier.filangi@rennes.inra.fr
#
#
#
# Les scripts doivent charger l'environnement par > source genocluster-env.sh 
# root des logiciels
LOGFILE=$GALAXY_HOME/database/log/log-qtlmap

#Pour plus de genericite (ajout de nouvelle carte ou nombre de carte differente selon la machine cible)
#l'appel est long du au chargement du module nvidia
#ngpu=`nvidia-smi -L | wc -l`
#pour l instant on ecrit en dur le nbre de gpu sur une machine
ngpu=2

PEDIGDIR=$SOFT_GENETIQUE/pedig/bin/
GS3=/softs/local/galaxy/GS3/GS3/gs3
GABAYES=/softs/local/galaxy/GABayes/build/gabayes

# add some variables for GenOuest execution
TMPDIR=$GALAXY_HOME/database/tmp/
QTLMAP_CPU='qtlmap'


DATABASE_GALAXY=/work/preprod/database
export LD_LIBRARY_PATH=/local/GCC/lib64/:$LD_LIBRARY_PATH


#initialisation openmp si besoin
if [ -z $NSLOTS ];then
 export OMP_NUM_THREADS=1
else
 export OMP_NUM_THREADS=$NSLOTS
fi

# Rend un ID pour l'utilisation d'un carte GPU
# -1 si aucune carte trouvÃ©
# 0 - (n-1) 
# condition : Les JOB_ID sont ordonnees ( 2 jobs (69 et 70) qui sont "r" => le JOB_ID=69 a ete lance avant le  JOB_ID=70 => id_gpu 0 pour 69 et id_gpu=1 pour 70) 
#
#if [ -z $HOSTNAME ];then
#ID_QGP_GPU=-1
#else

#if [ -z $SGE_BINARY_PATH ];then
#SGE_BINARY_PATH=/gridware/sge/bin/lx24-amd64/qstat
#fi

#ID_QGP_GPU=`$SGE_BINARY_PATH/qstat -r | awk 'BEGIN {id_gpu=-1;gpu_request=0} $8 ~ /'$HOSTNAME'/ {tocheck=0;if ( $5 == "r" && $1 <= '$JOB_ID') { tocheck=1};jobid=$1} $3 ~/gpu=/ && tocheck == 1 { if ('$JOB_ID' == jobid ) {gpu_request=1}; split($3,a,"=");id_gpu=id_gpu+a[2];tocheck=0 }  END { if ( gpu_request == 1 ) {print id_gpu} else {print -1}}'`
#fi

# set the environment variable with a free
function set_id_gpu {
TMPF=/tmp/id_gpu.$$
{
flock -n 300

if [ -s ${FILEREC_GPU} ];then
ID_QGP_GPU=`cat ${FILEREC_GPU} | awk 'BEGIN {FS="="} $2 == 0 {print $1;exit}'`
if [ -z ${ID_QGP_GPU} ];then
 echo "** None GPU resources availables. **"1>&2
 echo "** GPU Ressources availables ** "
 cat ${FILEREC_GPU} 1>&2
 ID_QGP_GPU=-1
 exit -1
fi
cat ${FILEREC_GPU} | awk 'BEGIN {FS="="} $1 != '${ID_QGP_GPU}' {print $0}'>${TMPF}
cat ${TMPF} > ${FILEREC_GPU}
echo "${ID_QGP_GPU}=1" >> ${FILEREC_GPU}
rm -rf ${TMPF}
else
#le fichier nexiste pas,on attribut le premier ID
ID_QGP_GPU=0
echo "${ID_QGP_GPU}=1" > ${FILEREC_GPU}
for ((igpu=1;igpu<$ngpu;igpu++))
do
echo "$igpu=0" >> ${FILEREC_GPU}
done
fi

#number of GPUs in the host
} 300> ${FILELOCK_GPU}
}


function release_id_gpu {
ID_QGP_GPU=$1
TMPF=/tmp/id_gpu.$$
{
flock -n 300
if [ -s ${FILEREC_GPU} ];then
cat ${FILEREC_GPU} | awk 'BEGIN {FS="="} $1 != '${ID_QGP_GPU}' {print $0}'>${TMPF}
cat ${TMPF} > ${FILEREC_GPU}
echo "${ID_QGP_GPU}=0" >> ${FILEREC_GPU}
rm -rf ${TMPF}
else
for ((igpu=0;igpu<$ngpu;igpu++))
do
echo "$igpu=0" >> ${FILEREC_GPU}
done
fi
} 300> ${FILELOCK_GPU}
}

# Tous les applications QGP doivent appeler cette fonction pour avoir des stats de bases
#
# ENTETE DU LOG
#
# JOB_ID_SGE, PID, NOM_PROGRAMME, DATE_DE_DEBUT DATE_DE_FIN DIFF_TEMPS NB_SLOTS IDGPU CODE_RETOUR
#
# date +%s => timestamp
# date -d @xxxxxxxxx => affichage de la date du timestamp xxxxxxxx


# ARG1 => Nom du programme
function stats_qgp_start {
__QGP_PROG=$1
__START_DATESTAMP=`date +%s`
}

#ARG1 => CODE RETOUR FONCTION
function stats_qgp_end {
__CODERET=$1
__END_DATESTAMP=`date +%s`
__ELAPSED_TIME=$(( ${__END_DATESTAMP} - ${__START_DATESTAMP} ))
{
flock -n 200
echo "$JOB_ID $PID ${REQNAME} ${__QGP_PROG} ${__START_DATESTAMP} ${__END_DATESTAMP} ${__ELAPSED_TIME} $NSLOTS ${ID_QGP_GPU} ${__CODERET}">>$LOGFILE
} 200>lockfile
}
#Gestion des sorties html

#donner en entree 1) le fichier ou ecrire l entete, 2) l application
qgp_header_html() {
  out=$1  
  nameapp=$2

  echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">">>$out
  echo "<HTML>">>$out
  echo "<HEAD>">>$out
  echo "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html;charset=iso-8859-1\">">>$out
 # echo "<TITLE>QGP - $nameapp </TITLE>">>$out
  echo "</HEAD>">>$out
  echo "<BODY>">>$out
}

qgp_end_html() {
  out=$1

  echo "</BODY>">>$out
  echo "</HTML>">>$out

}

############################################################
# encode the file to set a href tag
#encode_file_url() {
# file=`basename $1`
# number_file=`echo $file | awk 'BEGIN {FS="_"} {print $2}' | awk 'BEGIN {FS="."} {print $1}'`
# id=`python /work/preprod/galaxy-dist/scripts/helper.py -e $number_file | awk 'BEGIN {FS=":"}{sub(" ","",$2);print $2}'`
# echo "datasets/$id/display/?preview=True"
#}

output_html_qtlmap() {
PANALYSE=$1
html=$2
work_path="test"

echo "<h1>QTLMap</h1>" >> $html
#########################################################SUMARY
echo "<h2>Summary</h2>" >> $html
echo "<pre>" >> $html
current_file=`grep out_summary $PANALYSE | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`
cat  ${current_file} | grep -v $DATABASE_GALAXY >> $html
echo "</pre>" >> $html
#########################################################
#echo "<h2>Downloaded Files</h2>" >> $html
#current_file=`grep out_lrtsires $PANALYSE | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`
#echo "<p>">> $html
#echo $current_file >> $html
#echo `encode_file_url $current_file` >> $html
#echo "TEST:<a href=\"`encode_file_url $current_file`\">LRT Sires</a>">> $html
#echo "TEST:<a href=\"`basename $current_file`\">LRT Sires</a>">> $html
#echo "</p>">> $html
#########################################################PHASES
echo "<h2>Markers</h2>" >> $html
echo "<pre>" >> $html
current_file=`grep out_output $PANALYSE | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`
cat  ${current_file}_freqall | grep -v $DATABASE_GALAXY >> $html
echo "</pre>" >> $html
rm -rf ${current_file}_freqall #on l efface car il n est pas gerer par galaxy
#########################################################PHASES
echo "<h2>Phases</h2>" >> $html
echo "<pre>" >> $html
current_file=`grep out_phases $PANALYSE | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`
cat  ${current_file} | grep -v $DATABASE_GALAXY >> $html
echo "</pre>" >> $html

#########################################################RESULT
echo "<h2>Result File</h2>" >> $html
echo "<pre>" >> $html
current_file=`grep out_output $PANALYSE | tail -n1 | awk 'BEGIN {FS="="}{print $2}'`
cat  ${current_file} | grep -v $DATABASE_GALAXY >> $html
echo "</pre>" >> $html
}

#Ajouts janvier 2014

# ARG1 => Nom du programme
function stats_qgp_start {
__QGP_PROG=$1
__START_DATESTAMP=`date +%s`
}

#ARG1 => CODE RETOUR FONCTION
function stats_qgp_end {
__CODERET=$1
__END_DATESTAMP=`date +%s`
__ELAPSED_TIME=$(( ${__END_DATESTAMP} - ${__START_DATESTAMP} ))
{
flock -n 200
echo "$JOB_ID $PID ${REQNAME} ${__QGP_PROG} ${__START_DATESTAMP} ${__END_DATESTAMP} ${__ELAPSED_TIME} $NSLOTS ${ID_QGSP_GPU} ${__CODERET}">>$LOGFILE
} 200>lockfile
}
#Gestion des sorties html

#donner en entree 1) le fichier ou ecrire l entete, 2) l application
qgp_header_html() {
  out=$1  
  nameapp=$2

  echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">">>$out
  echo "<HTML>">>$out
  echo "<HEAD>">>$out
  echo "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html;charset=iso-8859-1\">">>$out
 # echo "<TITLE>QGP - $nameapp </TITLE>">>$out
  echo "</HEAD>">>$out
  echo "<BODY>">>$out
}

qgp_end_html() {
  out=$1

  echo "</BODY>">>$out
  echo "</HTML>">>$out

}


#add a tag with a href embeded_a file gzipped
add_tags_href_with_downloaded_file() {

current_file=$1
comments_to_down=$2
html__=$3

if [ -s "$current_file" ];then
 #encodage base64 pour embarqué le fichier à telecharge dans la page HTML
 newfile="./"`echo $comments_to_down"_"$JOB_ID".txt" | awk '{gsub("[ \t]","_",$0);print $0}'`
 ln -s $current_file $newfile
 #download="'`echo $comments_to_down |  sed -e 's/[ \t]/_/'`'"
 echo '<a href="data:application/x-gzip;base64,'`gzip --stdout $newfile | base64 -w 0`'">'>> $html__
 #echo '<a href="data:application/zip;base64,'`zip --stdout $current_file".txt" | base64 -w 0`'">'>> $html__
 #echo '<a href="data:text/plain;base64,'`base64 -w 0 $current_file".txt"`'">'>> $html__
 rm $newfile
 echo $comments_to_down >>$html__
 echo '</a>' >> $html__
fi

}

#add a tag with a href embeded_a file gzipped
add_tags_href_with_view_file() {

current_file=$1
comments_to_down=$2
html__=$3

if [ -s "$current_file" ];then
 #encodage base64 pour embarqué le fichier à telecharge dans la page HTML
 echo '<a href="data:text/plain;base64,'`base64 -w 0 $current_file".txt"`'">'>> $html__
 echo $comments_to_down >>$html__
 echo '</a>' >> $html__
fi

}

