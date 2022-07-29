# PyFlax

https://github.com/Polynominal/PyFlax

##Pure python tweening library

This is python flax, just like flax moves in the wind so will your vars, it is inspired by:
https://github.com/rxi/flux

##Install
to install simply drop the Tween.py in your project

##Design
Its mainly designed with classes in mind and modifiying the vars that they hold, however it can also modify independent vars too.
The only thing you need is delta time.
##Easing
Currently theres only "Linear" easing however you can easily add your own easing types in the Tween.py dictionary called "ease"
##Usage
vars is a dictionary list reflecting your class and expected value 

Timer.to(time,object,vars,easing)

*default easing is "Linear"

```python
from Tween import Tween
timer = Tween()
class box(x,y)
  def __init__(self,x,y):
      self.x = x 
      self.y = y 
inst = box(0,0)

tween = Timer.to(1,inst,{"x":20})

#your update loop 
timer.update(dt)
```
This will move the box from 0 to 20 in the x direction in 1 second.
#Advanced(Untested):
You can use a list as your var/item see:
```python
inst.color = [0,0,0]
tween = Timer.to(1,inst,{"color":[255,255,255]})
```
schedule another tween:
```python
inst.color =[0,0,0]
inst.x = 0 
inst.y = 0 
tween = Timer.to(1,inst,{"x":100,"y":100).after(1,{"color":[255,255,255]})
```
This will move the box to [100,100] in 1 second and after set its color from [0,0,0] to [255,255,255]

You can have as many vars as you want but they must be int.

##Planned features:
  stop a tween sequence.
  other types of easing, eg elastic and interface for costum methods.
  shortcut for creating single var tweens.

