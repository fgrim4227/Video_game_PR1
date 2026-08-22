"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of render_table, the rendering
shared by every state of the game (the mid line, both paddles, the
ball, and the score), since only the message overlaid on top of it
differs from one state to the next.
"""

import pygame

from gale.text import render_text

import settings


def render_table(surface: pygame.Surface, pong) -> None:
    pygame.draw.rect(
        surface,
        settings.COLOR_WHITE,
        pygame.Rect(
            round(settings.VIRTUAL_WIDTH / 2 - settings.MID_LINE_WIDTH / 2),
            0,
            settings.MID_LINE_WIDTH,
            settings.VIRTUAL_HEIGHT,
        ),
    )

    pong.player1.render(surface)
    pong.player2.render(surface)
    pong.ball.render(surface)

    render_text(
        surface,
        str(pong.player1_score),
        settings.FONTS["score"],
        settings.VIRTUAL_WIDTH / 2 - 50,
        settings.VIRTUAL_HEIGHT / 6,
        settings.COLOR_WHITE,
        center=True,
    )
    render_text(
        surface,
        str(pong.player2_score),
        settings.FONTS["score"],
        settings.VIRTUAL_WIDTH / 2 + 50,
        settings.VIRTUAL_HEIGHT / 6,
        settings.COLOR_WHITE,
        center=True,
    )
