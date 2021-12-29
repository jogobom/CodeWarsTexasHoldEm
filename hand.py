from pipeop import pipes
from itertools import groupby


def nothing(cards):
    return cards, ('nothing', [c[:1] for c in cards[:5]])


def get_card_value(card):
    return card[0:-1]


def get_card_suit(card):
    return card[-1]


def sort_cards_by_value(cards, value_getter=get_card_value):
    card_order = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    priorities = {card_order[i]: i for i in range(len(card_order))}
    return sorted(cards, key=lambda c: priorities[value_getter(c)])


def find_trick(previous, trick_size, trick_count_needed, trick_name, group_key_fn):
    cards = previous[0]
    grouped_cards = [list(g[1]) for g in groupby(cards, key=group_key_fn)]
    tricks_found = list(filter(lambda g: len(g) >= trick_size, grouped_cards))
    if len(tricks_found) >= trick_count_needed:
        return fill_hand(cards, trick_count_needed, trick_name, trick_size, tricks_found)
    else:
        return previous


def card_values_to_retain_from_trick(trick):
    return sort_cards_by_value(list(set([get_card_value(t) for t in trick])), value_getter=lambda c: c)


def fill_hand(cards, trick_count_needed, trick_name, trick_size, tricks_found):
    flattened_tricks = [c for trick in tricks_found[:trick_count_needed] for c in trick[:trick_size]]
    cards_not_included_in_trick = list(filter(lambda c: c not in flattened_tricks, cards))
    number_of_cards_to_fill_hand = 5 - len(flattened_tricks)
    return cards, (trick_name,
                   [*[c for t in tricks_found for c in card_values_to_retain_from_trick(t)],
                    *[get_card_value(c) for c in cards_not_included_in_trick][:number_of_cards_to_fill_hand]])


def pair(previous):
    return find_trick(previous, trick_size=2, trick_count_needed=1, trick_name='pair', group_key_fn=get_card_value)


def two_pair(previous):
    return find_trick(previous, trick_size=2, trick_count_needed=2, trick_name='two pair', group_key_fn=get_card_value)


def three_of_a_kind(previous):
    return find_trick(previous, trick_size=3, trick_count_needed=1, trick_name='three-of-a-kind', group_key_fn=get_card_value)


def four_of_a_kind(previous):
    return find_trick(previous, trick_size=4, trick_count_needed=1, trick_name='four-of-a-kind', group_key_fn=get_card_value)


def flush(previous):
    return find_trick(previous, trick_size=5, trick_count_needed=1, trick_name='flush', group_key_fn=get_card_suit)


@pipes
def hand(hole_cards, community_cards):
    print()
    cards = hole_cards + community_cards
    sorted_cards = sort_cards_by_value(cards)
    cards_and_best_hand = nothing(sorted_cards) >> pair >> two_pair >> three_of_a_kind >> four_of_a_kind >> flush
    return cards_and_best_hand[1]

