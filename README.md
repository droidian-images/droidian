Droidian
========

Droidian is a GNU/Linux distribution based on top of Mobian, a Debian-based distribution for mobile devices. The goal of Droidian is to be able to run Mobian on Android phones.

This repository is the canonical place to get Droidian images.

# Which image to get?

There are two different types of images:

* Fastboot-flashable image
* Recovery-flashable zipfile

Fastboot-flashable images are, instead, the recommended way to install Droidian. These images are device specific, so if you want one for your device you should create one yourself.
Fastboot-flashable images support Full Disk Encryption, and make use of the whole userdata partition.

The recovery flashable zipfile needs to be flashed via a suitable Android recovery (such as TWRP). Recovery flashable zipfiles are generic, and are useful to test drive Droidian or in early device porting stages.
You should pick up the correct zipfile for your specific device:

* Device with an Android 9 vendor: api28
* Device with an Android 10 vendor: api29
* Device with an Android 11 vendor: api30
* Device with an Android 12/12.1 vendor: api32
* Device with an Android 12/12.1 vendor: api33

If you're in doubt, and there is a fastboot-flashable image available for your device, it's recommended to use that.

## Recovery-flashable zipfile: bundles

Recovery flashable zipfiles support the addition of *bundles*, which allow to add functionality directly during the flashing process.

Currently available bundles:

* Devtools: Useful development tools for porters, not available in nightlies as they're embedded in the rootfs
* Adaptation bundle: Device specific bundle (containing kernel, device-specific settings, etc)

**Keep in mind that is still recommended using fastboot-flashable images if available for your device.**

# Fastboot-flashable image: installation instructions

## Preparations

If your device is A/B device, it is necessary to have both slots on same Android version.

Ensure you have `fastboot` installed.

## Installation

Extract the downloaded archive, then run:

```
./flash_all.sh
```

You might need to execute that at root depending on how your system is configured.

## Finalizing installation

The device will reboot automatically. When the device has booted, you can unlock the device with the default passcode `1234`.

# Recovery-flashable zipfile: installation instructions

## Preparations

If your device is A/B device, it is necessary to have both slots on same Android version.

Then, boot your favourite Android recovery.

## Installation

From recovery open adb sideload mode (under advanced on TWRP) and run following commands on your computer replacing `ARCH_YYYYMMDD` with the version of Droidian and `vendor-device` with the vendor and device codenames:

* `adb sideload droidian-OFFICIAL-phosh-phone-rootfs-apiXX-ARCH-VERSION_DATE.zip`

If you want to sideload devtools:

* `adb sideload droidian-devtools-ARCH_YYYYMMDD.zip`

If you want to sideload an adaptation bundle:

* `adb sideload droidian-adapatation-vendor-device-ARCH_YYYYMMDD.zip`

Note that you have to restart the sideload mode by tapping back and starting sideload again before every `adb sideload command`.

## Finalizing installation

Now, you have to reboot the device. It should boot to phosh (a graphical user interface used by Droidian) after rebooting once more automatically. When the device has booted, you can unlock the device with the default passcode `1234`.

## Troubleshooting

If the image does not boot and your userdata is not an ext4 partition, you might try formatting it. **Note that this is a destructive operation, you cannot recover files from userdata afterwards!**

* `fastboot format:ext4 userdata`
