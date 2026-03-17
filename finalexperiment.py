import csv
trials = []

import sys, pygame, random
participant_id = input("Enter participant ID: ")
pygame.init()
font = pygame.font.SysFont(None, 36) #extra: to create the text for 'Trial:#'

#--NOTES--
#extra = additional code not in the 'Posner Cuing Task' code - came from searching online
#edit: using the code from the 'Posner Cuing Task' but altering it to fit the experiment

# Window setup
mywindow = pygame.display.set_mode([800,600])
clock = pygame.time.Clock()

#extra: WELCOME SCREEN
waiting = True

while waiting:
    mywindow.fill((255,255,255))

    welcome_text = font.render("Welcome! Please press any key to continue.", True, (0,0,0))
    #extra: to center the text on the screen
    text_rect = welcome_text.get_rect(center=(mywindow.get_width()//2, mywindow.get_height()//2))
    mywindow.blit(welcome_text, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            waiting = False

#extra: INSTRUCTION SCREEN
waiting = True

while waiting:
    mywindow.fill((255,255,255))

    #extra: to create all the instruction lines
    instructions = [
        ("Instructions:", (0,0,0)),
        ("Press 'X' if the blue line is longer.", (0,0,255)),
        ("Press 'Y' if the red line is longer.", (255,0,0)),
        ("Press the spacebar if the lines are equal.", (0,0,0)),
        ("Whenever you are ready, press any key to start.", (0,0,0))   
    ]

    #extra: this draws each line of text, spaces it vertically, and centers it horizontally
    for i, (line, color) in enumerate(instructions):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(mywindow.get_width()//2, 200 + i*50))
        mywindow.blit(text_surface, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            waiting = False

# Experiment parameters
X_length = 400
y_values = [355,370,385,400,415,430,445]
Y_list = y_values * 10 #extra: this repeats each value 10 times
random.shuffle(Y_list) #extra: this randomizes the order
n_trials = len(Y_list)

# Run trials
for trial_num in range(n_trials):

    #edit: Generate random Y length
    Y_length = Y_list[trial_num]

    #edit: Random positions
    x1 = random.randint(50,350)
    y1 = random.randint(100,500)

    x2 = random.randint(450,700)
    y2 = random.randint(100,500)

    response_made = False
    running_trial = True

    while running_trial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not response_made:

                if event.key == pygame.K_x:
                    response = "X"

                elif event.key == pygame.K_y:
                    response = "Y"

                elif event.key == pygame.K_SPACE:
                    response = "Equal"

                else:
                    continue

                response_made = True
                print(f"Trial {trial_num+1}: Y length = {Y_length}, Response = {response}")

                trial = {
                     "participant_id": participant_id,
                     "trial_number": trial_num + 1,
                     "y_length": Y_length,
                     "response": response
                }

                trials.append(trial)

                pygame.time.wait(800)
                running_trial = False

        # Background
        mywindow.fill((255,255,255)) #edit: changed from grey background to white

        trial_text = font.render(f"Trial {trial_num + 1} of {n_trials}", True, (0,0,0))
        mywindow.blit(trial_text, (20,20)) #extra: adding Trials on the screen

        # Draw line X (blue)
        pygame.draw.line(
            mywindow,
            (0,0,255),
            (x1,y1),
            (x1 + X_length, y1),
            5
        )

        # Draw line Y (red)
        pygame.draw.line(
            mywindow,
            (255,0,0),
            (x2,y2),
            (x2 + Y_length, y2),
            5
        )

        pygame.display.flip()
        clock.tick(60)

print("Experiment complete!")

fieldnames = ["participant_id","trial_number", "y_length", "response"]

with open("experiment_data.csv", "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerows(trials)

pygame.quit()
sys.exit()