# rendering/ui_panel.py

import pygame

from rendering.colours import (
    COL_PANEL,
    COL_TEXT,
    COL_PANEL_HEADER,
    COL_MESSAGE,
    COL_AGENT,
)

from config import (
    GRID_SIZE,
    CELL_PX,
    WINDOW_W,
    WINDOW_H,
    MAX_TICKS,
)


class UIPanel:

    def __init__(
        self,
        screen,
        font_sm,
        font_md,
    ):
        self.screen = screen
        self.font_sm = font_sm
        self.font_md = font_md

    def draw(
        self,
        world,
        message_log,
    ):

        panel_x = GRID_SIZE * CELL_PX + 5

        pygame.draw.rect(
            self.screen,
            COL_PANEL,
            (panel_x, 0, WINDOW_W - panel_x, WINDOW_H),
        )

        y_offset = 10

        # ── tick header ─────────────────────────────────────────

        header = self.font_md.render(
            f"Tick {world.tick}/{MAX_TICKS}",
            True,
            COL_TEXT,
        )

        self.screen.blit(header, (panel_x + 8, y_offset))

        y_offset += 22

        # ── efficiency ──────────────────────────────────────────

        efficiency = world.collective_efficiency()

        eff_text = self.font_sm.render(
            f"Efficiency: {efficiency:.2%}",
            True,
            COL_TEXT,
        )

        self.screen.blit(eff_text, (panel_x + 8, y_offset))

        y_offset += 28

        # ── agent stats ─────────────────────────────────────────

        for agent in world.agents:

            colour = COL_AGENT.get(
                agent.personality,
                (180, 180, 180),
            )

            pygame.draw.rect(
                self.screen,
                colour,
                (panel_x + 8, y_offset, 10, 10),
            )

            info = self.font_sm.render(
                f"{agent.agent_id}: {agent.inventory} ({agent.personality[:4]})",
                True,
                COL_TEXT,
            )

            self.screen.blit(info, (panel_x + 22, y_offset))

            y_offset += 16

        # ── message log ─────────────────────────────────────────

        y_offset += 10

        msg_header = self.font_sm.render(
            "── messages ──",
            True,
            COL_PANEL_HEADER,
        )

        self.screen.blit(msg_header, (panel_x + 8, y_offset))

        y_offset += 16

        for line in message_log[-12:]:

            rendered = self.font_sm.render(
                line[:34],
                True,
                COL_MESSAGE,
            )

            self.screen.blit(rendered, (panel_x + 8, y_offset))

            y_offset += 14