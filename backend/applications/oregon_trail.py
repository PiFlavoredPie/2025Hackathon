#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oregon Trail (Terminal Edition)

A self-contained, text-based game inspired by MECC's classic "The Oregon Trail".
This version is designed to be simple to run (no external packages), while
still capturing the core decisions: supplies, pace, rations, hunting,
river crossings, and random events.

How to run:
    python3 oregon_trail.py

Target: Python 3.9+ (but generally works on 3.7+)
Dependencies: Standard library only.

Author: ChatGPT (2025)
License: MIT
"""

import sys
import random
import textwrap
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date, timedelta

# ----------------------------- Utility helpers -----------------------------

def wrap(text: str, width: int = 80) -> str:
    return "\n".join(textwrap.wrap(text, width=width))

def prompt_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            val = int(input(f"{prompt} "))
        except ValueError:
            print("Please enter a number.")
            continue
        if val < min_value or val > max_value:
            print(f"Enter a number between {min_value} and {max_value}.")
            continue
        return val

def prompt_choice(prompt: str, options: Dict[str, str]) -> str:
    """
    options: mapping from short key (e.g. 'a','b','c') to label shown.
    Returns the selected key.
    """
    keys = list(options.keys())
    while True:
        print(prompt)
        for k in keys:
            print(f"  [{k}] {options[k]}")
        choice = input("> ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice, try again.")

def yes_no(prompt: str) -> bool:
    while True:
        resp = input(f"{prompt} [y/n] ").strip().lower()
        if resp in ("y", "yes"): return True
        if resp in ("n", "no"): return False
        print("Please enter y or n.")

def money_to_str(cents: int) -> str:
    dollars = cents // 100
    cents_rem = cents % 100
    return f"${dollars:,}.{cents_rem:02d}"

def clamp(v: int, a: int, b: int) -> int:
    return max(a, min(b, v))

# ----------------------------- Game structures -----------------------------

@dataclass
class Person:
    name: str
    alive: bool = True
    health: int = 100  # 0-100

@dataclass
class Party:
    leader: str
    members: List[Person]
    money_cents: int
    pace: str = "steady"     # 'steady','strenuous','grueling'
    rations: str = "normal"  # 'bare-bones','meager','normal','filling'

    def living_members(self) -> List[Person]:
        return [p for p in self.members if p.alive]

    def size(self) -> int:
        return len(self.living_members())

@dataclass
class Supplies:
    oxen: int = 6           # head of oxen
    food_lbs: int = 0
    ammo: int = 0           # bullets
    clothing: int = 0       # sets
    wheels: int = 2
    axles: int = 2
    tongues: int = 2

@dataclass
class GameState:
    trail_miles: int = 0
    total_miles: int = 2000  # Independence, MO to Willamette Valley, OR
    date: date = field(default_factory=lambda: date(1848, 3, 1))  # Start Mar 1, 1848
    party: Party = None  # type: ignore
    supplies: Supplies = field(default_factory=Supplies)
    landmarks: List[Dict] = field(default_factory=list)
    next_landmark_idx: int = 0
    game_over: bool = False
    victory: bool = False

# ----------------------------- Content data -----------------------------

PROFESSIONS = {
    "a": ("Banker", 160000),     # $1600.00
    "b": ("Carpenter", 80000),   # $800.00
    "c": ("Farmer", 40000),      # $400.00
}

RATION_MULTIPLIERS = {
    "bare-bones": 0.5,
    "meager": 0.75,
    "normal": 1.0,
    "filling": 1.25,
}

PACE_MPD = {  # base miles per day by pace
    "steady": (12, 18),
    "strenuous": (16, 24),
    "grueling": (20, 30),
}

WEATHER_BY_MONTH = {
    3: ("cold", -2),     # (label, health modifier per day)
    4: ("chilly", -1),
    5: ("mild", 0),
    6: ("warm", -1),
    7: ("hot", -2),
    8: ("hot", -2),
    9: ("cool", -1),
    10: ("cold", -2),
}

STORE_PRICES = {
    # cents per unit
    "oxen": 2500,       # $25 per ox
    "food_lbs": 20,     # $0.20 / lb
    "ammo": 5,          # $0.05 / bullet
    "clothing": 1000,   # $10 / set
    "wheel": 1500,      # $15
    "axle": 1500,
    "tongue": 1500,
}

LANDMARKS = [
    {"name": "Kaw River Crossing", "mile": 102, "river": True, "depth_ft": (2, 6)},
    {"name": "Fort Kearny", "mile": 623, "river": False},
    {"name": "Chimney Rock", "mile": 664, "river": False},
    {"name": "Fort Laramie", "mile": 788, "river": False},
    {"name": "Independence Rock", "mile": 940, "river": False},
    {"name": "South Pass", "mile": 1092, "river": False},
    {"name": "Green River Crossing", "mile": 1195, "river": True, "depth_ft": (3, 8)},
    {"name": "Fort Hall", "mile": 1403, "river": False},
    {"name": "Snake River Crossing", "mile": 1640, "river": True, "depth_ft": (4, 10)},
    {"name": "Fort Boise", "mile": 1753, "river": False},
    {"name": "The Dalles", "mile": 1965, "river": False},
]

# ----------------------------- Core systems -----------------------------

def banner():
    print("=" * 72)
    print(" " * 18 + "THE OREGON TRAIL — Terminal Edition")
    print("=" * 72)

def explain():
    print(wrap(
        "You are about to begin a great adventure: crossing 2,000 miles of the North "
        "American wilderness. You must decide your supplies, manage food rations and "
        "pace, hunt for food, and survive illnesses and river crossings. Reach Oregon "
        "before the harsh winter to win."
    ))
    print()

def setup_party() -> Party:
    print("Choose your profession:")
    for k, (name, money) in PROFESSIONS.items():
        print(f"  [{k}] {name} — start with {money_to_str(money)}")
    choice = prompt_choice("What is your profession?", PROFESSIONS)
    prof_name, money = PROFESSIONS[choice]

    print()
    leader = input("What is the first name of the leader? ").strip() or "Leader"
    members = [Person(leader)]
    print("Enter the names of up to 4 additional party members (blank to stop).")
    while len(members) < 5:
        nm = input(f" Member {len(members)} name: ").strip()
        if not nm:
            break
        members.append(Person(nm))

    print()
    print(f"You chose to be a {prof_name} with {len(members)} party member(s).")
    return Party(leader=leader, members=members, money_cents=money)

def buy_supplies(party: Party, supplies: Supplies):
    print("\nGeneral Store at Independence, Missouri")
    print("-" * 72)
    print(wrap("You will need to buy supplies before starting your journey. "
               "You should buy: oxen (6-12), food (at least 200 lbs per person), "
               "ammunition, clothing, and spare wagon parts."))
    print()

    def purchase(item_key: str, label: str, min_val: int, max_val: int, pack: int = 1):
        nonlocal party
        price = STORE_PRICES[item_key]
        while True:
            qty = prompt_int(f"How many {label} ({money_to_str(price)} each)?", min_val, max_val)
            cost = qty * price
            if cost > party.money_cents:
                print(f"You can't afford that. You have {money_to_str(party.money_cents)}.")
                continue
            party.money_cents -= cost
            return qty * pack

    # Oxen: recommend 8-12
    print(f"You have {money_to_str(party.money_cents)}.")
    oxen = purchase("oxen", "oxen (recommend 8–12)", 6, 12)
    supplies.oxen = oxen
    print(f"Remaining money: {money_to_str(party.money_cents)}")

    food = prompt_int(
        f"How many pounds of food? ({money_to_str(STORE_PRICES['food_lbs'])} per lb)",
        200 * party.size(), 3000
    )
    cost_food = food * STORE_PRICES["food_lbs"]
    if cost_food > party.money_cents:
        print("You couldn't afford that much; buying as much as you can.")
        affordable = party.money_cents // STORE_PRICES["food_lbs"]
        food = max(0, affordable)
    party.money_cents -= food * STORE_PRICES["food_lbs"]
    supplies.food_lbs += food
    print(f"Remaining money: {money_to_str(party.money_cents)}")

    ammo = prompt_int(
        f"How many bullets? ({money_to_str(STORE_PRICES['ammo'])} each)",
        0, 500
    )
    cost_ammo = ammo * STORE_PRICES["ammo"]
    if cost_ammo > party.money_cents:
        affordable = party.money_cents // STORE_PRICES["ammo"]
        print(f"You couldn't afford that many; buying {affordable}.")
        ammo = affordable
    party.money_cents -= ammo * STORE_PRICES["ammo"]
    supplies.ammo += ammo
    print(f"Remaining money: {money_to_str(party.money_cents)}")

    clothing = prompt_int(
        f"How many sets of clothing? ({money_to_str(STORE_PRICES['clothing'])} each)",
        0, 10
    )
    cost_clothes = clothing * STORE_PRICES["clothing"]
    if cost_clothes > party.money_cents:
        affordable = party.money_cents // STORE_PRICES["clothing"]
        print(f"You couldn't afford that many; buying {affordable}.")
        clothing = affordable
    party.money_cents -= clothing * STORE_PRICES["clothing"]
    supplies.clothing += clothing
    print(f"Remaining money: {money_to_str(party.money_cents)}")

    for part_key in ("wheel", "axle", "tongue"):
        qty = prompt_int(f"How many spare {part_key}s? ({money_to_str(STORE_PRICES[part_key])} each)", 0, 3)
        cost = qty * STORE_PRICES[part_key]
        if cost > party.money_cents:
            affordable = party.money_cents // STORE_PRICES[part_key]
            print(f"You couldn't afford that many; buying {affordable}.")
            qty = affordable
        party.money_cents -= qty * STORE_PRICES[part_key]
        if part_key == "wheel": supplies.wheels += qty
        if part_key == "axle": supplies.axles += qty
        if part_key == "tongue": supplies.tongues += qty
        print(f"Remaining money: {money_to_str(party.money_cents)}")

    print("\nAll set! Time to head west.\n")

def init_game() -> GameState:
    banner()
    explain()
    party = setup_party()

    # Choose starting month
    month_map = {"a": "March", "b": "April", "c": "May", "d": "June", "e": "July"}
    mchoice = prompt_choice("What month do you want to start your trip?", month_map)
    month_name = month_map[mchoice]
    month_num = {"March":3,"April":4,"May":5,"June":6,"July":7}[month_name]
    gs = GameState(date=date(1848, month_num, 1))
    gs.party = party
    gs.landmarks = LANDMARKS.copy()

    buy_supplies(party, gs.supplies)

    # Set initial pace/rations
    pace_map = {"a":"steady","b":"strenuous","c":"grueling"}
    pchoice = prompt_choice("Choose your pace:", {"a":"steady (slow & safe)","b":"strenuous (faster)","c":"grueling (fast but risky)"})
    party.pace = pace_map[pchoice]

    rchoice = prompt_choice("Choose your rations:", {
        "a":"bare-bones (least food)",
        "b":"meager",
        "c":"normal",
        "d":"filling (most food)"
    })
    party.rations = {"a":"bare-bones","b":"meager","c":"normal","d":"filling"}[rchoice]

    return gs

# ----------------------------- Simulation logic -----------------------------

def daily_weather(d: date) -> Dict:
    label, health_mod = WEATHER_BY_MONTH.get(d.month, ("mild", 0))
    # Small randomness
    if random.random() < 0.15:
        label = random.choice(["rain", "windy", "very cold", "very hot"])
        if label == "very cold": health_mod -= 1
        if label == "very hot": health_mod -= 1
        if label == "rain": health_mod -= 0  # but can affect miles
        if label == "windy": health_mod -= 0
    return {"label": label, "health_mod": health_mod}

def consume_food(gs: GameState) -> None:
    eat_factor = RATION_MULTIPLIERS[gs.party.rations]
    daily_per_person = int(2 * 16 * eat_factor)  # 2 lbs per person baseline (approx), 16 oz/lb
    need = daily_per_person * gs.party.size()
    if gs.supplies.food_lbs >= need:
        gs.supplies.food_lbs -= need
    else:
        # Starvation: reduce health of all living members more
        shortage = need - gs.supplies.food_lbs
        gs.supplies.food_lbs = 0
        for p in gs.party.living_members():
            p.health = clamp(p.health - (10 + shortage // max(1, gs.party.size()*2)), 0, 100)

def travel_miles_for_day(gs: GameState, weather: Dict) -> int:
    lo, hi = PACE_MPD[gs.party.pace]
    miles = random.randint(lo, hi)

    # Weather effects
    if weather["label"] in ("rain", "very cold", "very hot"):
        miles = int(miles * 0.85)
    if gs.supplies.oxen < 6:
        miles = int(miles * 0.9)

    return max(5, miles)

def apply_daily_health(gs: GameState, weather: Dict) -> None:
    # Base adjustment from pace
    pace_penalty = {"steady": 0, "strenuous": -1, "grueling": -2}[gs.party.pace]

    # Ration effect (better rations = slightly better health)
    ration_bonus = {"bare-bones": -2, "meager": -1, "normal": 0, "filling": 1}[gs.party.rations]

    for p in gs.party.living_members():
        p.health = clamp(p.health + weather["health_mod"] + pace_penalty + ration_bonus, 0, 100)
        # Small fatigue
        p.health = clamp(p.health - random.randint(0, 1), 0, 100)
        if p.health == 0 and p.alive:
            p.alive = False
            print(f"☠ {p.name} has died.")

def random_events(gs: GameState, weather: Dict) -> None:
    """Random daily events that can help or hurt."""
    # Illness chance per person, higher under harsh conditions
    ill_base = 0.02
    if gs.party.pace == "grueling": ill_base += 0.01
    if gs.party.rations in ("bare-bones", "meager"): ill_base += 0.01
    if weather["label"] in ("very cold", "very hot"): ill_base += 0.01

    for p in gs.party.living_members():
        if random.random() < ill_base:
            disease = random.choice(["dysentery", "exhaustion", "cholera", "measles", "typhoid", "bad cold"])
            loss = random.randint(10, 25)
            p.health = clamp(p.health - loss, 0, 100)
            print(f"⚕ {p.name} fell ill with {disease} (-{loss} health).")
            if p.health == 0:
                p.alive = False
                print(f"☠ {p.name} has died of {disease}.")

    # Wagon mishaps
    mishap_chance = 0.04
    if gs.party.pace == "grueling": mishap_chance += 0.01
    if random.random() < mishap_chance:
        mishap = random.choice(["broken wheel", "broken axle", "broken tongue", "lost the trail", "bad water", "thief at night"])
        if mishap == "broken wheel":
            if gs.supplies.wheels > 0:
                gs.supplies.wheels -= 1
                print("🛠 A wagon wheel broke. You used a spare.")
            else:
                print("🛠 A wagon wheel broke, and you have no spare. You lost 2 days to repair.")
                gs.date += timedelta(days=1)  # extra day lost (on top of daily increment)
        elif mishap == "broken axle":
            if gs.supplies.axles > 0:
                gs.supplies.axles -= 1
                print("🛠 A wagon axle broke. You used a spare.")
            else:
                print("🛠 A wagon axle broke, and you have no spare. You lost 2 days to repair.")
                gs.date += timedelta(days=1)
        elif mishap == "broken tongue":
            if gs.supplies.tongues > 0:
                gs.supplies.tongues -= 1
                print("🛠 A wagon tongue broke. You used a spare.")
            else:
                print("🛠 A wagon tongue broke, and you have no spare. You lost 2 days to repair.")
                gs.date += timedelta(days=1)
        elif mishap == "lost the trail":
            lost_days = random.randint(1, 3)
            print(f"🧭 You got lost. You lost {lost_days} day(s).")
            gs.date += timedelta(days=lost_days - 1)  # -1 because we'll still advance a day below
        elif mishap == "bad water":
            print("💧 Bad water made everyone feel worse (-5 health).")
            for p in gs.party.living_members():
                p.health = clamp(p.health - 5, 0, 100)
        elif mishap == "thief at night":
            stolen = min(gs.supplies.food_lbs, random.randint(10, 40))
            gs.supplies.food_lbs -= stolen
            print(f"🕵 A thief stole {stolen} lbs of food.")

def check_landmark(gs: GameState) -> Optional[Dict]:
    if gs.next_landmark_idx >= len(gs.landmarks):
        return None
    lm = gs.landmarks[gs.next_landmark_idx]
    if gs.trail_miles >= lm["mile"]:
        print(f"\n=== You reached {lm['name']} (mile {lm['mile']}) ===")
        gs.next_landmark_idx += 1
        return lm
    return None

def river_crossing(gs: GameState, lm: Dict):
    print("\nA river blocks your path.")
    depth = random.randint(*lm.get("depth_ft", (3, 7)))
    width = random.randint(200, 400)  # feet
    print(f"Estimated river depth: {depth} ft; width: ~{width} ft.")

    options = {
        "a": "Attempt to ford (risky)",
        "b": "Caulk wagon & float (safer, lose a day)",
        "c": "Find a ferry (cost money, safer)",
        "d": "Wait and rest a day",
    }
    choice = prompt_choice("How will you cross?", options)

    risk = 0.0
    lost_food = 0
    if choice == "a":
        risk = 0.25 + 0.05 * max(0, depth - 3)
    elif choice == "b":
        risk = 0.10 + 0.03 * max(0, depth - 3)
        gs.date += timedelta(days=1)
    elif choice == "c":
        fee = 500  # $5
        if gs.party.money_cents >= fee:
            gs.party.money_cents -= fee
            print(f"You paid {money_to_str(fee)} for the ferry.")
            risk = 0.04 + 0.02 * max(0, depth - 3)
        else:
            print("You don't have enough money; you must ford.")
            risk = 0.25 + 0.05 * max(0, depth - 3)
    elif choice == "d":
        print("You camp and wait for better conditions.")
        gs.date += timedelta(days=1)
        # Try again recursively
        return river_crossing(gs, lm)

    if random.random() < risk:
        print("🌊 Disaster! The wagon swamped while crossing.")
        # Lose some supplies; potential injury
        lost_food = min(gs.supplies.food_lbs, random.randint(20, 100))
        gs.supplies.food_lbs -= lost_food
        if gs.supplies.ammo > 0 and random.random() < 0.5:
            lost_ammo = min(gs.supplies.ammo, random.randint(10, 50))
            gs.supplies.ammo -= lost_ammo
            print(f"You lost {lost_food} lbs of food and {lost_ammo} bullets.")
        else:
            print(f"You lost {lost_food} lbs of food.")
        for p in gs.party.living_members():
            if random.random() < 0.3:
                injury = random.randint(5, 20)
                p.health = clamp(p.health - injury, 0, 100)
                print(f"{p.name} was injured (-{injury} health).")
                if p.health == 0:
                    p.alive = False
                    print(f"☠ {p.name} drowned.")
    else:
        print("You crossed safely.")

def hunt(gs: GameState):
    if gs.supplies.ammo < 10:
        print("You don't have enough ammunition to hunt (need at least 10 bullets).")
        return
    print("You spend the day hunting.")
    gs.date += timedelta(days=1)
    gs.supplies.ammo -= random.randint(8, 20)
    gain = random.randint(40, 160)
    # Spoilage if too much
    if gs.party.size() <= 2 and gain > 100:
        spoil = random.randint(10, 40)
    else:
        spoil = random.randint(0, 20)
    kept = max(0, gain - spoil)
    gs.supplies.food_lbs += kept
    print(f"You brought back {gain} lbs of game, but {spoil} lbs spoiled. (+{kept} lbs food)")

def rest(gs: GameState):
    print("You decide to rest for the day.")
    gs.date += timedelta(days=1)
    for p in gs.party.living_members():
        heal = random.randint(3, 7)
        p.health = clamp(p.health + heal, 0, 100)
    # Consume food even while resting
    consume_food(gs)

def trade(gs: GameState):
    print("A trader approaches your camp...")
    offers = [
        {"give": ("ammo", random.randint(20, 60)), "for": ("food_lbs", random.randint(20, 60))},
        {"give": ("food_lbs", random.randint(30, 80)), "for": ("money_cents", 500)},
        {"give": ("clothing", 1), "for": ("food_lbs", 40)},
        {"give": ("wheel", 1), "for": ("ammo", 50)},
    ]
    offer = random.choice(offers)
    give_key, give_qty = offer["give"]
    for_key, for_qty = offer["for"]
    # Show offer description
    def label(key, qty):
        names = {
            "ammo": "bullets",
            "food_lbs": "lbs of food",
            "money_cents": "cash",
            "clothing": "set of clothing",
            "wheel": "wagon wheel",
        }
        return f"{qty} {names[key]}"
    print(f"Offer: they'll give you {label(give_key, give_qty)} for {label(for_key, for_qty)}.")
    if not yes_no("Accept the trade?"):
        print("You decline the trade.")
        return

    # Check resources
    def have_resource(key, qty):
        if key == "money_cents": return gs.party.money_cents >= qty
        if key == "ammo": return gs.supplies.ammo >= qty
        if key == "food_lbs": return gs.supplies.food_lbs >= qty
        if key == "clothing": return gs.supplies.clothing >= qty
        if key == "wheel": return gs.supplies.wheels >= qty
        return False

    def add_resource(key, qty):
        if key == "money_cents": gs.party.money_cents += qty
        if key == "ammo": gs.supplies.ammo += qty
        if key == "food_lbs": gs.supplies.food_lbs += qty
        if key == "clothing": gs.supplies.clothing += qty
        if key == "wheel": gs.supplies.wheels += qty

    def sub_resource(key, qty):
        if key == "money_cents": gs.party.money_cents -= qty
        if key == "ammo": gs.supplies.ammo -= qty
        if key == "food_lbs": gs.supplies.food_lbs -= qty
        if key == "clothing": gs.supplies.clothing -= qty
        if key == "wheel": gs.supplies.wheels -= qty

    if not have_resource(for_key, for_qty):
        print("You don't have enough to make that trade.")
        return
    sub_resource(for_key, for_qty)
    add_resource(give_key, give_qty)
    print("The trade is complete.")

def status(gs: GameState, weather: Dict):
    print("-" * 72)
    print(f"Date: {gs.date.strftime('%b %d, %Y')}   Weather: {weather['label']}   "
          f"Miles: {gs.trail_miles}/{gs.total_miles}")
    print(f"Pace: {gs.party.pace.title()}   Rations: {gs.party.rations.title()}")
    print(f"Food: {gs.supplies.food_lbs} lbs   Ammo: {gs.supplies.ammo}   "
          f"Clothing: {gs.supplies.clothing} sets")
    print(f"Parts: wheels {gs.supplies.wheels}, axles {gs.supplies.axles}, tongues {gs.supplies.tongues}")
    print(f"Oxen: {gs.supplies.oxen}   Cash: {money_to_str(gs.party.money_cents)}")
    print("Party health: " + ", ".join([f"{p.name}({p.health})" for p in gs.party.living_members()]))
    if gs.next_landmark_idx < len(gs.landmarks):
        next_lm = gs.landmarks[gs.next_landmark_idx]
        dist_next = max(0, next_lm["mile"] - gs.trail_miles)
        print(f"Next landmark: {next_lm['name']} in {dist_next} miles")
    else:
        print("No more landmarks ahead.")
    print("-" * 72)

def choose_action(gs: GameState) -> str:
    opts = {
        "t": "Travel",
        "r": "Rest",
        "h": "Hunt",
        "d": "Change rations",
        "p": "Change pace",
        "s": "Status / Continue",
        "x": "Trade",
        "q": "Quit game",
    }
    return prompt_choice("What do you want to do today?", opts)

def change_pace(gs: GameState):
    choice = prompt_choice("Choose new pace:", {"a":"steady","b":"strenuous","c":"grueling"})
    gs.party.pace = {"a":"steady","b":"strenuous","c":"grueling"}[choice]
    print(f"Pace set to {gs.party.pace}.")

def change_rations(gs: GameState):
    choice = prompt_choice("Choose new rations:", {"a":"bare-bones","b":"meager","c":"normal","d":"filling"})
    gs.party.rations = {"a":"bare-bones","b":"meager","c":"normal","d":"filling"}[choice]
    print(f"Rations set to {gs.party.rations}.")

def day_loop(gs: GameState):
    while not gs.game_over and not gs.victory:
        weather = daily_weather(gs.date)
        status(gs, weather)

        # Lose if everyone dies or it's winter deep (Dec 1) and not finished
        if gs.party.size() == 0:
            print("Your entire party has perished. Game over.")
            gs.game_over = True
            break
        if gs.date >= date(1848, 12, 1) and gs.trail_miles < gs.total_miles:
            print("Winter has arrived and you are still on the trail. The journey becomes impossible.")
            gs.game_over = True
            break

        action = choose_action(gs)

        if action == "q":
            if yes_no("Are you sure you want to quit?"):
                print("You abandon the journey. Game over.")
                gs.game_over = True
                break
            else:
                continue

        if action == "r":
            rest(gs)
            # day already advanced in rest()
        elif action == "h":
            hunt(gs)
            consume_food(gs)  # still consume food for that day
            apply_daily_health(gs, weather)
            random_events(gs, weather)
        elif action == "x":
            trade(gs)
            # trading doesn't inherently consume a day; ask user
            if yes_no("Camp for the night? (advance one day)"):
                gs.date += timedelta(days=1)
                consume_food(gs)
                apply_daily_health(gs, weather)
                random_events(gs, weather)
        elif action == "d":
            change_rations(gs)
            continue  # no day passes
        elif action == "p":
            change_pace(gs)
            continue  # no day passes
        else:
            # Travel day
            miles = travel_miles_for_day(gs, weather)
            gs.trail_miles += miles
            gs.date += timedelta(days=1)
            print(f"You traveled {miles} miles today.")
            consume_food(gs)
            apply_daily_health(gs, weather)
            random_events(gs, weather)

            # Landmark check
            lm = check_landmark(gs)
            if lm and lm.get("river"):
                river_crossing(gs, lm)

        # Victory check
        if gs.trail_miles >= gs.total_miles:
            gs.victory = True
            break

    if gs.victory:
        print("\n🏁 You made it to Oregon City! Congratulations!")
        survivors = [p for p in gs.party.members if p.alive]
        print(f"Survivors: {', '.join(p.name for p in survivors)}")
        score = gs.party.money_cents // 100 + gs.supplies.food_lbs // 5 + 50 * len(survivors)
        print(f"Final score: {score}")
    elif gs.game_over:
        print("\n☹ Better luck next time.")

def main():
    random.seed()
    gs = init_game()
    day_loop(gs)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Safe travels next time!")
