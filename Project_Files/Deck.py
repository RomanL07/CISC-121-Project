import random as rand

#Handles the information inside each card, not intended to be accessed directly, but meant to be handled through the deck class
class Card:
    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def get_suit(self) -> int:
        '''Returns the numerical value of the card's suit'''
        return self.suit
    
    def get_suit_name(self) -> str:
        '''Returns the string representation of the card's suit value'''
        suit_match = {
            0: "X",
            1: "S",
            2: "C",
            3: "H",
            4: "D"
        }
        return suit_match.get(self.suit)
    
    def get_value_name(self) -> str:
        '''Returns the string representation of the card's face value'''
        value_match = {
            0: "X",
            1: "A",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K"
        }
        return value_match.get(self.value)
        
    def get_value(self) -> int:
        '''Returns the numerical value of the card's face value'''
        return self.value

    def __str__(self) -> str:
        '''Returns a string readable version of the card's properties'''
        return(f"{self.get_value_name()}{self.get_suit_name()}")

    def __repr__(self) -> str:
        '''Returns a string readable version of the card's properties'''

        return self.__str__()

#Handles a list of card objects
class deck:
    suits = (1, 2, 3, 4)
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    def __init__(self):
        self.cards = []

    def generate_deck(self) -> None:
        '''Generates a full deck of cards already sorted'''
        for s in deck.suits:
            for v in deck.values:
                self.cards.append(Card(v, s))
    
    def generate_suits(self) -> None:
        '''Generates a full deck of cards but leaves values undeteremined with an "X"'''
        for s in deck.suits:
            for v in deck.values:
                self.cards.append(Card(0, s))

    def generate_values(self) -> None:
        '''Generates a deck of cards with only 1 suit, but the suit is left undetermined with "X"'''
        for v in deck.values:
            self.cards.append(Card(v, 0))

    def get_deck(self) -> list:
        '''Returns the list of the deck'''
        return self.cards
    
    def display_deck(self) -> list:
        '''Returns a string readable list of cards'''
        return [i for i in self.cards]

    def shuffle_deck(self) -> None:
        '''Shuffles the deck'''
        rand.shuffle(self.cards)

    def sort_suits(self) -> None:
        '''Sorts deck by suit, with priority from least to greatest: Spades, Clubs, Hearts, Diamonds'''
        length=len(self.cards)
        i=1
        while i<length:
            target=self.cards[i]
            target_val = target.get_suit()
            back_search=i-1
            while back_search>=0 and target_val<self.cards[back_search].get_suit():
                back_search-=1
            self.cards.insert(back_search+1, target)
            self.cards.pop(i+1)
            i+=1

    def sort_values(self) -> None:
        '''Sorts deck by value, will create complications if run without sorting suits first'''
        i=1
        suit_length = len(self.cards)//4
        length = suit_length
        for j in range(4):
            while i<length:
                target=self.cards[i]
                target_val = target.get_value()
                back_search=i-1
                while back_search>=0 and target_val<self.cards[back_search].get_value() and target.get_suit()==self.cards[back_search].get_suit():
                    back_search-=1
                self.cards.insert(back_search+1, target)
                self.cards.pop(i+1)
                i+=1
            length+=suit_length

    def is_deck_sorted(self) -> bool:
        '''Checks if the deck is sorted, returns False if the deck is not sorted'''
        x=0
        for i in self.suits:
            for j in self.values:
                if self.cards[x].get_suit()!=i and self.cards[x].get_value()!=j:
                    return False
                x+=1
        return True
    
    def clear(self) -> None:
        '''Empties the deck of cards'''
        self.cards.clear()

    def get_card(self, i) -> Card:
        '''Returns the card in the deck at a given index'''

        if not isinstance(i, int):
            return TypeError("index 'i' must be non-negative integer")
        
        if i<0 or i>len(self.cards):
            return IndexError("index 'i' is out of range of deck length")
        return self.cards[i]
