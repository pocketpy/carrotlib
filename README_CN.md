# CarrotLib🥕

CarrotLib🥕 是与 pocketpy 搭配使用的一套游戏开发框架。


## 一个最简单的例子

```python
# 导入 CarrotLib🥕
import carrotlib as cl

class MyGame(cl.Game):
    def on_ready(self):
        super().on_ready()
        # 初始化你的游戏

    @property
    def design_size(self):
        # 返回游戏的设计分辨率
        return (320, 180)
```

# 核心特性

## 对象树


## 资源管理

你的游戏可能会用到很多资源，比如纹理、声音、字体和源代码等，它们被存放在对应的项目文件夹中。
根据平台的差异，CarrotLib🥕 提供了三套方案来打包资源，并提供一组平台无关接口来加载资源。
1. 标准文件系统。在Windows/Linux/MacOS上，资源直接存放在文件系统中。此时，资源加载能力由C语言标准库函数所支持。
2. Android资源数据库。在Android上，资源被复制到一个特殊的assets目录中，并使用AAAssetManager来加载资源。
3. 硬编码资源数据库。若1和2的方案均不可用，资源将会被转换成字节数组，并硬编码到一个`.cpp`文件中，iOS和Web平台只能使用这种方法。

### 加载二进制

+ `load_asset(path: str) -> bytes`，从指定路径加载资源
+ `list_assets(root: str) -> list[str]`，列出指定目录下的所有资源


### 加载纹理

你可以使用`load_texture`函数从资源库中加载纹理。
纹理在第一次加载后将被缓存，后续相同参数的调用将直接返回缓存的纹理。

```python
import carrotlib as cl
tex = cl.load_texture("path/to/texture.png")
```

如果你不希望自动缓存纹理，可以使用`rl.LoadTexture`和`rl.UnloadTexture`函数。

### 加载帧动画


### 加载字体


### 加载声音



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
