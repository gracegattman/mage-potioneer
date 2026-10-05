(Notes:
	- run main.py to run game!
	- pip install pytmx is necessary for the map parsing
	- deprecated folder to show progress in certain files)

Some of the new developments for the final deliverable:
- Credit to the creator (me!) added to bottom of main menu screen
- Unique main menu, collection, and mixing music tracks now implemented!
- Game over screen when player runs out of ingredients before completing a level's potions
	- Clicking reroutes to main menu, where player can retry with the power-ups gained
	  from their previous playthrough
- Glow FX implemented upon ingredient collection
- Big UI updates to mixing phase
	- Larger ingredient and potion icons
	- Ingredients labeled by name as well as amount
	- Potions and Ingredients clearly categorized on their sides of the cauldron

Old Developments from Milestone 3:
- Created 4 layered maps with player collision implemented with props, inaccessible tiles, etc (10 pts)
- Expanded on ingredient placement to prevent ingredients from being placed in inaccessible spaces (5 pts)
- Connected collection and mixing modes with main.py file (5 pts)
- Implemented countdown timer that changes based on level progression (5 pts)
- Implemented better UI for mixing mode (total 30 pts)
	- Collected ingredient inventory (resets every level) displays with amount and cannot go negative (5 pts)
	- Ingredient icons + names displayed to show player what is added to cauldron (5 pts)
	- Unique potion icons displayed with overlay when first created (5 pts)
	- Final/milestone potions displayed with overlay once all 4 main potions per level are made (10 pts)
	- Potion inventory (resets every level) shown on right side of screen with ingredients involved (5 pts)
- Implemented progress.py to keep track of power-ups gained for different levels and game progression (5 pts)
- Implemented FX for potion creation (10 pts)
- Progression milestones/power-ups implemented where relevant (x2 speed, expanded collection radius, etc) (10 pts)
- Created buttons + interfacing for main menu (total 20 pts)
	- Main menu functionality for game control (10 pts)
	- Game instructions window for simplicity (10 pts)

Old Development from Milestone 2:
- Gathered all game assets (character spritesheet, ingredients, cauldron, FX, tilemap, etc.)
- Created 1600x1600 pixel map for collection mode based on tilemap
- Implemented player movement functionality based on arrow key inputs
- Implemented player animation based on spritesheet image sizing, both run and idle
- Implemented ingredient file input based on folder contents
- Implemented randomized ingredient placement
- Implemented collision detection between player and ingredients
- Implemented camera movement to follow player movement across map
- Implemented storage system to keep track of gathered ingredients
- Implemented some basics of mixing system:
	- Keeping track of what ingredients are input
	- Displaying cauldron and ingredients available on screen
	- Added ingredients based on user clicking on screen