import imgui
from imgui.integrations.glfw import GlfwRenderer
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pyimgui as imgui

import glfw
import OpenGL.GL as gl
import os, sys

from playground import backend
from playground.IconsFontAwesome6 import IconsFontAwesome6 as Icons
from playground.IconsFontAwesome6Brands import IconsFontAwesome6Brands as IconBrands


class Timer:
    def __init__(self, timeout: float):
        self.timeout = timeout
        self.start_time = imgui.get_time()

    def test_and_set(self):
        delta = imgui.get_time() - self.start_time
        if delta >= self.timeout:
            self.start_time = imgui.get_time()
            return True
        return False


class ProjectView:
    def __init__(self):
        self.task = None

        self.devices = []
        self.framework_compile_time = None
        self.timer = Timer(1.0)

        glyph_ranges = imgui.get_io().fonts.get_glyph_ranges_chinese()
        imgui.get_io().fonts.add_font_from_file_ttf(
            "playground/assets/fonts/ark-pixel-12px-monospaced-zh_cn.otf",
            24,
            glyph_ranges=glyph_ranges
        )
        icon_min, icon_max = Icons.ICON_MIN, Icons.ICON_MAX
        imgui.get_io().fonts.add_font_from_file_ttf(
            f"playground/assets/fonts/{Icons.FONT_ICON_FILE_NAME_FAR}",
            24,
            font_config=imgui.FontConfig(merge_mode=True),
            glyph_ranges=imgui.core.GlyphRanges([icon_min, icon_max, 0])
        )
        icon_min, icon_max = IconBrands.ICON_MIN, IconBrands.ICON_MAX
        self.default_font = imgui.get_io().fonts.add_font_from_file_ttf(
            f"playground/assets/fonts/{IconBrands.FONT_ICON_FILE_NAME_FAB}",
            24,
            font_config=imgui.FontConfig(merge_mode=True),
            glyph_ranges=imgui.core.GlyphRanges([icon_min, icon_max, 0])
        )

        self.source_font = imgui.get_io().fonts.add_font_from_file_ttf(
            "playground/assets/fonts/ark-pixel-12px-monospaced-zh_cn.otf",
            12,
            font_config=imgui.FontConfig(oversample_h=2, oversample_v=2),
            glyph_ranges=glyph_ranges
        )

        imgui.get_io().delta_time = 1.0 / 60.0
        
        self.root = None
        self._selected_file = None
        self._selected_content = None
        self.open_project("examples/01_HelloWorld")

    def poll_task(self):
        if self.task is not None:
            try:
                next(self.task)
            except StopIteration:
                self.task = None

    def start_task(self, task):
        if task is None:
            return
        if self.task is not None:
            return
        self.task = task

    @property
    def selected_file(self):
        return self._selected_file
    
    @property
    def selected_content(self):
        return self._selected_content
    
    @selected_file.setter
    def selected_file(self, value: str):
        self._selected_file = value
        if value:
            try:
                with open(self.selected_file_abspath, "rt", encoding='utf-8') as f:
                    self._selected_content = f.read()
            except Exception as e:
                print(e)
                self._selected_content = None
        glfw.set_window_title(
            glfw.get_current_context(),
            f"CarrotLib🥕 Playground - {os.path.basename(self.root)} - {self.selected_file}"
        )

    def open_project(self, root: str):
        if not root or not os.path.exists(root):
            return
        self.root = root
        self.selected_file = 'main.py'
        print('打开项目:', self.root)

    @property
    def root_abspath(self):
        if not self.root:
            return None
        return os.path.abspath(self.root)
    
    @property
    def selected_file_abspath(self):
        if not self.selected_file:
            return None
        return os.path.join(self.root_abspath, self.selected_file)
    
    def render_console(self):
        input_bg_color = (44/255, 40/255, 52/255, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *input_bg_color)

        # allow line wrap
        for line in backend.get_logs():
            imgui.push_text_wrap_pos(0)
            imgui.text(line)
            imgui.pop_text_wrap_pos()

        imgui.text("")
        
        if self.task is not None:
            imgui.set_scroll_here_y(1.0)
        imgui.pop_style_color()

    def render_file_hierarchy(self, root: str):
        # use recursive function to render file hierarchy
        flags = imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH
        for item in os.listdir(root):
            item_path = os.path.join(root, item)
            if os.path.isdir(item_path):
                if imgui.tree_node(item, flags=flags):
                    self.render_file_hierarchy(item_path)
                    imgui.tree_pop()
            else:
                imgui.tree_node(item, flags=imgui.TREE_NODE_LEAF | imgui.TREE_NODE_NO_TREE_PUSH_ON_OPEN | flags)
                if imgui.is_item_clicked(0):
                    self.selected_file = os.path.relpath(item_path, self.root)

    def render_text_editor(self):
        input_bg_color = (44/255, 40/255, 52/255, 1.0)
        input_fg_color = (171/255, 178/255, 191/255, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *input_bg_color)
        imgui.push_style_color(imgui.COLOR_TEXT, *input_fg_color)
        if self.selected_file:
            flags = imgui.INPUT_TEXT_READ_ONLY
            if self.selected_content is None:
                buffer = "[不支持的文件类型]"
            else:
                buffer = self.selected_content
            width, height = imgui.get_window_size()
            with imgui.font(self.source_font):
                buffer = imgui.input_text_multiline(
                    "##source",
                    buffer,
                    width=width,
                    height=height,
                    flags=flags
                )
        imgui.pop_style_color(count=2)

    def render(self):
        window_width, window_height = imgui.get_window_size()
        window_height -= 20

        # two column with splitter, drag to resize width
        imgui.begin_child("File Hierarchy", width=window_width * 0.25, height=window_height)

        full_width = imgui.get_window_width()
        if imgui.button(f"{Icons.ICON_FOLDER} 新建项目", width=full_width):
            if not os.path.exists("projects"):
                os.mkdir("projects")
            path = backend.open_directory("选择一个空文件夹作为新项目的存储位置", "projects")
            if path:
                if len(os.listdir(path)) != 0:
                    print("文件夹不为空，无法创建项目")
                else:
                    backend.new_project(path)
                    self.open_project(path)
        if imgui.button(f"{Icons.ICON_FOLDER_OPEN} 打开项目", width=full_width):
            path = backend.open_directory("选择项目", "examples")
            if path:
                self.open_project(path)
        imgui.spacing()

        if self.root:
            self.render_file_hierarchy(self.root)

        imgui.end_child()

        imgui.same_line()

        imgui.begin_child("Text Editor", width=window_width * 0.75, height=window_height, border=True)

        if project_view.timer.test_and_set():
            # update devices
            project_view.devices = backend.get_android_devices()
            # test if framework is compiled
            if backend.is_framework_compiled():
                t = os.path.getmtime(backend.FRAMEWORK_EXE_PATH)
                t = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
                project_view.framework_compile_time = t
            else:
                project_view.framework_compile_time = None


        if project_view.framework_compile_time:
            imgui.text(f"框架编译时间: {project_view.framework_compile_time}")
        else:
            imgui.text("框架编译时间: 未编译")

        imgui.spacing()

        # drop fields
        imgui.separator()
        imgui.text(f"已连接设备：{len(self.devices)}")
        for device in self.devices:
            imgui.text(f"{IconBrands.ICON_ANDROID} {device.title}")
            imgui.same_line(spacing=10)
            # small text button
            if imgui.small_button(f"{Icons.ICON_CIRCLE_PLAY} 运行"):
                project_view.start_task(backend.install_apk_and_run(device, self.root_abspath))
        imgui.spacing()
        imgui.separator()

        imgui.columns(4, border=False)
        column_width = imgui.get_column_width()
        
        if imgui.button(f"{Icons.ICON_C} 编译框架", width=column_width):
            project_view.start_task(backend.compile_framework())
        imgui.next_column()
        if imgui.button(f"{Icons.ICON_T} 同步模板", width=column_width):
            backend.sync_project_template(self.root_abspath)
        imgui.next_column()
        if imgui.button(f"{Icons.ICON_V} 启动 VSCode", width=column_width):
            project_view.start_task(backend.start_vscode(self.selected_file_abspath, self.root_abspath))
        imgui.next_column()
        if imgui.button(f"{Icons.ICON_CIRCLE_PLAY} 运行项目", width=column_width):
            project_view.start_task(backend.run_project(self.root_abspath))
        # ------------------------- #
        imgui.next_column()
        if imgui.button(f"{IconBrands.ICON_WINDOWS} 构建 Windows", width=column_width):
            project_view.start_task(backend.build_win32(self.root_abspath))
        imgui.next_column()
        if imgui.button(f"{IconBrands.ICON_ANDROID} 构建 Android", width=column_width):
            project_view.start_task(backend.build_android(self.root_abspath))
        imgui.next_column()

        imgui.push_style_var(imgui.STYLE_ALPHA, 0.4)
        if imgui.button(f"{IconBrands.ICON_APPLE} 构建 iOS", width=column_width):
            pass
        imgui.next_column()
        if imgui.button(f"{IconBrands.ICON_CHROME} 构建 Web", width=column_width):
            pass
        imgui.pop_style_var()

        imgui.next_column()

        imgui.columns(1)

        imgui.begin_child("Console", flags=imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_BACKGROUND)
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (10, 10))
        # self.render_text_editor()
        self.render_console()
        imgui.pop_style_var()
        imgui.end_child()

        imgui.end_child()


if __name__ == "__main__":
    assert glfw.init()

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1440, 720, "CarrotLib🥕 Playground", None, None)
    if not window:
        glfw.terminate()
        exit(1)

    # Make the window's context current
    glfw.make_context_current(window)

    # Setup Dear ImGui context
    imgui.create_context()
    impl = GlfwRenderer(window)

    project_view = ProjectView()
    impl.refresh_font_texture()

    # Main loop
    while not glfw.window_should_close(window):
        project_view.poll_task()
        glfw.poll_events()

        # Start the Dear ImGui frame
        if project_view.task is None:
            impl.process_inputs()

        imgui.new_frame()

        with imgui.font(project_view.default_font):
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (0, 10))
            imgui.set_next_window_position(0, 0)
            window_size = glfw.get_window_size(window)
            imgui.set_next_window_size(window_size[0], window_size[1])
            imgui.begin("CarrotLib Playground", flags=imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_BACKGROUND)
            project_view.render()
            imgui.end()
            imgui.pop_style_var()

        gl.glClearColor(33/255, 37/255, 43/255, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    # Cleanup
    impl.shutdown()
    glfw.terminate()
