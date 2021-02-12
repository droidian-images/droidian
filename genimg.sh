#!/bin/bash
ROOTFS_PATH=$(find . -maxdepth 1 -mindepth 1 -type d -name .debos-*)/root
ROOTFS_SIZE=$(du -sm $ROOTFS_PATH | awk '{ print $1 }')

IMG_NAME=$1
IMG_SIZE=$(( ${ROOTFS_SIZE} + 250 )) # FIXME 250MB contingency
IMG_MOUNTPOINT=".image"

# create root img
echo "Creating an empty root image"
dd if=/dev/zero of=$IMG_NAME bs=1M count=${IMG_SIZE}
mkfs.ext4 -O ^metadata_csum -O ^64bit -F $IMG_NAME

# mount the image
echo "Mounting root image"
mkdir -p $IMG_MOUNTPOINT
mount -o loop $IMG_NAME ${IMG_MOUNTPOINT}

# copy rootfs content
echo "Syncing rootfs content"
rsync --archive -H -A -X $ROOTFS_PATH/* ${IMG_MOUNTPOINT}
rsync --archive -H -A -X $ROOTFS_PATH/.[^.]* ${IMG_MOUNTPOINT}
sync
echo "done."

# umount the image
echo "umount root image"
umount $IMG_MOUNTPOINT
