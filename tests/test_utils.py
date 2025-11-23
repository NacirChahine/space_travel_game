import pygame
from src.utils.helpers import split_text

def test_split_text():
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)
    text = "This is a long text that should be split into multiple lines."
    # We don't know the exact width in pixels, but we can test that it returns a list
    lines = split_text(text, font, 100)
    assert isinstance(lines, list)
    assert len(lines) > 1
