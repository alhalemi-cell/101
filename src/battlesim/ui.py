import battlesim.models as m
import battlesim.constants as c
import pygame
import sys

def draw_text(text, font, screen, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_panel(screen, x, y, width, height, bg_color, border_color, border_radius=8):
    pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=border_radius)
    pygame.draw.rect(screen, border_color, (x, y, width, height), width=4, border_radius=border_radius)

def draw_hp_bar(monster: m.Monster, x: int, y: int, screen: pygame.Surface, font: pygame.font.Font):
    draw_panel(screen, x, y, 280, 100, c.UI.Colors.PANEL_BG, c.UI.Colors.PANEL_BORDER)

    # Monster name
    draw_text(f"{monster.name}", font, screen, c.UI.Colors.BLACK, x + 15, y + 8)

    # Type badge
    type_colors = {
        m.MonsterType.FIRE:  (220, 90,  40),
        m.MonsterType.WATER: (60,  130, 220),
        m.MonsterType.GRASS: (60,  180, 60),
    }
    type_color = type_colors.get(monster.monster_type, c.UI.Colors.GRAY)
    pygame.draw.rect(screen, type_color, (x + 160, y + 10, 60, 20), border_radius=4)
    small_font = pygame.font.SysFont(c.UI.Font.FONT_NAME, 14)
    draw_text(monster.monster_type.name, small_font, screen, c.UI.Colors.WHITE, x + 165, y + 12)

    # HP numbers
    draw_text(f"HP: {monster.current_health}/{monster.max_health}", small_font, screen, c.UI.Colors.BLACK, x + 15, y + 38)

    # HP bar
    ratio = monster.current_health / monster.max_health
    bar_x, bar_y = x + 15, y + 58
    hp_color = c.UI.Colors.GREEN
    if ratio <= 0.2:
        hp_color = c.UI.Colors.RED
    elif ratio <= 0.5:
        hp_color = c.UI.Colors.YELLOW

    pygame.draw.rect(screen, c.UI.Colors.GRAY, (bar_x, bar_y, c.UI.HealthBar.BAR_WIDTH, c.UI.HealthBar.BAR_HEIGHT), border_radius=4)
    if ratio > 0:
        pygame.draw.rect(screen, hp_color, (bar_x, bar_y, int(c.UI.HealthBar.BAR_WIDTH * ratio), c.UI.HealthBar.BAR_HEIGHT), border_radius=4)
    pygame.draw.rect(screen, c.UI.Colors.BLACK, (bar_x, bar_y, c.UI.HealthBar.BAR_WIDTH, c.UI.HealthBar.BAR_HEIGHT), width=2, border_radius=4)

    # Status badges
    badge_x = x + 15
    badge_y = y + 78
    if monster.is_asleep:
        pygame.draw.rect(screen, (100, 100, 220), (badge_x, badge_y, 40, 16), border_radius=3)
        draw_text("SLP", small_font, screen, c.UI.Colors.WHITE, badge_x + 4, badge_y + 1)
        badge_x += 46
    if monster.is_poisoned:
        pygame.draw.rect(screen, (160, 50, 200), (badge_x, badge_y, 40, 16), border_radius=3)
        draw_text("PSN", small_font, screen, c.UI.Colors.WHITE, badge_x + 4, badge_y + 1)
        badge_x += 46
    if monster.is_leech_seeded:
        pygame.draw.rect(screen, (40, 160, 40), (badge_x, badge_y, 40, 16), border_radius=3)
        draw_text("SED", small_font, screen, c.UI.Colors.WHITE, badge_x + 4, badge_y + 1)

def draw_battle_interface(screen, font, battle_text, current_monster):
    draw_panel(screen, 10, 460, 780, 130, c.UI.Colors.PANEL_BG, c.UI.Colors.PANEL_BORDER)

    # wrap battle text
    words = battle_text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < 300:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '

    if current_line:
        lines.append(current_line.strip())

    for i, line in enumerate(lines[:3]):
        draw_text(line, font, screen, c.UI.Colors.BLACK, 25, 475 + i * 26)

    menu_x, menu_y = 390, 460
    draw_panel(screen, menu_x, menu_y, 400, 130, c.UI.Colors.WHITE, c.UI.Colors.PANEL_BORDER)

    positions = [
        (menu_x + 20, menu_y + 25), (menu_x + 200, menu_y + 25),
        (menu_x + 20, menu_y + 75), (menu_x + 200, menu_y + 75)
    ]

    for i, move in enumerate(current_monster.moves.moves):
        draw_text(f"{i + 1}: {move.name}", font, screen, c.UI.Colors.BLACK, positions[i][0], positions[i][1])

def main_menu(screen, font):
    options = ["PLAY", "QUIT"]
    selected_index = 0

    while True:
        screen.fill((30, 30, 30))
        draw_text("POKEMON BATTLE SIM", font, screen, c.UI.Colors.WHITE, 250, 150)
        draw_text("Use UP/DOWN to navigate, ENTER to confirm", font, screen, (200, 200, 200), 160, 220)
        
        for i, option in enumerate(options):
            color = c.UI.Colors.GREEN if i == selected_index else c.UI.Colors.GRAY
            prefix = "> " if i == selected_index else "  "
            draw_text(f"{prefix}{option}", font, screen, color, 350, 300 + i * 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return True
                    else:
                        pygame.quit()
                        sys.exit()
        
        pygame.display.flip()

def monster_selection_menu(screen, font, monsters: tuple[m.Monster], title: str, player1_monsters: list[m.Monster], player2_monsters: list[m.Monster]):
    selected_index = 0

    while True:
        screen.fill((30, 30, 30)) 
        draw_text(title, font, screen, c.UI.Colors.WHITE, 200, 50)
        draw_text("Use UP/DOWN to choose, ENTER to confirm", font, screen, c.UI.Colors.GRAY, 150, 100)
        draw_text(f"Player 1 Team: {', '.join(m.name for m in player1_monsters)}", font, screen, c.UI.Colors.GREEN, 275, 150)
        draw_text(f"Player 2 Team: {', '.join(m.name for m in player2_monsters)}", font, screen, c.UI.Colors.GREEN, 275, 500)
        
        for i, monster in enumerate(monsters):
            color = c.UI.Colors.GREEN if i == selected_index else c.UI.Colors.GRAY
            prefix = "> " if i == selected_index else "  "
            draw_text(f"{prefix}{i + 1}. {monster.name}", font, screen, color, 50, 180 + i * 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(monsters)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(monsters)
                elif event.key == pygame.K_RETURN:
                    return monsters[selected_index]

        pygame.display.flip()

def switch_monster_menu(screen, font, team: list[m.Monster], current_monster: m.Monster) -> m.Monster:
    swappable = [mon for mon in team if not mon.fainted and mon != current_monster]
    if not swappable:
        return current_monster

    selected_index = 0

    while True:
        screen.fill((30, 30, 30))
        draw_text("SWITCH MONSTER  (ESC to cancel)", font, screen, c.UI.Colors.WHITE, 200, 50)
        draw_text("Use UP/DOWN to choose, ENTER to confirm", font, screen, c.UI.Colors.GRAY, 150, 100)

        for i, monster in enumerate(swappable):
            color = c.UI.Colors.GREEN if i == selected_index else c.UI.Colors.GRAY
            prefix = "> " if i == selected_index else "  "
            hp_ratio = monster.current_health / monster.max_health
            draw_text(
                f"{prefix}{monster.name}   HP: {monster.current_health}/{monster.max_health}",
                font, screen, color, 200, 200 + i * 50
            )
            # Mini HP bar
            bar_x, bar_y = 500, 205 + i * 50
            pygame.draw.rect(screen, c.UI.Colors.GRAY, (bar_x, bar_y, 150, 12), border_radius=4)
            bar_color = c.UI.Colors.GREEN if hp_ratio > 0.5 else c.UI.Colors.YELLOW if hp_ratio > 0.25 else c.UI.Colors.RED
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(150 * hp_ratio), 12), border_radius=4)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return current_monster  # cancelled, no switch
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(swappable)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(swappable)
                elif event.key == pygame.K_RETURN:
                    return swappable[selected_index]

def win_screen(screen, font, winner: str) -> bool:
    """Returns True if player wants to play again, False to quit."""
    options = ["PLAY AGAIN", "QUIT"]
    selected_index = 0

    while True:
        screen.fill((30, 30, 30))
        draw_text(f"{winner} WINS!", font, screen, c.UI.Colors.GREEN, 300, 150)
        draw_text("Use UP/DOWN to choose, ENTER to confirm", font, screen, c.UI.Colors.GRAY, 150, 220)

        for i, option in enumerate(options):
            color = c.UI.Colors.GREEN if i == selected_index else c.UI.Colors.GRAY
            prefix = "> " if i == selected_index else "  "
            draw_text(f"{prefix}{option}", font, screen, color, 330, 320 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_index == 0  # True = play again, False = quit
