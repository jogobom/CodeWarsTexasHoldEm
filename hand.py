from pipeop import pipes
from itertools import groupby


def nothing(cards):
    return cards, ('nothing', [c[:1] for c in cards[:5]])


def find_trick(previous, trick_size, trick_count_needed, trick_name):
    cards = [c[:1] for c in previous[0]]
    grouped = [list(g[1]) for g in groupby(cards)]
    tricks_found = list(filter(lambda g: len(g) >= trick_size, grouped))
    if len(tricks_found) >= trick_count_needed:
        flattened_tricks = [c for trick in tricks_found[:trick_count_needed] for c in trick[:trick_size]]
        cards_not_included_in_trick = list(filter(lambda c: c not in flattened_tricks, cards))
        number_of_cards_to_fill_hand = 5 - len(flattened_tricks)
        print(f'{number_of_cards_to_fill_hand} needed from {cards_not_included_in_trick} to fill hand after finding {flattened_tricks}')
        return cards, (trick_name,
                       [*[t[0] for t in tricks_found],
                        *[c[:1] for c in cards_not_included_in_trick][:number_of_cards_to_fill_hand]])
    else:
        return previous


def pair(previous):
    return find_trick(previous, trick_size=2, trick_count_needed=1, trick_name='pair')


def two_pair(previous):
    return find_trick(previous, trick_size=2, trick_count_needed=2, trick_name='two pair')


def three_of_a_kind(previous):
    return find_trick(previous, trick_size=3, trick_count_needed=1, trick_name='three-of-a-kind')


@pipes
def hand(hole_cards, community_cards):
    print()
    cards = hole_cards + community_cards
    card_order = ['A', 'K', 'Q', 'J', '9', '8', '7', '6', '5', '4', '3', '2']
    priorities = {card_order[i]: i for i in range(len(card_order))}
    cards.sort(key=lambda e: priorities[e[:1]])
    cards_and_best_hand = nothing(cards) >> pair >> two_pair >> three_of_a_kind
    return cards_and_best_hand[1]
