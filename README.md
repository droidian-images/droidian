# DLS OS

**DLS OS** is a GNU/Linux distribution based on Debian, oriented towards **penetration testing** and cybersecurity research. It is designed to bring the power of a full Linux pentesting environment to mobile devices, taking inspiration from Droidian(**Mobian**) and adapted to run on Android-based phones.

This repository is the canonical place to get DLS OS images.

# Which image to get?

There are two different types of images:

* Fastboot-flashable image  
* Recovery-flashable zipfile

Fastboot-flashable images are the recommended way to install DLS OS. These images are device-specific, so if you want one for your device, you might need to create it yourself.  
Fastboot-flashable images support **Full Disk Encryption** and utilize the entire userdata partition.

The recovery-flashable zipfile needs to be flashed via a suitable Android recovery (such as TWRP). Recovery flashable zipfiles are **generic**, and are useful to test drive DLS OS or in early stages of device porting.

You should choose the correct zipfile for your specific device:

* Device with an Android 9 vendor: api28  
* Device with an Android 10 vendor: api29  
* Device with an Android 11 vendor: api30  
* Device with an Android 12/12.1 vendor: api32  
* Device with an Android 13 vendor: api33

If you're unsure, and a fastboot-flashable image is available for your device, it's recommended to use that.

## Recovery-flashable zipfile: bundles

Recovery flashable zipfiles support the addition of **bundles**, which allow you to add extra functionality directly during the flashing process.

Currently available bundles:

* **Devtools**: Useful development tools for porters (not available in nightlies as they are embedded in the rootfs)  
* **Adaptation bundle**: Device-specific bundle (kernel, settings, etc.)

> **Note:** It is still recommended to use fastboot-flashable images if available for your device.

# Fastboot-flashable image: installation instructions

## Preparations

If your device uses A/B partitions, make sure both slots run the same Android version.

Ensure `fastboot` is installed.

## Installation

Extract the downloaded archive, then run:

```bash
./flash_all.sh
```

You might need root permissions depending on your system configuration.

## Finalizing installation

The device will reboot automatically. When it boots up, you can unlock it using the default passcode `1234`.

# Recovery-flashable zipfile: installation instructions

## Preparations

If your device uses A/B partitions, make sure both slots run the same Android version.

Then boot into your preferred Android recovery.

## Installation

From recovery, open **ADB sideload mode** (under "Advanced" in TWRP) and run the following commands on your computer, replacing `ARCH_YYYYMMDD` with the version of DLS OS and `vendor-device` with the appropriate codename:

* `adb sideload dlsos-OFFICIAL-phosh-phone-rootfs-apiXX-ARCH-VERSION_DATE.zip`

To sideload development tools:

* `adb sideload dlsos-devtools-ARCH_YYYYMMDD.zip`

To sideload an adaptation bundle:

* `adb sideload dlsos-adaptation-vendor-device-ARCH_YYYYMMDD.zip`

> ⚠️ Restart sideload mode after each command by going back and selecting it again.

## Finalizing installation

Reboot the device. It should boot into **phosh**, the graphical user interface used by DLS OS. After one more reboot, you can unlock it with the default passcode `1234`.

## Troubleshooting

If the image doesn't boot and your userdata is not formatted as ext4, you may need to format it manually.

> ⚠️ **Warning: This will erase all data on the userdata partition!**

```bash
fastboot format:ext4 userdata
```
