import pygame
import random
import sys

from database import load_top_scores
from utils import split_text
from game_assets import draw_button


# Welcome Screen with Naro Chan Logo and Random Fact
def show_welcome_screen(assets):
    screen = pygame.display.set_mode((assets['SCREEN_WIDTH'], assets['SCREEN_HEIGHT']))
    clock = pygame.time.Clock()

    # Choose a random fact
    space_facts = [
        "The Milky Way galaxy contains over 100 billion stars.",
        "The Andromeda Galaxy is the closest large galaxy to ours.",
        "The Hubble Space Telescope has been orbiting Earth since 1990.",
        "The International Space Station is the size of a football field.",
        "The Moon is slowly moving away from Earth.",
        "Mars is often called the Red Planet.",
        "Jupiter has the Great Red Spot, a giant storm that has been raging for centuries.",
        "Saturn is known for its beautiful rings, made of ice and rock.",
        "Pluto was reclassified as a dwarf planet in 2006.",
        "The Voyager 1 spacecraft is the farthest human-made object from Earth.",
        "Black holes are regions of space where gravity is so strong that nothing can escape.",
        "Comets are made of ice, dust, and rock.",
        "Asteroids are rocky objects in space.",
        "The universe is billions of years old.",
        "The Big Bang theory explains the origin of the universe.",
        "There may be life on other planets in the universe.",
        "Space suits protect astronauts from the harsh conditions of space.",
        "The first artificial satellite was Sputnik 1, launched in 1957.",
        "The Apollo 11 mission was the first to land humans on the Moon.",
        "The International Space Station is a joint project of many countries.",
        "Space is completely silent.",
        "The hottest planet in our solar system is Venus.",
        "A full NASA space suit costs $12 million.",
        "Neutron stars can spin 600 times per second.",
        "One day on Venus is longer than one year on Earth.",
        "There are more stars in the universe than grains of sand on Earth.",
        "The Sun accounts for 99.86% of the mass in the Solar System.",
        "There could be 500 million planets capable of supporting life in our galaxy.",
        "The Earth is a tiny speck in the vastness of space.",
        "The Milky Way galaxy is about 100,000 light-years across.",
        "Black holes are regions of space where gravity is so strong that nothing can escape.",
        "The International Space Station orbits Earth at a speed of about 17,500 miles per hour.",
        "The Apollo 11 mission was the first to land humans on the Moon.",
        "The Sun is about 4.6 billion years old.",
        "The Moon is about 4.5 billion years old.",
        "The Sun's surface temperature is about 5,500 degrees Celsius.",
        "The Sun's core temperature is about 15 million degrees Celsius."
    ]
    random_fact = random.choice(space_facts)

    # Text wrapping for fact
    font = pygame.font.SysFont(None, 30)
    wrapped_fact_lines = split_text(random_fact, font, 760)

    # To manage the blinking effect of "Press ENTER"
    blink = True
    blink_timer = pygame.time.get_ticks()

    while True:
        screen.fill(assets['BLACK'])  # Black background

        # Show logo
        screen.blit(assets['logo_img'], (assets['SCREEN_WIDTH'] // 2 - assets['logo_img'].get_width() // 3, 110))

        # Show fact text
        for i, line in enumerate(wrapped_fact_lines):
            fact_text = font.render(line, True, assets['YELLOW'])
            fact_text_x = assets['SCREEN_WIDTH'] // 2 - fact_text.get_width() // 2  # Center horizontally
            screen.blit(fact_text, (fact_text_x, 500 + i * 30))

        # Show title text
        title_font = pygame.font.SysFont(None, 50)
        title_text = title_font.render("Welcome to Spaceship Game!", True, (255, 255, 255))  # White title
        title_text_x = assets['SCREEN_WIDTH'] // 2 - title_text.get_width() // 2  # Center horizontally
        screen.blit(title_text, (title_text_x, 50))

        # Blinking "Press ENTER" text
        if blink:
            enter_text = title_font.render("Press ENTER to Start", True, assets['RED'])
            enter_text_x = assets['SCREEN_WIDTH'] // 2 - enter_text.get_width() // 2
            screen.blit(enter_text, (enter_text_x, 440))

        # Manage the blinking effect every 500ms
        if pygame.time.get_ticks() - blink_timer > 500:
            blink = not blink
            blink_timer = pygame.time.get_ticks()

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Exit the splash screen to start the game

        pygame.display.update()
        clock.tick(30)


# To save top scored player initials
def get_player_initials(assets):
    screen = pygame.display.set_mode((assets['SCREEN_WIDTH'], assets['SCREEN_HEIGHT']))
    font = pygame.font.SysFont(None, 55)
    instructions_font = pygame.font.SysFont(None, 35)
    initials = ""

    while True:
        screen.fill(assets['BLACK'])

        # Display instructions
        instruction_text = font.render("Enter Your Initials:", True, assets['WHITE'])
        instruction_text_x = assets['SCREEN_WIDTH'] // 2 - instruction_text.get_width() // 2
        screen.blit(instruction_text, (instruction_text_x, 100))

        # Display initials input
        initials_text = font.render(initials, True, assets['WHITE'])
        initials_text_x = assets['SCREEN_WIDTH'] // 2 - initials_text.get_width() // 2
        screen.blit(initials_text, (initials_text_x, 200))

        # Display "Press Enter to Submit" and validation
        if len(initials) == 3:
            submit_text = instructions_font.render("Press Enter to Submit", True, assets['WHITE'])
        else:
            submit_text = instructions_font.render("Enter 3 Letters", True, assets['WHITE'])

        submit_text_x = assets['SCREEN_WIDTH'] // 2 - submit_text.get_width() // 2
        screen.blit(submit_text, (submit_text_x, 300))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    return initials  # Return initials when enter is pressed and 3 characters are typed
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]  # Remove the last character
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()  # Add uppercase letters only

        pygame.display.update()
        pygame.time.delay(100)


# End Screen with top 5 scores and "Replay" button
def show_end_screen(score, assets):
    screen = pygame.display.set_mode((assets['SCREEN_WIDTH'], assets['SCREEN_HEIGHT']))
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 40)  # Smaller font for top 5 scores

    # Load the top 5 scores from the database (returns empty list if unavailable)
    top_scores = load_top_scores()  # we get top updated scores

    while True:
        screen.fill(assets['BLACK'])

        # Game over text
        title_text = font.render("Game Over!", True, assets['RED'])
        title_text_x = assets['SCREEN_WIDTH'] // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_text_x, 50))

        # Display player's score
        score_text = font.render(f"Your Score: {score}", True, assets['WHITE'])
        score_text_x = assets['SCREEN_WIDTH'] // 2 - score_text.get_width() // 2
        screen.blit(score_text, (score_text_x, 150))

        # Display top 5 scores
        top_scores_title = small_font.render("Top 5 High Scores", True, assets['YELLOW'])
        top_scores_title_x = assets['SCREEN_WIDTH'] // 2 - top_scores_title.get_width() // 2
        screen.blit(top_scores_title, (top_scores_title_x, 250))

        # Check if scores are available
        if len(top_scores) > 0:
            # Iterate through the top 5 scores and display them
            for i, entry in enumerate(top_scores):
                initials = entry.get('initials', 'N/A')
                high_score = entry.get('high_score', 0)
                score_text = small_font.render(f"{i+1}. {initials} - {high_score}", True, assets['WHITE'])
                score_text_x = assets['SCREEN_WIDTH'] // 2 - score_text.get_width() // 2
                screen.blit(score_text, (score_text_x, 300 + i * 40))  # Space the scores vertically
        else:
            # Display message when database is unavailable
            unavailable_font = pygame.font.SysFont(None, 35)
            unavailable_text = unavailable_font.render("Leaderboard unavailable", True, assets['WHITE'])
            unavailable_text_x = assets['SCREEN_WIDTH'] // 2 - unavailable_text.get_width() // 2
            screen.blit(unavailable_text, (unavailable_text_x, 320))

        # Draw replay and exit buttons
        replay_button = draw_button(screen, "Replay", assets['SCREEN_WIDTH'] // 2 - 100, 520, 200, 50, font_size=40, idle_color=(80, 80, 200), hover_color=(100, 100, 250))

        # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return "replay"

        pygame.display.update()
        pygame.time.delay(100)
