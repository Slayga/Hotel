from requests import head


# Smaller test than test_imgui.py
import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer


def main():
    imgui.create_context()  # type: ignore
