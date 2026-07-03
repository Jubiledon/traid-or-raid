# simulation/simulation_runner.py

from typing import Optional

from world.world import GridWorld

from simulation.turn_manager import run_turn
from simulation.metrics import build_episode_results
from rendering.renderer import Renderer

from config import (
    MAX_TICKS,
    RESOURCE_COUNT,
)

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class SimulationRunner:

    def __init__(
        self,
        world: GridWorld,
        brains: dict,
        headless: bool = False,
        log_path: Optional[str] = None,
    ):

        self.world = world
        self.brains = brains
        self.headless = headless
        self.log_path = log_path

        self.display = None

        if not headless and PYGAME_AVAILABLE:
            self.display = Renderer(world)

    # ---------------------------------------------------------
    # main loop
    # ---------------------------------------------------------

    def run(self) -> dict:

        running = True

        while (self._simulation_active() and running
        ):

            if self.display:
                running = self.display.handle_events()

            run_turn(
                self.world,
                self.brains,
                self.display,
            )

            if self.display:
                self.display.draw()

        self._shutdown()

        return build_episode_results(
            self.world,
            self.brains,
        )

    # ---------------------------------------------------------
    # cleanup
    # ---------------------------------------------------------

    def _shutdown(self):

        if self.display:
            self.display.quit()

        if self.log_path:
            self.world.save_log(self.log_path)

    def _simulation_active(self) -> bool:

        if self.world.tick >= MAX_TICKS:
            return False

        if self.world.resources_remaining() == 0:
            return False

        return True