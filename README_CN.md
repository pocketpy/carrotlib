# CarrotLib🥕

CarrotLib🥕是与[pocketpy](https://github.com/pocketpy/pocketpy)搭配使用的一套面向对象的游戏开发框架。


## 一个最简单的例子

```python
# main.py
import carrotlib as cl		# 导入CarrotLib🥕

class MyGame(cl.Game):
    def on_ready(self):
        super().on_ready()
        # TODO: 初始化你的游戏

    @property
    def design_size(self):
        return (320, 180)	# 返回游戏的设计分辨率
```

当脚本被加载后，CarrotLib🥕会自动搜索`main.py`中，第一个继承自`cl.Game`的类进行实例化。

## 对象树与节点

CarrotLib🥕使用类似Unity和Godot的树形结构来管理所有游戏对象，这些游戏对象都继承自一个公共的父类`Node`。

在游戏初始化时，根节点被自动创建出来，你将在`MyGame.on_ready`函数中创建自己需要的节点。

> 你可以使用`cl.g.root`来访问根节点。`cl.g`是一个特别的模块，里面包含了许多全局数据。

#### `Node`的创建

+ `Node.__init__(self, name=None, parent=None)`

`Node`接受两个参数，`name`为节点的名字，名字在同一层级下是唯一的，因此你可以通过`.children`来用名字查找子节点。`parent`可以设置节点的父节点，当它为`None`时，父节点为根节点。

#### `Node`的销毁

+ `Node.destroy(self)`，立即销毁节点
+ `Node.destroy_later(self,  delay: float)`，在若干秒后销毁节点

节点的销毁是将其从对象树中移除，它的数据仍将短暂存留在内存中，直到Python GC发生。

#### `Node`的虚方法

+ `Node.on_ready(self)`，当节点即将进入第一帧的逻辑时，调用一次
+ `Node.on_update(self)`，每帧调用一次，重写此函数以实现游戏逻辑
+ `Node.on_render(self)`，每帧调用一次，重写此函数以渲染游戏场景中的对象（使用世界空间的变换矩阵）
+ `Node.on_render_ui(self)`，每帧调用一次，重写此函数以渲染UI对象（使用UI空间的变换矩阵）
+ `Node.on_destroy(self)`，当节点即将被销毁时，调用一次

#### `Node`的坐标变换

每个`Node`实例中都存储了位置、旋转和缩放的信息。

+ `Node.position: vec2`，节点的本地坐标
+ `Node.rotation: float`，节点的本地旋转角度（顺时针、弧度制）
+ `Node.scale: vec2`，节点的缩放值
+ `Node.global_position: vec2`，节点的世界坐标

要获取节点在世界空间下的更详细数据，可以使用`Node.transform(self) -> mat3x3`，该函数返回一个从世界空间到节点本地空间的变换矩阵。

#### 在对象树中查找节点

+ `Node.children: dict[str, Node]`，节点的子节点
+ `Node.parent: Node`，节点的父节点
+ `Node.get_node(self, path: str)`，以相对路径逐级查找子节点

## 控件

控件`Control`是`Node`的子类，用于在UI上绘图和实现交互。

+ `cl.controls.Image`，图片控件
+ `cl.controls.Label`，标签控件，用来绘制单行的短文本
+ `cl.controls.Text`，文本控件，用来绘制多行的长文本
+ `cl.controls.Container`，容器控件，为其他控件提供定位能力

## 协程

CarrotLib🥕提供了类似Unity的协程支持。协程对象是一个标准的Python迭代器，通过一个节点来执行。

+ `Node.start_coroutine(self, coro)`，启动一个协程
+ `Node.stop_coroutine(self, coro)`，停止一个协程
+ `Node.stop_all_coroutines(self)`，停止所有协程

以下是一个等待5秒后打印`Hello, world`的协程。

```python
def hello_coro():
    yield from cl.WaitForSeconds(5.0)
    print("Hello, world")
    
# 启动协程：node.start_coroutine(hello_coro())
```

## 绘图

#### 绘制纹理

`cl.draw_texture(transform: mat3x3, tex: rl.Texture2D, src_rect: rl.Rectangle=None, flip_x=False, flip_y=False, color: rl.Color = None, origin: vec2 = None)`

+ `transform`，基础变换
+ `tex`，纹理
+ `src_rect`，源矩形
+ `flip_x`，翻转x轴
+ `flip_y`，翻转y轴
+ `color`，颜色
+ `origin`，锚点（默认为中心)

#### 绘制文本

`cl.draw_text(font: rl.Font, pos: vec2, text: str, font_size: int, color: rl.Color, spacing: int = 0, line_spacing: int = 0, origin: vec2 = None)`

#### 绘制圆

`cl.draw_circle(center: vec2, radius: float, color: rl.Color, solid=True)`

#### 绘制矩形

`cl.draw_rect(rect: rl.Rectangle, color: rl.Color = None, origin: vec2 = None, solid=True)`

#### 绘制线段

`cl.draw_line(begin: vec2, end: vec2, color: rl.Color)`

## 资源管理

游戏中会用到很多资源，比如纹理、声音、字体和源代码等，它们被存放在对应的项目文件夹中。

根据平台的差异，CarrotLib🥕提供了三套方案来打包资源，并提供一组平台无关接口来加载资源。

1. **标准文件系统**。在Windows/Linux/MacOS上，资源直接存放在文件系统中。此时，资源加载能力由C语言标准库函数所支持。
2. **Android资源数据库**。在Android上，资源被复制到一个特殊的assets目录中，并使用AAAssetManager来加载资源。
3. **硬编码资源数据库**。若1和2的方案均不可用，资源将会被转换成字节数组，并硬编码到一个`.cpp`文件中，iOS和Web平台只能使用这种方法。

#### 加载二进制

+ `cl.load_asset(path: str) -> bytes`，从指定路径加载资源，返回资源本身的字节
+ `cl.list_assets(root: str) -> list[str]`，列出指定目录下的所有资源路径


#### 加载纹理

你可以使用`load_texture`函数从资源库中加载纹理（首次加载后缓存）。

```python
tex = cl.load_texture("path/to/texture.png")
```

如果你不希望自动缓存纹理，可以使用更加底层的`rl.LoadTexture`和`rl.UnloadTexture`函数。

#### 加载字体

你可以使用`load_font`函数从资源库中加载字体（首次加载后缓存）。

```
font: rl.Font = cl.load_font("path/to/font.ttf")
```

在CarrotLib🥕中，字体所包含的字符集是在加载时确定的。默认的`load_font`函数只会构建ASCII字符集。

若字体中包含中文，你需要使用`load_font_cjk`来加载，它会为字体额外构建4000个常用的汉字字符。

```
font: rl.Font = cl.load_font_cjk("path/to/font.ttf")
```


#### 加载声音

你可以使用`load_sound`函数从资源库中加载声音（首次加载后缓存）。

```
sound: rl.Sound = cl.load_sound("path/to/sound.wav")
```

> 要播放一次性的声音，可使用`cl.play_sound`。

## 构建与发布

在构建之前，运行如下命令来预构建。

```
python scripts\prebuild.py projects\<your_project>
```

#### Windows/Linux/MacOS

```
mkdir build
cd build
mkdir win32
cd win32
cmake ..\..
cmake --build .
Debug\Game.exe ..\..\projects\<your_project>
```

#### Android

```bash
cd android
chmod +x ./gradlew
./gradlew --no-daemon assembleDebug
```

#### iOS

```
bash build_ios.h
```

#### Web

```
bash build_web.h
python -m http.server -d build/web
```

