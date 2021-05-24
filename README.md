# LRL

Low Rim League basketball

The LRL is a low rim basketball league consisting of 3 players on each team with a game played to 50 in a half court set on about 8.75ft rims.

simulation.py is a Python file that can simulate single games, a team's season, or the entire league's season. Each team has a rebound rate, offensive efficiency, defensive efficiency, and three players. Each player has a shot tendency, a two point tendency, 2pt %, and 3pt %. 

The program loops through possessions until one team reaches 50 points. Each possession consists of randomly determining a player to shoot, randomly deciding whether they shoot a 2 or a 3, and finally randomly calculating if the shot attempted was made. If the shot was made, possession switches to the other team. However, if the shot was missed, the two teams' rebound rates determine who gets the rebound and the possession. Offensive and defensive efficiency rates also help or hurt the success of a shot attempt. This process is repeated for the entire game. 
