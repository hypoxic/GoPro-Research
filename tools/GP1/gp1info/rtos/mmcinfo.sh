mmcinfo()
{
  if [ "`find /sys/  |grep mmc`" == "" ]; then
    echo "No MMC device is found"
    return
  fi
option=$1

case ${option} in 
    misc)
echo "--------- misc  debug information ---------------------------"
preferred_erase_size_STRING=`find /sys/devices -name 'preferred_erase_size'| grep mmc| xargs cat`
echo "preferred_erase_size_STRING: $preferred_erase_size_STRING"
printf "preferred_erase_size_STRING: %d (=0x%x =%dM) bytes\n" \
  $preferred_erase_size_STRING $preferred_erase_size_STRING $(($preferred_erase_size_STRING/((1024*1024))))
erase_size_STRING=`find /sys/devices -name 'erase_size'| grep mmc| xargs cat`
echo "erase_size_STRING:              $erase_size_STRING"
enhanced_area_size_STRING=`find /sys/devices -name 'enhanced_area_size'| grep mmc| xargs cat`
echo "enhanced_area_size_STRING:      $enhanced_area_size_STRING"
type_STRING=`find /sys/devices -name 'type'| grep mmc| xargs cat`
echo "type_STRING:                    $type_STRING"

# debug section
status_STRING=`find /sys/kernel/debug/mmc* -name 'status'| grep mmc| xargs cat`
echo "status_STRING (JEDEC card status): 0x$status_STRING"
state_STRING=`find /sys/kernel/debug/mmc* -name 'state'| grep mmc| xargs cat`
echo "state_STRING (JEDEC card state): $state_STRING"
clock_STRING=`find /sys/kernel/debug/mmc* -name 'clock'| grep mmc| xargs cat`
echo "clock_STRING: $clock_STRING"


;;
cid)
echo "--------- CID ---------------------------"
CID_STRING=`find /sys/devices -name 'cid'| grep mmc| xargs cat| sed 's/.\{2\}/& /g'`
CID_ARRAY=($CID_STRING)
echo "CID Binary:  $CID_STRING"
CID_NAME=`find /sys/devices -name 'name'| grep mmc| xargs cat`
echo "CID_MID:   0x${CID_ARRAY[0]}"
echo "CID_NAME:  $CID_NAME"
CID_DATE=`find /sys/devices -name 'date'| grep mmc| xargs cat`
echo "CID_DATE:  $CID_DATE"
;;

csd)
echo "--------- CSD ---------------------------"
CSD_STRING=`find /sys/devices -name 'csd'| grep mmc| xargs cat| sed 's/.\{2\}/& /g'`
echo "CSD Binary:  $CSD_STRING"

;;

ecsd| ext_csd) # ext_csd
echo "--------- find /sys/kernel/debug/mmc* -name 'ext_csd' and decode: -------- "
# cat '/sys/kernel/debug/mmc0/mmc0:0001/ext_csd' | sed 's/.\{2\}/& /g' | fold -w48
# cat '/sys/kernel/debug/mmc0/mmc0:0001/ext_csd' | sed 's/.\{2\}/& /g' | fold -w24
EXT_CSD_STRING=`cat '/sys/kernel/debug/mmc0/mmc0:0001/ext_csd' | sed 's/.\{2\}/& /g'`
EXT_CSD_ARRAY=($EXT_CSD_STRING)
 # echo ${EXT_CSD_ARRAY[@]}
 let MAX_NUM=511
 let COUNTER=MAX_NUM
 while [  $COUNTER -gt -1 ]; do  # -gt  larger than
    printf "[%03d]=0x%s "  ${COUNTER}  ${EXT_CSD_ARRAY[$((MAX_NUM-COUNTER))]}
    if [ $((COUNTER%8)) -eq 0 ]; then
      printf "\n"
    fi
    let COUNTER=COUNTER-1
 done
printf "EXT_CSD_REV[192]=%d\n" ${EXT_CSD_ARRAY[$((MAX_NUM-192))]}
printf "EXT_CSD_SEC_COUNT[215-212]=0x%x%x%x%x\n" ${EXT_CSD_ARRAY[$((MAX_NUM-215))]} ${EXT_CSD_ARRAY[$((MAX_NUM-214))]} \
    ${EXT_CSD_ARRAY[$((MAX_NUM-213))]} ${EXT_CSD_ARRAY[$((MAX_NUM-212))]}
;;
*)
mmcinfo ext_csd
mmcinfo cid
mmcinfo csd
mmcinfo misc
;;
esac


}