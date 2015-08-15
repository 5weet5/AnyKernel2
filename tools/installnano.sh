#!/sbin/sh

# Mount system
/tmp/busybox mount /system

NANODIR=/system/etc/nano
NANOBIN=/system/xbin/nano

# Check for previous installation of nano
if [ ! -d "$NANODIR" ] || [ ! -f "$NANOBIN"] ; then
	cp -rf system/etc/nano /system/etc/nano
	cp -rf system/etc/terminfo /system/etc/terminfo
	cp -f system/etc/xbin/nano /system/xbin/nano
	cp -rf system/lib /system/lib
else
	echo "Previous version of nano detected. Skipping install"
fi