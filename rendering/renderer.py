# rendering/renderer.py

import pygame

from rendering.colours import (
    COL_BG,
    COL_GRID,
    COL_RESOURCE,
    COL_AGENT,
    COL_TEXT,
)

from rendering.ui_panel import UIPanel

from config import (
    GRID_SIZE,
    CELL_PX,
    WINDOW_W,
    WINDOW_H,
)


class Renderer:

    def __init__(self, world):

        pygame.init()

        self.world = world

        self.screen = pygame.display.set_mode(
            (WINDOW_W, WINDOW_H)
        )

        pygame.display.set_caption("Trade or Raid")

        self.font_sm = pygame.font.SysFont(
            "monospace",
            11,
        )

        self.font_md = pygame.font.SysFont(
            "monospace",
            13,
        )

        self.clock = pygame.time.Clock()

        self.message_log = []

        self.ui_panel = UIPanel(
            self.screen,
            self.font_sm,
            self.font_md,
        )

    # ---------------------------------------------------------
    # event handling
    # ---------------------------------------------------------

    def handle_events(self) -> bool:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                return False

        return True

    # ---------------------------------------------------------
    # draw frame
    # ---------------------------------------------------------

    def draw(self):

        self.screen.fill(COL_BG)

        self._draw_grid()

        self._draw_resources()

        self._draw_agents()

        self.ui_panel.draw(
            self.world,
            self.message_log,
        )

        pygame.display.flip()

        self.clock.tick(8)

    # ---------------------------------------------------------
    # grid
    # ---------------------------------------------------------

    def _draw_grid(self):

        for x in range(GRID_SIZE + 1):

            pygame.draw.line(
                self.screen,
                COL_GRID,
                (x * CELL_PX, 0),
                (x * CELL_PX, WINDOW_H),
            )

        for y in range(GRID_SIZE + 1):

            pygame.draw.line(
                self.screen,
                COL_GRID,
                (0, y * CELL_PX),
                (GRID_SIZE * CELL_PX, y * CELL_PX),
            )

    # ---------------------------------------------------------
    # resources
    # ---------------------------------------------------------

    def _draw_resources(self):

        for x in range(GRID_SIZE):

            for y in range(GRID_SIZE):

                if self.world.resources[x, y] == 1:

                    cx = x * CELL_PX + CELL_PX // 2
                    cy = y * CELL_PX + CELL_PX // 2

                    pygame.draw.circle(
                        self.screen,
                        COL_RESOURCE,
                        (cx, cy),
                        8,
                    )

    # ---------------------------------------------------------
    # agents
    # ---------------------------------------------------------

    def _draw_agents(self):

        for agent in self.world.agents:

            cx = agent.x * CELL_PX + CELL_PX // 2
            cy = agent.y * CELL_PX + CELL_PX // 2

            colour = COL_AGENT.get(
                agent.personality,
                (180, 180, 180),
            )

            # body

            pygame.draw.circle(
                self.screen,
                colour,
                (cx, cy),
                18,
            )

            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (cx, cy),
                18,
                2,
            )

            # id label

            label = self.font_sm.render(
                agent.agent_id[-4:],
                True,
                (20, 20, 20),
            )

            self.screen.blit(
                label,
                (
                    cx - label.get_width() // 2,
                    cy - label.get_height() // 2,
                ),
            )

            # inventory

            badge = self.font_sm.render(
                str(agent.inventory),
                True,
                COL_TEXT,
            )

            self.screen.blit(
                badge,
                (cx + 14, cy - 22),
            )

            # speech bubble

            if agent.last_message:

                msg = agent.last_message[:30]

                if len(agent.last_message) > 30:
                    msg += "…"

                bubble = self.font_sm.render(
                    f'"{msg}"',
                    True,
                    (230, 230, 150),
                )

                self.screen.blit(
                    bubble,
                    (
                        max(0, cx - 40),
                        max(0, cy - 38),
                    ),
                )

    # ---------------------------------------------------------
    # messages
    # ---------------------------------------------------------

    def push_message(
        self,
        agent_id: str,
        msg: str,
    ):

        self.message_log.append(
            f"{agent_id}: {msg[:28]}"
        )

        if len(self.message_log) > 40:
            self.message_log.pop(0)

    # ---------------------------------------------------------
    # shutdown
    # ---------------------------------------------------------

    def quit(self):

        pygame.quit()