# jetson-vision

Copy files from laptop to Jetson w/o copying subfolders.

`scp GRT2022Vision/* grt@10.1.92.94:~/GRT2022Vision`

fix flickering left stream because turret is making modificaitons on the camera frame so make a copy or something before passing to turret
fix lagging camera stream