# Parachuter
old school parachuter game in python using pygame.
Running main.py opens the game. The buttons are clicked with the mouse.
In game, the controls are left and right arrow keys to aim the cannon, space to fire a bullet, and p to pause.

## December 18 update:
Game is in working order.

The enemies spawn rate is an increasing rate, and maybe should be slowed down for future games. Will possibly add 
what is effectively "Levels" where, after a certain score increase, the rate increases at that point. 

Bullets need a slight fix, they struggle to fire just left or right of directly upward. The angle of the sprote is correct,
but the angle of movement is not. I believe this is due to delta_x being so close to 0 when calculating the movement,
whereas the angle of the sprite is a direct roation via degrees. 

I am taking a break to start Snake, to reaffirm the basics (at this point I am no longer doing basic pygame work) but will return to add 
animations and improve the above. 
