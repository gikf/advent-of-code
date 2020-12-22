# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:19:02 2020
"""
from collections import deque


def main():
    players_decks = parse_cards(get_file_contents().strip().split('\n\n'))
    end_decks = play_combat(players_decks)
    print('Combat')
    print('Deck scores: ', [score_deck(deck) for deck in end_decks])
    print('Recursive combat')
    recursive_decks = play_recursive_combat(players_decks)
    print('Deck scores: ', [score_deck(deck) for deck in recursive_decks])


def play_recursive_combat(decks):
    """Play recursive combat.

    If in previous round there were decks with the same card order, end game
    with win for player 1.
    If dealt cards have value equal or lower than number of cards left in each
    deck determine winner based on recursed game, with card count as dealt
    cards.
    """
    deck1, deck2 = [deck.copy() for deck in decks]
    memo = set()
    while deck1 and deck2:
        decks_key = f'{deck1}, {deck2}'
        if decks_key in memo:
            return deck1, deque()
        memo.add(decks_key)
        card1, card2 = [deck.popleft() for deck in (deck1, deck2)]
        if card1 <= len(deck1) and card2 <= len(deck2):
            sub_decks = [
                prepare_deck(deck, count)
                for deck, count in [(deck1, card1), (deck2, card2)]
            ]
            player1, player2 = play_recursive_combat(sub_decks)
            add_to_deck(deck1, deck2, bool(player1), card1, card2)
        else:
            add_to_deck(deck1, deck2, card1 > card2, card1, card2)
    return deck1, deck2


def prepare_deck(deck, number_of_cards):
    """Prepare sub_deck, from deck leaving starting number_of_cards cards."""
    sub_deck = deck.copy()
    while len(sub_deck) != number_of_cards:
        sub_deck.pop()
    return sub_deck


def play_combat(decks):
    """Play simple combat game."""
    deck1, deck2 = [deck.copy() for deck in decks]
    while deck1 and deck2:
        card1, card2 = [deck.popleft() for deck in (deck1, deck2)]
        add_to_deck(deck1, deck2, card1 > card2, card1, card2)
    return deck1, deck2


def add_to_deck(deck1, deck2, condition, card1, card2):
    """Add cards in correct order to deck1 or deck2 based on condition"""
    if condition:
        add_cards_to_deck(deck1, card1, card2)
    else:
        add_cards_to_deck(deck2, card2, card1)


def add_cards_to_deck(deck, *cards):
    """Add to deck all cards."""
    for card in cards:
        deck.append(card)


def parse_cards(input_file):
    """Parse cards from input."""
    players = []
    for deck in input_file:
        cards = deque([int(num) for num in deck.split('\n')[1:]])
        players.append(cards)
    return players


def score_deck(deck):
    """Score deck, multiply cards based on their position in the deck."""
    total_score = 0
    deck_size = len(deck)
    for score, card in enumerate(deck):
        total_score += (deck_size - score) * card
    return total_score


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
