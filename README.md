# Civ7_Colors
## Description
This repo contains a Python script that allows a user to edit the main colors of leaders in the video game Sid Meier's Civilization VII. 

> It is important to note that this code edits the Civilization VII source code directly, namely the following files: `playerstandardcolors.xml` and `playercolors.xml`. **This program lets you safely undo any changes to regain the original source code**.

## Functionality
| Button/Section Name | Description |
| --- | --- |
| "Select a Leader" | A list of leaders to select from as the target of the color assignment. |      
| "Choose Primary Color" | Displays a color picker to select a primary color. The primary color represents a civilization's **outer borders** and **background color** of city nameplates. |
| "Choose Secondary Color" | Displays a color picker to select a secondary color. The secondary color represents a civilization's **inner borders** and **text color** of city nameplates. | 
| "Reset Files" | Restores the game source code to its original state as if the mod never touched it. |
| "Subimt!" | Assigns the current primary and secondary color selection to the selected leader. |
