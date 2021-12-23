from pipeop import pipes
from itertools import groupby


def nothing(cards):
    return cards, ('nothing', [c[:1] for c in cards[:5]])


def pair(previous):
    cards = [c[:1] for c in previous[0]]
    print(f'Cards are {cards}')
    grouped = [list(g[1]) for g in groupby(cards)]
    trick_size = 2
    trick_found = next(filter(lambda g: len(g) >= trick_size, grouped), None)
    print(f'Trick found is {trick_found}')
    if trick_found is not None:
        cards_not_included_in_trick = list(filter(lambda c: c not in trick_found, cards))
        number_of_cards_to_fill_hand = 5 - trick_size + 1
        return cards, ('pair',
                       [*trick_found[0], *[c[:1] for c in cards_not_included_in_trick]][:number_of_cards_to_fill_hand])
    else:
        return previous


@pipes
def hand(hole_cards, community_cards):
    cards = hole_cards + community_cards
    card_order = ['A', 'K', 'Q', 'J', '9', '8', '7', '6', '5', '4', '3', '2']
    priorities = {card_order[i]: i for i in range(len(card_order))}
    cards.sort(key=lambda e: priorities[e[:1]])
    cards_and_best_hand = nothing(cards) >> pair
    return cards_and_best_hand[1]
