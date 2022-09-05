import pickle
import subprocess
import eel
# import test

# initializing the application in the current directory
eel.init("./")

# using the eel.expose command


@eel.expose
def generate(config):
    print(config)
    with open("myconfig", 'wb') as f:
        pickle.dump(config, f)
    subprocess.run(
        ["blender", "RuletaWithAnim.blend", "--python", "casino.py"])
    return "Done"


# starting the application
eel.start("./web/index.html")
