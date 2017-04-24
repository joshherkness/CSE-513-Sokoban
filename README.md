# CSE-513-Sokoban

Sokoban solver created using Q-Learning.

## Setup

1. Ensure you have Python3 installed
2. Ensure you have `pip3` installed
3. Install matplotlib `$ pip3 install matplotlib`
    - https://matplotlib.org/faq/installing_faq.html
4. Install sokoenginepy `$ pip3 install sokoenginepy`
    - http://sokoenginepy.readthedocs.io/en/latest/#

## Running 

```
$ python3 sokoban.py
$ python3 sokoban.py -f 'levels/level_0.txt'
$ python3 sokoban.py -f 'levels/level_1.txt'
$ python3 sokoban.py -f 'levels/level_3.txt'
$ python3 sokoban.py -f 'levels/level_4.txt'
$ python3 sokoban.py -f 'levels/level_5.txt'
$ python3 sokoban.py -f 'levels/level_6.txt'
$ python3 sokoban.py -f 'levels/level_7.txt'
```

### Custom (Advanced)

The following options can be passed into the script using the corresponding flags.

```
-l : Learning rate 
-d : Discount factor
-f : Level file
-a : Max actions 
-e : Episodes
-r : Render level
-p : Plot data
```

An example of these options being used can be seen below.  **Note**: the flags must appear in the order listed.

```
$ python3 sokoban.py -l 0.3 -d 0.4 -f '~/.../custom_level.txt' -a 1000 -e 450 -r False -p False
```

### Help

A full list of arguments can be seen using the help flag.

```
$ python3 sokoban.py -h
```

## Examples

https://www.youtube.com/playlist?list=PLQZtoUQgc-vOQVVSYV5h5U2Et5Ei_BNfa

