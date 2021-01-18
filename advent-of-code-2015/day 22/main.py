"""Advent of Code 2015 Day 22."""

PLAYER = object()
BOSS = object()


def main(file_input='input.txt'):
    boss = parse_boss([line.strip() for line in get_file_contents(file_input)])
    player = get_player()
    fights = simulate(player, boss, [], {})
    won_by_player = [fight for fight in fights if fight[0] is PLAYER]
    won_by_mana = sorted(won_by_player, key=lambda item: item[1])
    print(f'Minimum mana to win: {won_by_mana[0][1]}')
    hard = simulate(player, boss, [],
                    {'Level Hard': [{'Player Turn': (heal, -1)}, -1]},
                    0,
                    {})
    won_on_hard_by_player = [fight for fight in hard if fight[0] is PLAYER]
    won_on_hard = sorted(won_on_hard_by_player, key=lambda item: item[1])
    print(f'Minimum mana to win on level hard: {won_on_hard[0][1]}')


def simulate(player, boss, cur_fight, effects, mana=0, memo={}):
    """Make fight simulations finding possible combinations until win."""
    key = ','.join((str(player), str(boss)))
    if key in memo:
        return memo[key]
    if is_dead(boss):
        return [(PLAYER, mana, cur_fight)]
    elif is_dead(player):
        return [(BOSS, mana, cur_fight)]
    if len(cur_fight) > 20:
        return []

    last_player = cur_fight[-1][0] if cur_fight else BOSS
    cur_player, cur_boss = player.copy(), boss.copy()
    effects = apply_effects(effects.copy(), cur_player, cur_boss, last_player)

    if is_dead(cur_boss):
        return [(PLAYER, mana, cur_fight)]
    elif is_dead(cur_player):
        return [(BOSS, mana, cur_fight)]

    result = make_next_turn(last_player,
                            effects,
                            cur_player,
                            cur_boss,
                            cur_fight,
                            mana,
                            memo)
    memo[key] = result
    return result


def make_next_turn(last_player, *args):
    """Call correct turn function based on last_player."""
    last_player_to_next_turn = {
        BOSS: player_turn,
        PLAYER: boss_turn,
    }
    return last_player_to_next_turn[last_player](*args)


def player_turn(effects, cur_player, cur_boss, cur_fight, mana, memo):
    """Make player turn."""
    possible_turns = get_possible_player_turns(
        effects, cur_player, cur_boss, cur_fight, mana, memo)
    return possible_turns if possible_turns else [(BOSS, mana, cur_fight)]


def boss_turn(effects, cur_player, cur_boss, cur_fight, mana, memo):
    """Make boss turn."""
    next_player, next_boss = cur_player.copy(), cur_boss.copy()
    damage = next_boss['Damage'] - next_player['Armor']
    cast_spell((do_damage, damage if damage > 0 else 1),
               next_boss, next_player)
    return simulate(next_player,
                    next_boss,
                    cur_fight + [(BOSS, (do_damage, damage))],
                    effects.copy(),
                    mana,
                    memo)


def is_dead(player):
    """Check if player is dead."""
    return player['Hit Points'] <= 0


def get_possible_player_turns(effects, player, boss, fight, mana, memo):
    """Get possible next turns based on active effects and player mana."""
    possible_turns = []
    for spell in get_spells():
        spell_name, mana_cost, spell_actions = spell
        if spell_name in effects or mana_cost > player['Mana']:
            continue
        next_player, next_boss = player.copy(), boss.copy()
        next_effects = effects.copy()
        apply_spell(spell_actions, spell_name, next_effects, next_player,
                    next_boss)
        next_player['Mana'] -= mana_cost
        next_turns = simulate(next_player,
                              next_boss,
                              fight + [(PLAYER, (spell_name))],
                              next_effects,
                              mana + mana_cost,
                              memo)
        possible_turns.extend(next_turns)
    return possible_turns


def apply_spell(spell_actions, spell_name, effects, player, boss):
    """Apply spell_actions. If needed add effect to effect."""
    for action in spell_actions:
        if action[0] == 'effect':
            effect_actions, timer = action[1:]
            if 'Start' in effect_actions:
                cast_spell(effect_actions['Start'], player, boss)
            effects[spell_name] = [effect_actions, timer]
        else:
            cast_spell(action, player, boss)


def apply_effects(effects, player, boss, last_player):
    """Apply all active effects to player and boss and based on last_player."""
    for effect_name, (effect_actions, timer) in effects.copy().items():
        if 'Player Turn' in effect_actions and last_player is BOSS:
            cast_spell(effect_actions['Player Turn'], player, boss)
        if 'Middle' in effect_actions:
            cast_spell(effect_actions['Middle'], player, boss)
        timer -= 1
        effects[effect_name] = [effect_actions, timer]
        is_effect_ending = timer == 0
        if is_effect_ending and 'End' in effect_actions:
            cast_spell(effect_actions['End'], player, boss)
        if is_effect_ending:
            effects.pop(effect_name)
    return effects


def cast_spell(spell_to_cast, attacker, defender):
    """Cast spell from spell_to_cast tuple of spell and value."""
    spell, value = spell_to_cast
    spell(value, attacker, defender)


def do_damage(value, attacker, defender):
    """Do value damage to defender."""
    add_to_attribute('Hit Points', -value, defender)


def heal(value, attacker, defender):
    """Add value to hit points for attacker."""
    add_to_attribute('Hit Points', value, attacker)


def add_armor(value, attacker, defender):
    """Add value to armor for attacker."""
    add_to_attribute('Armor', value, attacker)


def add_mana(value, attacker, defender):
    """Add value to mana for attacker."""
    add_to_attribute('Mana', value, attacker)


def add_to_attribute(attribute, value, player):
    """Add value to attribute for player."""
    player[attribute] += value


def get_player(hp=50, mana=500):
    return {'Hit Points': hp, 'Mana': mana, 'Armor': 0}


def parse_boss(lines):
    """Parse boss data from lines to dictionary."""
    boss = {}
    for line in lines:
        attribute, value = line.split(':')
        boss[attribute] = int(value)
    return boss


def get_spells():
    """Get available spells."""
    return [('Magic Missle', 53, [(do_damage, 4)]),
            ('Drain', 73, [(do_damage, 2), (heal, 2)]),
            ('Shield', 113, [['effect', {'Start': (add_armor, 7),
                                         'End': (add_armor, -7)}, 6]]),
            ('Poison', 173, [['effect', {'Middle': (do_damage, 3)}, 6]]),
            ('Recharge', 229, [['effect', {'Middle': (add_mana, 101)}, 5]])]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
