import random

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    # my classical for-loops solution:
    # hands = []
    # for i in range(numhands):
    #     hand = []
    #     for j in range(n):
    #         card = random.choice(deck)
    #         hand.append(card)
    #         deck.remove(card)
    #     hands.append(hand)
    # return hands
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    # my option with list comprehension
    # return [hand for hand in iterable if hand_rank(hand) == hand_rank(max(iterable, key=hand_rank))]
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

def hand_rank(hand):
    "Return a value indicating the ranking of a hand"
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))                     # 2 3 4 5 6 -> (8, 6); 6 7 8 9 T -> (8, 10)
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks)) # 9 9 9 9 3 -> (7, 9, 3)
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    # alternative options: dict lookup or bruteforce if-else
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

# My option:
# def straight(ranks):
#     "Return True if the ordered ranks form a 5-card straight."
#     count = 1
#     while count < len(ranks):
#         if ranks[count] != ranks[count-1] - 1:
#             return False
#         count += 1
#     return True

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

# My option:
# def flush(hand):
#     "Return True if all the cards have the same suit."
#     count = 1
#     while count < len(hand):
#         if hand[count][-1] != hand[count-1][-1]:
#             return False
#         count += 1
#     return True

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None

def two_pair(ranks):
    first = 0
    second = 0
    for r in ranks:
        if ranks.count(r) == 2 and r != first:
            if not first: first = r
            else: second = r
    if first and second:
        return (first, second)
    return None

def hand_percentages(n=70*1000):
    "Sample n random hands and print a table of percentages for each type of hand."
    counts = [0] * 9
    for i in range(int(n/10)):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print("%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n))

hand_names = [
    "High Card",
    "Pair",
    "2 Pair",
    "3 Kind",
    "Straight",
    "Flush",
    "Full House",
    "4 Kind",
    "Straight Flush",
]

hand_percentages()

def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # straight flush  
    sf2 = "6D 7D 8D 9D TD".split() # straight flush equal to sf1
    fk = "9D 9H 9S 9C 7D".split() # four of a kind
    fh = "TD TC TH 7C 7D".split() # full house
    tp = "5S 5D 9H 9C 6S".split() # two pairs
    s1 = "AS 2S 3S 4S 5S".split() # A-5 straight
    s2 = "2C 3C 4C 5C 6C".split() # 2-6 straight
    ah = "AS 2S 3S 4S 6C".split() # A high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    assert poker([s1, s2, ah, sh]) == [s2]
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf1) == True
    assert flush(fk) == False
    assert kind(4,fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)
    assert card_ranks(sf1) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert poker([sf1, fk, fh]) == [sf1]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf1]) == [sf1]
    assert poker([sf1] + 99*[fh]) == [sf1]
    assert hand_rank(sf1) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return "tests pass"

print(test())

# print(max([3, 4, 5, 0]), max([3, 4, -5, 0], key=abs)) # 5, -5