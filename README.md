# GRT2022Vision

Copy files from laptop to Jetson w/o copying subfolders. 
`scp GRT2022Vision/* grt@10.1.92.94:~/GRT2022Vision`

Kill TCP port so you don't need to reboot every time you run the socket. It takes some time to fully kill
`sudo fuser -k 5800/tcp`

- fix by removing outliers outside of where most of the contours are positioned x-wise 
- debug angles code w/ the calib function in turret.py
- udev by position on usb hub (jetson) in case first camera dies

other things
- test w/ different object points
- try regular solvepnp not solvep3p and see how it is
- ligerbots for their solvepnp procedure (also open on my phone)
- any way to wrap socket code 
- any way to abstract the local vs jetson; image vs video capture testing?
- filtering via aspect ratio (can we grab more of the tapes that only reflect half of their tape?)
- what if we just use the middle three or four, ignoring tiny pieces of tape?
- can we have redundant vision methods; ie: using calib; fixed angles/heights; solvepnp

if getting negative values from solvepnp, might be due to incorrect image resoolution (doesn't match camera matrix)

- record possible resolutions 