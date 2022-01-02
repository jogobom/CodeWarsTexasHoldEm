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


def generate_trick_parts(trick_parts_needed, cards, group_key_fn):
    grouped_cards = [list(g[1]) for g in groupby(cards, key=group_key_fn)]
    try:
        for required_trick_length in trick_parts_needed:
            trick_part_found = next(filter(lambda g: len(g) >= required_trick_length, grouped_cards))
            grouped_cards.remove(trick_part_found)
            yield trick_part_found[:required_trick_length]
    except StopIteration:
        return


def find_trick(previous, trick_parts_needed, trick_name, group_key_fn):
    cards = previous[0]
    trick_parts_found = list(generate_trick_parts(trick_parts_needed, cards, group_key_fn))
    if [len(found) for found in trick_parts_found] == trick_parts_needed:
        return fill_hand(cards, trick_name, trick_parts_found)
    return previous


def card_values_to_retain_from_trick(trick):
    return sort_cards_by_value(list(set([get_card_value(t) for t in trick])), value_getter=lambda c: c)


def fill_hand(cards, trick_name, trick_parts_found):
    flattened_tricks = [c for trick in trick_parts_found for c in trick]
    cards_not_included_in_trick = list(filter(lambda c: c not in flattened_tricks, cards))
    number_of_cards_to_fill_hand = 5 - len(flattened_tricks)
    return cards, (trick_name,
                   [*[c for t in trick_parts_found for c in card_values_to_retain_from_trick(t)],
                    *[get_card_value(c) for c in cards_not_included_in_trick][:number_of_cards_to_fill_hand]])


def pair(previous):
    return find_trick(previous, trick_parts_needed=[2], trick_name='pair', group_key_fn=get_card_value)


def two_pair(previous):
    return find_trick(previous, trick_parts_needed=[2, 2], trick_name='two pair', group_key_fn=get_card_value)


def three_of_a_kind(previous):
    return find_trick(previous, trick_parts_needed=[3], trick_name='three-of-a-kind', group_key_fn=get_card_value)


def four_of_a_kind(previous):
    return find_trick(previous, trick_parts_needed=[4], trick_name='four-of-a-kind', group_key_fn=get_card_value)


def flush(previous):
    return find_trick(previous, trick_parts_needed=[5], trick_name='flush', group_key_fn=get_card_suit)


# def straight(previous):
#     return find_trick(previous, trick_parts_needed=[5], trick_name='straight', group_key_fn=get_card_suit)


def full_house(previous):
    return find_trick(previous, trick_parts_needed=[3, 2], trick_name='full house', group_key_fn=get_card_value)


@pipes
def hand(hole_cards, community_cards):
    print()
    cards = hole_cards + community_cards
    sorted_cards = sort_cards_by_value(cards)
    cards_and_best_hand = nothing(sorted_cards) >> pair >> two_pair >> three_of_a_kind >> flush >> full_house >> four_of_a_kind
    return cards_and_best_hand[1]
