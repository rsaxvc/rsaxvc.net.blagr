Title:TempTale Direct Teardown
Author:rsaxvc
CreatedDateTime:2017-04-05T22:10:52
ModifiedDateTime:2017-04-05T22:10:52
Tag:STM32
Tag:ARM
Tag:flash
Tag:Teardown
---
<h2>A Handy Shipping Watchdog</h2>
<p>
Ever wonder if your kobe beef shipped quickly enough? If your
suspicous neighbor popped the lid on your coolerful of science
experiment? Some other, simple, zany reason? TempTale makes a line
of very handy environmental monitors. Drop one in when a sensitive
shipment is packed, and the receipient can quickly verify that
the package temperature was maintained through the shipment
by opening an automatically generated PDF file on the device.
The device appears as a USB mass storage device with a single PDF
file onboard.
</p>

<h2>But, how does it work?</h2>
<p>
Album link:<br/>
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/40925843@N03/albums/72157678556173453" title="TempTaleDirect"><img src="https://c1.staticflickr.com/4/3771/33284635230_b9c74882cb.jpg" width="375" height="500" alt="TempTaleDirect"></a>
</p><p>
Internally, it consists of an STM32 ARM microcontroller,
external serial flash, a coin cell battery with solder
terminals, some buttons, a high-speed and low-speed
oscillator, and a bare LCD panel.
</p><p>
The bare LCD is neat, as the static discharge on my fingers
caused a shimmer of pixels when I first touched it. Also, pay
attention to the front edge below: The glass has metal contacts
that then touch thin metal sheets embedded in the thick white-faced
foam strip at the front. Contact is held in by the case and pcb.
</p><p>
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/40925843@N03/32855532543/in/album-72157678556173453/" title="TempTale direct teardown"><img src="https://c1.staticflickr.com/4/3666/32855532543_34ffea30da.jpg" width="500" height="375" alt="TempTale direct teardown"></a>
</p><p>
Software-wise, only a few components are needed
for something like this.
<a href="http://www.keil.com/download/docs/362.asp">
A USB mass-storage driver</a>,
<a href="http://www.st.com/content/ccc/resource/technical/document/user_manual/61/79/2b/96/c8/b4/48/19/DM00105259.pdf/files/DM00105259.pdf/jcr:content/translations/en.DM00105259.pdf">
a filesystem driver</a>,
<a href="https://github.com/libharu/libharu/">
a PDF writer</a>,
and some custom logic to wake up the CPU from a
low-power event, likely the RTC alarm,
read the temperature, and store it to a
circular buffer. Just before USB enumeration,
write the circular buffer into a PDF file. Possible
example components are linked above.
</p><p>
These are really handy little devices, I hope they
become more widely deployed in the future for shipment
validation. Sensitech even makes models with GPS and
accelerometers as well.
</p>
