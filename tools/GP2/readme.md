# GP2 Scripts and Apps

These are really quick hacky scripts thrown together to research the GP2. Feel free to push a clean up. 

* __extracth10.py__  Extracts the various firmware sections. Ignores the signature. Either mount or use 7-zip to extract roofs from section_id08_type03.bin
* __extracth10dtb.py__ Extracts the Device Tree for the RTOS & Linux. Requires FdtBlobParse
* __extracth10bmpd.py__ Extracts all the bitmaps for the front and rear displays. requires decompress.py
* __extracth10romfs.py__ Extracts the romfile system out of a GP2 binary
* __busybox__ Busybox with all the applets built for the GP2
* __ida__ Scripts and loaders for GP2 based GoPro Cameras
