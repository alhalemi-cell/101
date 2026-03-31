import battlesim.models as m
import battlesim.constants as c
import battlesim.ui as ui
import battlesim.sprite as s 
import pygame
import os          
import random
import sys 

TEAM_SIZE = 3

def draft_teams(screen: pygame.Surface, font: pygame.font.Font) -> tuple[list[m.Monster], list[m.Monster]]:
    available_monsters: list[m.Monster] = list(c.Monsters.MONSTERS_LIST)
    player_one_team: list[m.Monster] = []
    player_two_team: list[m.Monster] = []

    for pick_number in range(TEAM_SIZE):
        player_one_pick = ui.monster_selection_menu(
            screen,
            font,
            tuple(available_monsters),
            f"PLAYER 1 PICK {pick_number + 1}/{TEAM_SIZE}",
            player_one_team,
            player_two_team,
        )
        player_one_team.append(player_one_pick)
        available_monsters.remove(player_one_pick)

        player_two_pick = ui.monster_selection_menu(
            screen,
            font,
            tuple(available_monsters),
            f"PLAYER 2 PICK {pick_number + 1}/{TEAM_SIZE}",
            player_one_team,
            player_two_team,
        )
        player_two_team.append(player_two_pick)
        available_monsters.remove(player_two_pick)

    return player_one_team, player_two_team

def main() -> None:
    _ = pygame.init()
    pygame.mixer.init() 

    screen: pygame.Surface = pygame.display.set_mode((c.Config.Pygame.SCREEN_WIDTH, c.Config.Pygame.SCREEN_HEIGHT))
    font: pygame.font.Font = pygame.font.SysFont(c.UI.Font.FONT_NAME, c.UI.Font.FONT_SIZE)
    pygame.display.set_caption("Pokemon Battle Sim")

    try:
        hit_sound = pygame.mixer.Sound(os.path.join(c.Assets.SOUND_DIR, c.Assets.HIT_SOUND))
        faint_sound = pygame.mixer.Sound(os.path.join(c.Assets.SOUND_DIR, c.Assets.FAINT_SOUND))
    except (FileNotFoundError, pygame.error):
        hit_sound = None
        faint_sound = None

    if ui.main_menu(screen, font):
        player_one_team, player_two_team = draft_teams(screen, font)
        for monster in player_one_team + player_two_team:
            monster.reset()
        fielded_monsters: list[m.Monster] = [player_one_team[0], player_two_team[0]]
        
        running: bool = True
        game_over: bool = False
        clock = pygame.time.Clock()
        current_turn: int = 0
        battle_text: str = "Choose an attack!"
        
        p1_shake_timer = 0
        p2_shake_timer = 0

        while running:
            _ = clock.tick(60)
            
            screen.fill(c.UI.Colors.BG_SKY)
            pygame.draw.rect(screen, c.UI.Colors.BG_GROUND, (0, 300, c.Config.Pygame.SCREEN_WIDTH, 300))

            active_player_monster = fielded_monsters[current_turn % 2]
            active_enemy_monster = fielded_monsters[(current_turn + 1) % 2]

            p1_offset = random.choice([-5, 5]) if p1_shake_timer > 0 else 0
            p2_offset = random.choice([-5, 5]) if p2_shake_timer > 0 else 0
            if p1_shake_timer > 0: p1_shake_timer -= 1
            if p2_shake_timer > 0: p2_shake_timer -= 1

            bob = int(5 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 5).y)
            s.StaticMonsterSprite(fielded_monsters[0].name, s.SpriteOrientation.REAR_FACING, 150 + p1_offset, 290 + bob).draw(screen)
            s.StaticMonsterSprite(fielded_monsters[1].name, s.SpriteOrientation.FRONT_FACING, 500 + p2_offset, 120 - bob).draw(screen)

            ui.draw_hp_bar(fielded_monsters[1], 50, 50, screen, font)    
            ui.draw_hp_bar(fielded_monsters[0], 480, 320, screen, font)  
            ui.draw_battle_interface(screen, font, battle_text, active_player_monster)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if not game_over and event.type == pygame.KEYDOWN:
                    turn_completed = False
                    
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        move_idx = event.key - pygame.K_1
                        move = active_player_monster.moves.GetMove(move_idx)
                        battle_text = active_player_monster.attack(move, active_enemy_monster, c.TypeRelations.GetEffectiveMultiplier)
                        
                        if hit_sound: hit_sound.play()
                        
                        if current_turn % 2 == 0: p2_shake_timer = 15
                        else: p1_shake_timer = 15
                        
                        turn_completed = True

                    elif event.key == pygame.K_s:
                        active_team = player_one_team if current_turn % 2 == 0 else player_two_team
                        chosen = ui.switch_monster_menu(screen, font, active_team, active_player_monster, (current_turn % 2) + 1)
                        if chosen != active_player_monster:
                            fielded_monsters[current_turn % 2] = chosen
                            battle_text = f"Player {(current_turn % 2) + 1} switched to {chosen.name}!"
                            turn_completed = True
                        else:
                            battle_text = "Switch cancelled."
                    if turn_completed:
                        current_turn += 1
                        # Re-read active monster AFTER potential switch
                        current_active = fielded_monsters[(current_turn - 1) % 2]
                        current_enemy = fielded_monsters[current_turn % 2]
                        current_active.end_of_turn(current_enemy)
                        
                        if fielded_monsters[0].fainted:
                            if faint_sound: faint_sound.play()
                        if fielded_monsters[1].fainted:
                            if faint_sound: 
                                faint_sound.play()
            if not game_over:
                for i in range(2):
                    if fielded_monsters[i].fainted:
                        team = player_one_team if i == 0 else player_two_team
                        alive_monsters = [m for m in team if not m.fainted]
                        if alive_monsters:
                            fielded_monsters[i] = alive_monsters[0]
                            battle_text += f" Player {i+1} sent out {fielded_monsters[i].name}!"
                        else:
                            winner = f"PLAYER {2 if i == 0 else 1}"
                            game_over = True
                            play_again = ui.win_screen(screen, font, winner)
                            if play_again:
                                running = False
                                return main()
                            running = False

    pygame.quit()

def get_keyboard_input(valid: set[str]) -> str:
    while True:
        user_input = input("> ").lower()
        if user_input in valid:
            return user_input
        print(f"Invalid input. Choose: {', '.join(valid)}")

if __name__ == "__main__":
    main()
