"""
DRAGON'S SHADOW - A Terminal Text Adventure
Save the princess from the dragon... if you dare.

Built with OOP: Character (base) -> Hero / Villain -> Goblin, Dragon
"""

import random
import time
import sys


def slow_print(text, delay=0.015):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def pause(seconds=0.8):
    time.sleep(seconds)


def get_choice(prompt, valid_options):
    """Loops until the user enters one of the valid option keys."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"  Invalid choice. Please enter one of: {', '.join(valid_options)}")


# ----------------------------------------------------------------------
#  WEAPON
# ----------------------------------------------------------------------

class Weapon:
    def __init__(self, name, attack_bonus, defense_bonus=0, speed_bonus=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.speed_bonus = speed_bonus


# ----------------------------------------------------------------------
#  BASE CHARACTER CLASS
# ----------------------------------------------------------------------

class Character:
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_speed = speed
        self.weapon = None

    @property
    def attack_power(self):
        bonus = self.weapon.attack_bonus if self.weapon else 0
        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = self.weapon.defense_bonus if self.weapon else 0
        return self.base_defense + bonus

    @property
    def speed(self):
        bonus = self.weapon.speed_bonus if self.weapon else 0
        return self.base_speed + bonus

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg - self.defense)  # always at least 1 dmg gets through
        self.hp = max(0, self.hp - actual)
        return actual

    def show_stats(self):
        bar_len = 20
        filled = int(bar_len * self.hp / self.max_hp)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  {self.name:<10} [{bar}] {self.hp}/{self.max_hp} HP  "
              f"| ATK {self.attack_power}  DEF {self.defense}  SPD {self.speed}")


# ----------------------------------------------------------------------
#  HERO CLASS
# ----------------------------------------------------------------------

class Hero(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=7, defense=2, speed=5)
        self.stamina = 25          # too low for the forest at the start
        self.has_sword = False

    def equip(self, weapon):
        self.weapon = weapon
        self.has_sword = True
        self.base_attack += 5
        self.base_defense += 2
        self.base_speed += 1
        self.stamina += 40
        print()
        slow_print(f"  ⚔  You picked up the {weapon.name}!")
        slow_print("  Your body surges with new strength and confidence.")
        self.show_stats()

    def get_moves(self):
        """Returns dict: key -> (display_name, dmg_multiplier, hit_chance, kind)"""
        if not self.has_sword:
            return {
                "1": ("Punch", 1.0, 0.90, "attack"),
                "2": ("Kick", 1.3, 0.75, "attack"),
            }
        else:
            return {
                "1": ("Light Attack", 1.0, 0.95, "attack"),
                "2": ("Heavy Attack", 1.7, 0.70, "attack"),
                "3": ("Deflect", 0.0, 1.00, "deflect"),
                "4": ("Parry", 0.0, 1.00, "parry"),
            }


# ----------------------------------------------------------------------
#  VILLAIN CLASSES
# ----------------------------------------------------------------------

class Villain(Character):
    def __init__(self, name, hp, attack, defense, speed):
        super().__init__(name, hp, attack, defense, speed)


class Goblin(Villain):
    def __init__(self):
        super().__init__("Goblin", hp=28, attack=6, defense=1, speed=4)


class Dragon(Villain):
    def __init__(self):
        super().__init__("Dragon", hp=90, attack=15, defense=5, speed=6)


# ----------------------------------------------------------------------
#  COMBAT SYSTEM
# ----------------------------------------------------------------------

def combat(hero, enemy):
    slow_print(f"\n⚠️   A {enemy.name} blocks your path! ⚠️")
    pause()

    while hero.is_alive() and enemy.is_alive():
        print("\n" + "-" * 50)
        hero.show_stats()
        enemy.show_stats()

        moves = hero.get_moves()
        print("\n  What will you do?")
        for key, (mv_name, *_rest) in moves.items():
            print(f"   {key}. {mv_name}")

        choice = get_choice("  > ", list(moves.keys()))
        move_name, dmg_mult, hit_chance, kind = moves[choice]

        defending = False
        parry_ready = False

        if kind == "attack":
            if random.random() <= hit_chance:
                dmg = int(hero.attack_power * dmg_mult * random.uniform(0.85, 1.15))
                actual = enemy.take_damage(dmg)
                print(f"\n  You use {move_name} and deal {actual} damage to the {enemy.name}!")
            else:
                print(f"\n  You use {move_name}... but it misses!")
        elif kind == "deflect":
            defending = True
            print("\n  You raise your guard, ready to deflect the next blow.")
        elif kind == "parry":
            parry_ready = True
            print("\n  You focus, timing a parry for the enemy's attack.")

        if not enemy.is_alive():
            break

        # --- Enemy's turn ---
        pause(0.5)
        base_dmg = int(enemy.attack_power * random.uniform(0.85, 1.15))

        if parry_ready:
            if random.random() < 0.5:
                counter_dmg = int(hero.attack_power * 0.9)
                actual = enemy.take_damage(counter_dmg)
                print(f"  The {enemy.name} attacks — you PARRY and counter for {actual} damage!")
            else:
                actual = hero.take_damage(base_dmg)
                print(f"  Your parry fails! The {enemy.name} hits you for {actual} damage.")
        elif defending:
            actual = hero.take_damage(int(base_dmg * 0.35))
            print(f"  You deflect the attack, taking only {actual} damage.")
        else:
            actual = hero.take_damage(base_dmg)
            print(f"  The {enemy.name} strikes you for {actual} damage!")

        if not hero.is_alive():
            break

    return hero.is_alive()


# ----------------------------------------------------------------------
#  GAME CLASS - STORY / STATE MANAGEMENT
# ----------------------------------------------------------------------

class Game:
    def __init__(self):
        self.hero = None

    # ---------------- Story scenes ----------------

    def intro(self):
        print("\n" + "=" * 55)
        slow_print("           🐉  DRAGON'S SHADOW  🐉")
        print("=" * 55)
        name = input("\nBefore we begin... what is your name, hero? > ").strip()
        if not name:
            name = "Hero"
        self.hero = Hero(name)
        pause()
        slow_print(f"\nYou are {self.hero.name}. A quiet villager, an ordinary")
        slow_print("soul, with no idea that today your life will change forever.")
        pause()
        self.house_scene()

    def house_scene(self):
        print()
        slow_print("You wake up in your small wooden house. The morning light")
        slow_print("creeps through the window... but something is wrong.")
        slow_print("Outside, you hear shouting, screaming, and panicked footsteps.")

        print("\nWhat do you do?")
        print("  1. Go back to sleep")
        print("  2. Go check what the noises are about")
        choice = get_choice("> ", ["1", "2"])

        if choice == "1":
            self.ending_lazy()
        else:
            self.noise_scene()

    def noise_scene(self):
        print()
        slow_print("You step outside, rubbing the sleep from your eyes.")
        slow_print("The village square is in chaos. People are pointing to the sky.")
        pause()
        slow_print("A massive shadow passes overhead — leathery wings, a roar")
        slow_print("that shakes the rooftops. A DRAGON has swooped down and")
        slow_print("snatched the Princess right from the castle balcony!")
        pause()
        slow_print("The villagers are panicking. The guards are frozen in fear.")

        print("\nWhat do you do?")
        print("  1. Who cares about the princess, live your life")
        print("  2. Be a hero — go save her")
        choice = get_choice("> ", ["1", "2"])

        if choice == "1":
            self.ending_coward()
        else:
            self.path_scene()

    def path_scene(self):
        print()
        slow_print("Your heart pounds. You've decided — you will save the princess.")
        slow_print("You grab whatever you can find and head toward the wilderness")
        slow_print("beyond the village. Two paths lie ahead of you:")

        print("\nWhere do you go?")
        print("  1. The Forest (said to lead straight to the dragon's lair)")
        print("  2. The Cave (a darker, closer route)")
        choice = get_choice("> ", ["1", "2"])

        if choice == "1":
            self.try_forest_early()
        else:
            self.cave_scene()

    def try_forest_early(self):
        print()
        slow_print("You start toward the forest, but your legs give out almost")
        slow_print("immediately. You're out of shape and out of breath —")
        slow_print(f"your stamina ({self.hero.stamina}) isn't nearly enough for that journey.")
        pause()
        slow_print("You'll need to build yourself up first. The cave it is.")
        pause()
        self.cave_scene()

    def cave_scene(self):
        print()
        slow_print("You creep into the damp, narrow cave. Water drips somewhere")
        slow_print("in the darkness. Suddenly, a snarling GOBLIN leaps out,")
        slow_print("blocking your path, brandishing a crude rusty blade!")

        print("\nWhat do you do?")
        print("  1. Fight")
        print("  2. Run away")
        choice = get_choice("> ", ["1", "2"])

        if choice == "2":
            self.ending_ran()
            return

        goblin = Goblin()
        won = combat(self.hero, goblin)

        if not won:
            self.ending_defeated(goblin.name)
            return

        print()
        slow_print("You land the final blow — the goblin collapses, defeated!")
        pause()
        slow_print("Searching the cave floor, you find a GLEAMING SWORD wedged")
        slow_print("between the rocks, along with the goblin's small satchel of")
        slow_print("supplies that restores some of your strength.")
        sword = Weapon("Ancient Sword", attack_bonus=5, defense_bonus=2, speed_bonus=1)
        self.hero.equip(sword)
        pause()
        slow_print("\nYou feel ready now. It's time to head to the forest, and")
        slow_print("face the dragon.")
        pause()
        self.forest_scene()

    def forest_scene(self):
        print()
        slow_print("With your new sword at your side and stamina renewed, you")
        slow_print("march confidently into the forest. The trees grow thicker,")
        slow_print("the air grows hotter... until you reach a scorched clearing.")
        pause()
        slow_print("There she is — the Princess, chained near the mouth of a cave,")
        slow_print("and coiled before her, a massive DRAGON, smoke curling from")
        slow_print("its nostrils as it turns to face you.")
        pause()

        print("\nWhat do you do?")
        print("  1. Fight the dragon")
        print("  2. Turn back")
        choice = get_choice("> ", ["1", "2"])

        if choice == "2":
            self.ending_ran()
            return

        dragon = Dragon()
        won = combat(self.hero, dragon)

        if not won:
            self.ending_defeated(dragon.name)
            return

        self.ending_victory()

    # ---------------- Endings ----------------

    def ending_lazy(self):
        print()
        slow_print("You roll over and go back to sleep. Whatever's happening")
        slow_print("outside isn't your problem...")
        slow_print("\n💤  YOU LAZY! GAME OVER.  💤")
        self.ask_replay()

    def ending_coward(self):
        print()
        slow_print("You shrug and head back inside. Not every problem needs")
        slow_print("a hero. The princess's fate is no longer your concern.")
        slow_print("\n🏚  YOU CHOSE TO LIVE YOUR LIFE. GAME OVER.  🏚")
        self.ask_replay()

    def ending_ran(self):
        print()
        slow_print("You turn and flee, your heart hammering with fear.")
        slow_print("The princess's cries echo behind you as you disappear")
        slow_print("into the trees, never to return.")
        slow_print("\n🏃  YOU RAN AWAY. GAME OVER.  🏃")
        self.ask_replay()

    def ending_defeated(self, enemy_name):
        print()
        slow_print(f"The {enemy_name} overwhelms you. Your vision fades to black")
        slow_print("as your quest ends here, in failure.")
        slow_print("\n💀  YOU WERE DEFEATED. GAME OVER.  💀")
        self.ask_replay()

    def ending_victory(self):
        print()
        slow_print("With a final, mighty strike, the dragon lets out a")
        slow_print("thunderous roar and collapses, defeated at last!")
        pause()
        slow_print("You rush to the princess and break her chains. She looks")
        slow_print("at you with grateful, teary eyes.")
        pause()
        slow_print(f'\n"Thank you, {self.hero.name}. You are truly a hero," she says.')
        slow_print("\n👑  VICTORY! YOU SAVED THE PRINCESS!  👑")
        self.ask_replay()

    # ---------------- Replay loop ----------------

    def ask_replay(self):
        choice = get_choice("\nPlay again? (yes/no) > ", ["yes", "no", "y", "n"])
        if choice in ("yes", "y"):
            print("\n" * 2)
            self.intro()
        else:
            print("\nThanks for playing DRAGON'S SHADOW. Farewell, hero.")
            sys.exit(0)


# ----------------------------------------------------------------------
#  ENTRY POINT
# ----------------------------------------------------------------------

if __name__ == "__main__":
    game = Game()
    game.intro()