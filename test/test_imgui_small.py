# Smaller test than test_imgui.py, note '# type: ignore' is for pylint
import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer


class TestImguiSmall:
    def __init__(self):
        self.console_message = "Hello World!"

    def main(self):
        imgui.create_context()  # type: ignore
        window = self.impl_glfw_init()

        impl = GlfwRenderer(window)

        io = imgui.get_io()

        while not glfw.window_should_close(window):
            self.render_frame(impl, window)

        impl.shutdown()
        glfw.terminate()

    def frame_commands(self):
        io = imgui.get_io()  # type: ignore

        # ctrl+q to quit
        if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
            sys.exit(0)

        # Main bar with quit button
        with imgui.begin_main_menu_bar() as main_menu_bar:  # type: ignore
            if main_menu_bar.opened:
                with imgui.begin_menu("File", True) as file_menu:  # type: ignore
                    if file_menu.opened:
                        clicked_quit, selected_quit = imgui.menu_item(  # type: ignore
                            "Quit", "Ctrl+Q"
                        )
                        if clicked_quit:
                            sys.exit(0)

        # Console window
        with imgui.begin("Console Messages") as console:
            if console.opened:
                with imgui.begin_menu("Clear", True) as clear_console:
                    if clear_console.opened:
                        clicked_clear, selected_clear = imgui.menu_item(
                            "Clear"
                        )
                        if clicked_clear:
                            self.console_message = ""
            # Add to console message with button press
            with imgui.begin_child("Console Region", -1, 150, border=True):
                imgui.text(self.console_message)
                imgui.set_scroll_y(imgui.get_scroll_max_y())
            imgui.button("Add to console message")
            if imgui.is_item_hovered():
                with imgui.begin_tooltip():
                    imgui.text("Add 'Hello World!' to console message")
            if imgui.is_item_clicked():
                self.console_message += "\n" + "Hello World!"
            imgui.show_metrics_window()

    def render_frame(self, impl, window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()  # type: ignore

        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.frame_commands()

        imgui.render()  # type: ignore
        impl.render(imgui.get_draw_data())  # type: ignore
        glfw.swap_buffers(window)

    def impl_glfw_init(self):
        width, height = 1600, 900
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        window = glfw.create_window(
            int(width), int(height), window_name, None, None
        )
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        return window


if __name__ == "__main__":
    TestImguiSmall().main()
