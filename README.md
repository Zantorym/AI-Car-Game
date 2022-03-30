# AI-Car-Game

## Team Members
- Terence Yu
- Sarvang Konnur
- George Nikitakis
- Jaspreet Singh Marwah [(Zantorym)](https://github.com/Zantorym)
- Vaibhav Jain


## Progress so far

We have a functioning game where the user can control a car's speed and direction. We've implemented collision detection, i.e., when the game is provided an image of a hand-drawn race track, it is able to figure out the boundaries of the track for collision. The car is fitted with 13 sensors in the form of rays emitting from the car in different directions. These sensors will work like LIDAR to tell the AI driving the car how far it is from objects surrounding it. The game currently has 3 different maps. If at any time a user crashes, the game stops and they need to restart. If a user is able to successfully complete a lap without crashing, the game gives them a victory message (we are currently working on the game recording the details of the user's lap such that it may feed those details to an AI which would use that information to learn to play the game). 

## Work in-progress

We're currently in the final phases of implementing a main menu from which a user can change maps and add obstacles. We are also working on integrating Imitation Learning to the project, such that an AI learns to play the game based on a trial run provided by the user.


![Demo](https://user-images.githubusercontent.com/35334286/160731510-cb481f4d-fd97-4d19-9e31-63eb43b77ab0.gif)
