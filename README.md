# How to use Gige camera with Raspberry Pi 3B+

This is a step by step guide to install the tiscamera software on a Raspberry Pi 3B+ and use it with opencv.

## install dependencies for tiscam

`sudo apt install autoconf aravis-tools glade cmake g++ git gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-x gtk-doc-tools intltool libqt5gstreamer-dev libaudit-dev libaudit1 libgirepository1.0-dev libglib2.0-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libnotify-dev libnotify4 libpcap-dev libpcap0.8 libtinyxml-dev libudev-dev libudev1 libusb-1.0-0-dev libxml2 libxml2-dev libzip-dev pkg-config python-setuptools python3-sphinx qtbase5-dev qtdeclarative5-dev uvcdynctrl  -y`

`pip3 install ninja`

`sudo apt install gstreamer1.0-tools -y`

`export PATH="$HOME/.local/bin:$PATH"`

## install tiscam

`git clone --recursive https://github.com/TheImagingSource/tiscamera.git`

`cd tiscamera`

`mkdir build`

`cd build`

`cmake -DBUILD_ARAVIS=ON -DBUILD_GST_1_0=ON -DBUILD_TOOLS=ON -DBUILD_V4L2=ON -DCMAKE_INSTALL_PREFIX=/usr ..`

`make`

`sudo make install`

## start tcam service

`sudo systemctl daemon-reload`

`sudo systemctl enable tcam-gige-daemon.service`

`sudo systemctl start tcam-gige-daemon.service`

## start gui

`tcam-capture`

## install opencv with aravis

`cd ~`

`git clone  https://github.com/opencv/opencv`

`cd opencv`

`mkdir build && cd build`

`cmake -D CMAKE_BUILD_TYPE=RELEASE -D INSTALL_C_EXAMPLES=OFF -D PYTHON_EXECUTABLE=/usr/bin/python/aravis_opencv/gige_py/bin/python -D WITH_GSTREAMER=ON  -D WITH_ARAVIS=ON  ..`

`make -j4`

## last 2 percent need lots of memory, you may need to increase swap temporarily, use make -j1 to save some memory for the last bit.

## ------ increase swap --------

`sudo dphys-swapfile swapoff`

`sudo nano /etc/dphys-swapfile`

`CONF_SWAPSIZE=1024`

`sudo dphys-swapfile setup`

`sudo dphys-swapfile swapon`

## -----------------------------

`sudo make install`

`export GI_TYPELIB_PATH="/usr/lib/x86_64-linux-gnu/girepository-1.0"`

`export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH`

## Install Aravis

`sudo apt install meson ninja-build`

`sudo pip3 install meson`

`sudo ln -s /usr/local/bin/meson /usr/bin/meson`

`cd ~`

`wget https://github.com/AravisProject/aravis/releases/download/0.8.26/aravis-0.8.26.tar.xz`

`tar -xf aravis-0.8.26.tar.xz`

`cd aravis-0.8.26`

`meson --prefix /usr --buildtype=plain build`

`cd build`

`ninja`

`sudo ninja install`

`sudo ldconfig `

## Install opencv

`pip install opencv-python==4.5.3.56`

`pip install --upgrade numpy`
