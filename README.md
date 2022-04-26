# AI-Car-Game

Check out our [website](http://aidi-2005-ai-car-game.s3-website.ca-central-1.amazonaws.com/)!

## Team Members
- Terence Yu
- Sarvang Konnur
- George Nikitakis
- Jaspreet Singh Marwah [(Zantorym)](https://github.com/Zantorym)
- Vaibhav Jain

## Installation and Usage

Dowload or clone repo
Go to the below link and download the .pkg and .exe files
https://drive.google.com/drive/folders/1HMJa5bPTzg0LzoAVUNR8ag7bdd_LjEqO?usp=sharing

- place the .pkg file in Code/build/main_menu/ directory
- place the .exe file in Code/dist/ directory

Run .exe file to enjoy :)

## Progress so far

We have a functioning game where the user can control a car's speed and direction. The user can select from 3 different maps using the main menu. We've implemented collision detection, i.e., when the game is provided an image of a hand-drawn race track, it is able to figure out the boundaries of the track for collision. The car is fitted with 13 sensors in the form of rays emitting from the car in different directions. These sensors will work like LIDAR to tell the AI driving the car how far it is from objects surrounding it. The game currently has 3 different maps. If at any time a user crashes, the game stops and they need to restart. If a user is able to successfully complete a lap without crashing, the game gives them a victory message. The game then records the details of the user's lap such that it may feed those details to an AI model which then uses that information to learn to play the game. 

## Work in-progress

We're currently in the final phases of improving the AI model's track run.


![AI Demo Run](https://user-images.githubusercontent.com/92330440/164180088-d2949956-fc8a-4129-871d-3bdee96904ae.gif)

