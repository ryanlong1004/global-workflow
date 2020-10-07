#!/bin/sh
set -u
#------------------------------------
# USER DEFINED STUFF:
#
# USE_PREINST_LIBS: set to "true" to use preinstalled libraries.
#                   Anything other than "true"  will use libraries locally.
#------------------------------------

#------------------------------------
# END USER DEFINED STUFF
#------------------------------------

build_dir=`pwd`
logs_dir=$build_dir/logs
if [ ! -d $logs_dir  ]; then
  echo "Creating logs folder"
  mkdir $logs_dir
fi

# Check final exec folder exists
if [ ! -d "../exec" ]; then
  echo "Creating ../exec folder"
  mkdir ../exec
fi

#------------------------------------
# GET MACHINE
#------------------------------------
target=""
source ./machine-setup.sh > /dev/null 2>&1

#------------------------------------
# INCLUDE PARTIAL BUILD 
#------------------------------------

. ./partial_build.sh

#------------------------------------
# Exception Handling Init
#------------------------------------
ERRSCRIPT=${ERRSCRIPT:-'eval [[ $err = 0 ]]'}
err=0

#------------------------------------
# build libraries first
#------------------------------------
$Build_libs && {
	echo " .... Library build not currently supported .... "
	#echo " .... Building libraries .... "
	#./build_libs.sh > $logs_dir/build_libs.log 2>&1
}

#------------------------------------
# build fv3
#------------------------------------
$Build_fv3gfs && {
	echo " .... Building fv3 .... "
	./build_fv3.sh > $logs_dir/build_fv3.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building fv3."
		echo "The log file is in $logs_dir/build_fv3.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gsi
#------------------------------------
$Build_gsi && {
	echo " .... Building gsi .... "
	./build_gsi.sh > $logs_dir/build_gsi.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gsi."
		echo "The log file is in $logs_dir/build_gsi.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build ncep_post
#------------------------------------
$Build_ncep_post && {
	echo " .... Building ncep_post .... "
	./build_ncep_post.sh > $logs_dir/build_ncep_post.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building ncep_post."
		echo "The log file is in $logs_dir/build_ncep_post.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build ufs_utils
#------------------------------------
$Build_ufs_utils && {
	echo " .... Building ufs_utils .... "
	./build_ufs_utils.sh > $logs_dir/build_ufs_utils.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building ufs_utils."
		echo "The log file is in $logs_dir/build_ufs_utils.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_wafs - optional checkout 
#------------------------------------
if [ -d gfs_wafs.fd ]; then
	$Build_gfs_wafs  && {
		echo " .... Building gfs_wafs  .... "
		./build_gfs_wafs.sh > $logs_dir/build_gfs_wafs.log 2>&1
		rc=$?
		if [[ $rc -ne 0 ]] ; then
			echo "Fatal error in building gfs_wafs."
			echo "The log file is in $logs_dir/build_gfs_wafs.log"
		fi
		((err+=$rc))
	}
fi

#------------------------------------
# build sfcanl_nsttfchg 
#------------------------------------
$Build_sfcanl_nsttfchg && {
	echo " .... Building gaussian_sfcanl and nst_tf_chg .... "
	./build_sfcanl_nsttfchg.sh > $logs_dir/build_sfcanl_nsttfchg.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building Build_sfcanl_nsttfchg."
		echo "The log file is in $logs_dir/Build_sfcanl_nsttfchg.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build enkf_chgres_recenter
#------------------------------------
$Build_enkf_chgres_recenter && {
	echo " .... Building enkf_chgres_recenter .... "
	./build_enkf_chgres_recenter.sh > $logs_dir/build_enkf_chgres_recenter.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building enkf_chgres_recenter."
		echo "The log file is in $logs_dir/build_enkf_chgres_recenter.log"
	fi
	((err+=$rc))
}


#------------------------------------
# build enkf_chgres_recenter_nc
#------------------------------------
$Build_enkf_chgres_recenter_nc && {
	echo " .... Building enkf_chgres_recenter_nc .... "
	./build_enkf_chgres_recenter_nc.sh > $logs_dir/build_enkf_chgres_recenter_nc.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building enkf_chgres_recenter_nc."
		echo "The log file is in $logs_dir/build_enkf_chgres_recenter_nc.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build tropcy_NEMS
#------------------------------------
$Build_tropcy && {
	echo " .... Building tropcy_NEMS .... "
	./build_tropcy_NEMS.sh > $logs_dir/build_tropcy_NEMS.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building tropcy_NEMS."
		echo "The log file is in $logs_dir/build_tropcy_NEMS.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gdas
#------------------------------------
$Build_gdas && {
	echo " .... Building gdas .... "
	./build_gdas.sh > $logs_dir/build_gdas.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gdas."
		echo "The log file is in $logs_dir/build_gdas.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_fbwndgfs
#------------------------------------
$Build_gfs_fbwndgfs && {
	echo " .... Building gfs_fbwndgfs .... "
	./build_gfs_fbwndgfs.sh > $logs_dir/build_gfs_fbwndgfs.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gfs_fbwndgfs."
		echo "The log file is in $logs_dir/build_gfs_fbwndgfs.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_overpdtg2
#------------------------------------
$Build_gfs_overpdtg2 && {
	echo " .... Building gfs_overpdtg2 .... "
	./build_gfs_overpdtg2.sh > $logs_dir/build_gfs_overpdtg2.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gfs_overpdtg2."
		echo "The log file is in $logs_dir/build_gfs_overpdtg2.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_wintemv
#------------------------------------
$Build_gfs_wintemv && {
	echo " .... Building gfs_wintemv .... "
	./build_gfs_wintemv.sh > $logs_dir/build_gfs_wintemv.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gfs_wintemv."
		echo "The log file is in $logs_dir/build_gfs_wintemv.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_bufrsnd
#------------------------------------
$Build_gfs_bufrsnd && {
	echo " .... Building gfs_bufrsnd .... "
	./build_gfs_bufrsnd.sh > $logs_dir/build_gfs_bufrsnd.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gfs_bufrsnd."
		echo "The log file is in $logs_dir/build_gfs_bufrsnd.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build fv3nc2nemsio
#------------------------------------
$Build_fv3nc2nemsio && {
	echo " .... Building fv3nc2nemsio .... "
	./build_fv3nc2nemsio.sh > $logs_dir/build_fv3nc2nemsio.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building fv3nc2nemsio."
		echo "The log file is in $logs_dir/build_fv3nc2nemsio.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build regrid_nemsio
#------------------------------------
$Build_regrid_nemsio && {
	echo " .... Building regrid_nemsio .... "
	./build_regrid_nemsio.sh > $logs_dir/build_regrid_nemsio.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building regrid_nemsio."
		echo "The log file is in $logs_dir/build_regrid_nemsio.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build gfs_util       
#------------------------------------
# Only build on WCOSS
if [ $target = wcoss -o $target = wcoss_cray -o $target = wcoss_dell_p3 ]; then
	$Build_gfs_util && {
		echo " .... Building gfs_util .... "
		./build_gfs_util.sh > $logs_dir/build_gfs_util.log 2>&1
		rc=$?
		if [[ $rc -ne 0 ]] ; then
			echo "Fatal error in building gfs_util."
			echo "The log file is in $logs_dir/build_gfs_util.log"
		fi
		((err+=$rc))
	}
fi

#------------------------------------
# build gsd_prep_chem
#------------------------------------
$Build_gsd_prep_chem && {
	echo " .... Building gsd_prep_chem .... "
	./build_gsd_prep_chem.sh > $logs_dir/build_gsd_prep_chem.log 2>&1
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		echo "Fatal error in building gsd_prep_chem."
		echo "The log file is in $logs_dir/build_gsd_prep_chem.log"
	fi
	((err+=$rc))
}

#------------------------------------
# build prod_util
#------------------------------------
$Build_prod_util && {
	echo " .... prod_util build not currently supported .... "
	#echo " .... Building prod_util .... "
	#./build_prod_util.sh > $logs_dir/build_prod_util.log 2>&1
}

#------------------------------------
# build grib_util
#------------------------------------
$Build_grib_util && {
	echo " .... grib_util build not currently supported .... "
	#echo " .... Building grib_util .... "
	#./build_grib_util.sh > $logs_dir/build_grib_util.log 2>&1
}

echo;echo " .... Build system finished .... "

exit 0
