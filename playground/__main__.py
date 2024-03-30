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

class ProjectView:
    def __init__(self):
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
            20,
            font_config=imgui.FontConfig(oversample_h=2, oversample_v=2),
            glyph_ranges=glyph_ranges
        )

        imgui.get_io().delta_time = 1.0 / 60.0

        self.root = "projects/magicpd"
        self.selected_file = f"{self.root}/main.py"


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
                    self.selected_file = item_path

    def render_text_editor(self):
        input_bg_color = (44/255, 40/255, 52/255, 1.0)
        input_fg_color = (171/255, 178/255, 191/255, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *input_bg_color)
        imgui.push_style_color(imgui.COLOR_TEXT, *input_fg_color)
        if not os.path.exists(self.selected_file):
            self.selected_file = None
        if self.selected_file:
            flags = 0
            try:
                with open(self.selected_file, "rt") as f:
                    buffer = f.read()
            except:
                buffer = "[不支持的文件类型]"
                flags |= imgui.INPUT_TEXT_READ_ONLY
            width, height = imgui.get_window_size()
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

        # two column with splitter, drag to resize width
        imgui.begin_child("File Hierarchy", width=window_width * 0.3, height=window_height)

        full_width = imgui.get_window_width()
        if imgui.button(f"{Icons.ICON_FOLDER} 新建项目", width=full_width):
            backend.new_project("new_project")
            self.root = "projects/new_project"
            self.selected_file = f"{self.root}/main.py"
        if imgui.button(f"{Icons.ICON_FOLDER_OPEN} 打开项目", width=full_width):
            backend.run_project(os.path.abspath(self.root))
        if imgui.button(f"{Icons.ICON_CODE} 启动 VSCode", width=full_width):
            if sys.platform == "win32":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Applications\\code.exe\\shell\\open\\command")
                code_path = winreg.QueryValue(key, None)
                backend.cmd([code_path.replace("%1", os.path.abspath(self.root))])
            else:
                raise NotImplementedError

        imgui.spacing()

        self.render_file_hierarchy(self.root)
        imgui.end_child()

        imgui.same_line()

        imgui.begin_child("Text Editor", width=window_width * 0.7, height=window_height, border=True)

        if backend.is_framework_compiled():
            framework_compile_time = os.path.getmtime(backend.FRAMEWORK_EXE_PATH)
            framework_compile_time = datetime.fromtimestamp(framework_compile_time).strftime("%Y-%m-%d %H:%M:%S")
            imgui.text(f"框架编译时间: {framework_compile_time}")
        else:
            imgui.text("框架编译时间: 未编译")

        imgui.separator()
        imgui.columns(4, border=False)
        column_width = imgui.get_column_width()
        
        if imgui.button(f"{Icons.ICON_C} 编译框架", width=column_width):
            backend.compile_framework()
        imgui.next_column()
        if imgui.button(f"{Icons.ICON_CIRCLE_PLAY} 运行项目", width=column_width):
            backend.run_project(os.path.abspath(self.root))
        imgui.next_column()
        if imgui.button(f"{Icons.ICON_CIRCLE_PLAY} 运行 Android", width=column_width):
            backend.run_project(os.path.abspath(self.root))
        imgui.next_column()
        # ...
        imgui.next_column()

        imgui.columns(1)
        imgui.columns(4, border=False)

        if imgui.button(f"{IconBrands.ICON_WINDOWS} 构建 Windows", width=column_width):
            pass
        imgui.next_column()
        if imgui.button(f"{IconBrands.ICON_ANDROID} 构建 Android", width=column_width):
            backend.build_android(os.path.abspath(self.root))
        imgui.next_column()

        if sys.platform != "darwin":
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.4)
            if imgui.button(f"{IconBrands.ICON_APPLE} 构建 iOS", width=column_width):
                pass
            imgui.pop_style_var()
        else:
            if imgui.button(f"{IconBrands.ICON_APPLE} 构建 iOS", width=column_width):
                pass
        imgui.next_column()
        if imgui.button(f"{IconBrands.ICON_CHROME} 构建 Web", width=column_width):
            pass
        imgui.next_column()

        imgui.columns(1)

        with imgui.font(self.source_font):
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (10, 10))
            self.render_text_editor()
            imgui.pop_style_var()
        imgui.end_child()


if __name__ == "__main__":
    assert glfw.init()

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 720, "CarrotLib🥕 Playground", None, None)
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
        glfw.poll_events()

        # Start the Dear ImGui frame
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
