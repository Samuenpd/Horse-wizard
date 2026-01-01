import pygame


class Renderer:
    def __init__(self, screen, map_game, entities):
        self.screen = screen
        self.map_game = map_game
        self.entities = entities

    def render(self):
        self.screen.fill((0, 0, 0))

        self.map_game.draw(self.screen)

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.flip()
