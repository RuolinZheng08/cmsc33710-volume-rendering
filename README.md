# cmsc33710-volume-rendering
[Python] Volume Rendering and Ray Casting

```
./rrendr go \
-i cube.nrrd \
-fr 6 12 5 -at 0 0 0 -up 0 0 1 \
-nc -2.3 -fc 2.3 -fov 14 \
-sz 320 280 \
-us 0.03 -s 0.03 -k bspln3 -p rgbalit -b over \
-nt 2 -lut lut.nrrd -lit rgb.txt -o cube-rgb.nrrd

python3 go.py \
-i utils/cube.nrrd \
-fr 6 12 5 -at 0 0 0 -up 0 0 1 \
-nc -2.3 -fc 2.3 -fov 14 \
-us 0.03 -s 0.03 \
-lut utils/lut.nrrd -lit utils/rgb.txt \
-sz 320 280 -nt 2 -o utils/cube-rgb-py.nrrd

overrgb -i cube-rgb.nrrd -b 0 0 0 -o cube-rgb.png
overrgb -i cube-rgb-py.nrrd -b 0 0 0 -o cube-rgb-py.png
```
