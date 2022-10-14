# casinopy
Blender automation script for assistance in creation of a casino game, which started out only as a blender automation and video rendering project.<br> 
Due to the need of some Physics features, the game project had to be reimplemented from scratch in Unity engine. <a href='https://github.com/ShivangMishra/RouletteGame'>It's here</a>. <br> I've left this script here to serve as revision code for some edge case <a href="https://docs.blender.org/api/current/index.html">bpy</a> operations.<br>
This project uses <a href='https://github.com/python-eel/Eel'> eel </a > for creating a simple GUI. <br>
The inputs from the eel GUI are passed to the main.py script. The main.py saves the configuration locally. <br>  
The main.py file runs casino script with a blender context (need to set up blender path). <br>
casino.py handles all the blender operations.
