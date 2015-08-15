#!/sbin/sh

# Mount /system
/tmp/busybox mount /system

# If busybox not in /system/xbin/busybox then install
if [ ! -f /system/xbin/busybox ]; then
	echo "@Busybox not found. Installing..."
	cp /tmp/busybox /system/xbin/busybox
	chmod 755 /system/xbin/busybox
	/system/xbin/busybox --install /system/xbin
else
	echo '@Found previous busybox install--skipping'
fi