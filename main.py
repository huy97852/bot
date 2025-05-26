import time
import random
from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player


def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Press any key.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device

def solve_rune(g, p, target):
    while True:
        print("Pathing towards rune...")
        p.go_to(target)
        time.sleep(1)
        p.press("ALT")
        time.sleep(1)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            p.hold("LEFT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("LEFT")

            p.hold("RIGHT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("RIGHT")

            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                break
            else:
                print("Trying again...")


if __name__ == "__main__":
    c = interception()
    d = bind(c)

    g = Game((5, 60, 180, 130))
    p = Player(c, d, g)
    target = (97, 32.5)

    while True:
        # other_location = g.get_other_location()
        # if other_location > 0:
        #     print("A player has entered your map.")

        rune_location = g.get_rune_location()
        # if rune_location is not None:
        #     print("A rune has appeared.")
        #     solve_rune(g, p, rune_location)

        print("Running...")
        p.hold("X")
        time.sleep(10)
        p.release_all()
        p.press("LEFT")
        time.sleep(0.1)
        p.hold("X")
        time.sleep(10)
        p.press("RIGHT")