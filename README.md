# Installation instructions

## Preparations

Ensure your device has a vendor partition from Android 9 (newer versions will not work and Android 8 might work but any other older versions will not). If your device is A/B device (sargo and pro1 are A/B devices), it is necessary to have both slots on same Android version. So, if you upgraded Android to newer version than Android 9 (Pie), you have to downgrade Android first (flash Android 9 separately on both slots).

Download the rootfs for your architecture and your device's adaptation package from the releases of this repository. You can also download devtools for the same architecture if you wish so. Devtools may come handy if something goes wrong during installation. Also, it is recommended to ensure that you have the latest fastboot and adb versions. You will also need to have a recovery image (TWRP is recommended) for your phone.

After this, reboot your phone to fastboot (by pressing power and volume down buttons at the same time for a while) and connect the phone to your computer. Then, run following commands on your computer:

* `fastboot boot /path/to/recovery.img`

## Installation

From recovery open adb sideload mode (under advanced on TWRP) and run following commands on your computer replacing `ARCH_YYYYMMDD` with the version of Droidian and `vendor-device` with the vendor and device codenames:

* `adb sideload droidian-rootfs-api28gsi-ARCH_YYYYMMDD.zip`
* `adb sideload droidian-devtools-ARCH_YYYYMMDD.zip`
* `adb sideload droidian-adapatation-vendor-device-ARCH_YYYYMMDD.zip`

Note that you have to restart the sideload mode by tapping back and starting sideload again before every `adb sideload command`.

## Finalizing installation

Now, you have to reboot the device. It should boot to phosh (a graphical user interface used by Droidian) after rebooting once more automatically. When the device has booted, you can unlock the device with the default passcode `1234`.

## Troubleshooting

If the image does not boot and your userdata is not an ext4 partition, you might try formatting it. **Note that this is a destructive operation, you cannot recover files from userdata afterwards!**

* `fastboot format:ext4 userdata`
