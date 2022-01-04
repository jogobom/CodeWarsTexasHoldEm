from itertools import groupby

def nothing(cards):
    return cards, ('nothing', [get_card_value(c) for c in cards[:5]])

def get_card_value(card):
    return card[0:-1]

def group_by_value(indexed_card):
    card = indexed_card[1]
    return get_card_value(card)

def group_by_suit(indexed_card):
    card = indexed_card[1]
    return card[-1]

def group_consecutive(indexed_card):
    index = indexed_card[0]
    card = indexed_card[1]
    priorities = get_card_priorities()
    return priorities[get_card_value(card)] - index

def group_consecutive_and_suit(indexed_card):
    return str(group_consecutive(indexed_card)) + group_by_suit(indexed_card)

def get_card_priorities():
    card_order = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    return {card_order[i]: i for i in range(len(card_order))}    

def sort_cards_by_value(cards, value_getter=get_card_value):
    priorities = get_card_priorities()
    return sorted(cards, key=lambda c: priorities[value_getter(c)])

def generate_trick_parts(trick_parts_needed, cards, group_key_fn):
    grouped_cards = [[c[1] for c in list(g[1])] for g in groupby(enumerate(cards), key=group_key_fn)]
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
    return find_trick(previous, trick_parts_needed=[2], trick_name='pair', group_key_fn=group_by_value)

def two_pair(previous):
    return find_trick(previous, trick_parts_needed=[2, 2], trick_name='two pair', group_key_fn=group_by_value)

def three_of_a_kind(previous):
    return find_trick(previous, trick_parts_needed=[3], trick_name='three-of-a-kind', group_key_fn=group_by_value)

def four_of_a_kind(previous):
    return find_trick(previous, trick_parts_needed=[4], trick_name='four-of-a-kind', group_key_fn=group_by_value)

def flush(previous):
    return find_trick(previous, trick_parts_needed=[5], trick_name='flush', group_key_fn=group_by_suit)

def straight(previous):
    return find_trick(previous, trick_parts_needed=[5], trick_name='straight', group_key_fn=group_consecutive)

def straight_flush(previous):
    return find_trick(previous, trick_parts_needed=[5], trick_name='straight-flush', group_key_fn=group_consecutive_and_suit)

def full_house(previous):
    return find_trick(previous, trick_parts_needed=[3, 2], trick_name='full house', group_key_fn=group_by_value)

def hand(hole_cards, community_cards):
    print()
    cards = hole_cards + community_cards
    sorted_cards = sort_cards_by_value(cards)
    cards_and_best_hand = straight_flush(four_of_a_kind(full_house(flush(straight(three_of_a_kind(two_pair(pair(nothing(sorted_cards)))))))))
    return cards_and_best_hand[1]
