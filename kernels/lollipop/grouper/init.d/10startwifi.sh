#!/system/bin/sh
# Start Wifi at boot
insmod /system/lib/modules/bcmdhd.ko firmware_path=/system/vendor/firmware/fw_bcmdhd.bin nvram_path=/system/etc/nvram.txt
