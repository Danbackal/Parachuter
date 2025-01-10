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

## January 10 Update:
Hey it's been a bit.
I fixed the menu clicking so we don't get a double click when switching from pause to new game. 
The functions are messy and very unoptimized but I like the direction it is heading.
Instead of working on a new game, I am going to add a lot more to this one.

### FUTURE DEVELOPMENT PLANS
I am looking into adding visual changes (header, current level, bullets and coins) as well as an upgrade system.

Current upgrade thought is we keep track of coins. Its easy now, to spray and pray, so we will start with a set amount of bullets.
Enemies, when killed, will drop a set amount of money. From the pause menu, there will either be a new tab, or just an overlay, that lets you upgrade.
I am picturing things like:
- Double Barrel: two bullets for the price of one
- Armor Piercing Rounds: upgradable, bullets pass through multiple enemies (1, 2, 3, all)
- Explosive Rounds: upgradable, shrapnel shoots off when hitting an enemy. May only travel certain distance. May only make a set number of shrapnel. May only kill if it hits the parachute specifically? Needs work.
- Buy more bullets
