# carrotlib🥕

## Caveat

+ This project is NOT ready for production.
+ This project mainly serves for my own games.

## Create a project

Create a folder, for example `projects/<your_project>`
and run the following command to copy template files to all projects located in `projects` folder.

```bash
python scripts/sync_template.py
```
Create a `main.py` in `<your_project>` folder. And this is the entry point of your game.

```python
# main.py
import carrotlib as cl

class MyCallbacks(cl.Callbacks):
    def on_ready(self):
        super().on_ready()

        """Initialize your game here."""

cl.main(MyCallbacks(), design_size=(1280, 720), title='<your_project>')
```

## Build win32

```
mkdir build
cd build
mkdir win32
cd win32
cmake ..\..
cmake --build .
Debug\Game.exe ..\..\projects\<your_project>
```

## Build android

First sync your project folder with the android assets folder.
```bash
python prebuild <your_project>
```

Run the following commands to build the android project.
```bash
pip install cmake==3.26.3
cd android
chmod +x ./gradlew
./gradlew --no-daemon assembleDebug
```

## Third party libraries

This project uses the following libraries:

+ [pocketpy](https://github.com/blueloveTH/pocketpy)
+ [raylib](https://github.com/raysan5/raylib)
+ [box2d](https://github.com/erincatto/box2d)