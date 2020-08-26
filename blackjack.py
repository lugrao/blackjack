import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def __str__(self):
        cards = ""
        for card in self.cards:
            cards += str(card) + "\n"
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()


class Player:

    def __init__(self, name):
        self.name = name
        self.bankroll = 100
        self.hand = []

    def add_money(self, amount):
        self.bankroll += amount

    def remove_money(self, amount):
        if amount > self.bankroll:
            return "Not enough money!"
        self.bankroll -= amount

    def hit(self, deck):
        self.hand.append(deck.deal_one())

    def hand_value(self):
        aces_count = 0
        total_sum = 0
        for card in self.hand:
            if card.value != 11:
                total_sum += card.value
            else:
                aces_count += 1

        if aces_count > 0:
            for i in range(aces_count):
                if total_sum + 11 <= 21:
                    total_sum += 11
                else:
                    total_sum += 1
        return total_sum


def print_hand(player, round=""):
    print("\nYour hand:" if player.name == "HUMAN" else "\nDealer's hand:")
    if player.name == "DEALER" and round == "1st":
        print(f"{dealer.hand[0]}"
              "\nThe other card is faced down."
              f"\nTotal value: {dealer.hand[0].value} + ??")
    else:
        for card in player.hand:
            print(card)
        print(f"Total value: {player.hand_value()}")


def deal_cards(n):
    for i in range(n):
        human.hit(deck)
        dealer.hit(deck)


# Game Setup
human = Player("HUMAN")
dealer = Player("DEALER")

deck = Deck()
deck.shuffle()

# Game on
while True:

    # check if no more money or cards:
    if human.bankroll == 0:
        print("\nNo more money to bet! Game over!"
              f"\nYou ended up with ${human.bankroll}. You should sell your car and play again.")
        break
    if len(deck.cards) < 10:
        print("\nNot enough cards to play, the game is over!!"
              f"\nYou ended up with ${human.bankroll}. Remember to keep gambling no matter what.")
        break

    # placing the bet
    bet = 0
    print(f'\n\nYou have up to ${human.bankroll} to bet.')
    betting = True
    while betting:
        try:
            bet = int(input("Type the amount yo want to bet: "))
        except:
            print("\nSorry, I only accept numbers.")
        if bet > 0 and bet <= human.bankroll:
            break
        else:
            print(
                f"\nYou must place a bet higher than $0 and lower than or equal to ${human.bankroll}.")

    print(f'Your bet is ${bet}.')

    # hand on
    round_on = True
    round_result = "..."

    # card dealing
    deal_cards(2)
    print_hand(human)
    print_hand(dealer, round="1st")

   # human's turn
    while round_on:

        if human.hand_value() > 21:
            print("\nYou busted! Dealer wins this one.")
            round_result = "dealer wins"
            round_on = False
            break

        if human.hand_value() == 21:
            break

        next_move = ""
        while next_move not in ["hit", "stay"]:
            next_move = input(
                "\nIf you want to draw another card, type HIT. If you don't, type STAY: ").lower()

        if next_move == "hit":
            human.hit(deck)
            print_hand(human)

        if next_move == "stay":
            print("\nDealer's turn.")
            break

    input("\n[Enter to continue]")

    # dealer's turn
    while round_on:
        print("\nThe Dealer revealed his faced down card.")
        print_hand(dealer)

        input("\n[Enter to continue]")

        while dealer.hand_value() < human.hand_value():
            dealer.hit(deck)
            print(
                f"\nThe Dealer drew another card. It's the {dealer.hand[-1]}.")
            print_hand(dealer)

            if dealer.hand_value() > 21:
                print("\nThe Dealer busted! HUMAN WINS!!")
                round_result = "human wins"
                round_on = False
                break
            input("\n[Enter to continue]")
        break

    # compare hands
    if round_on:
        if human.hand_value() > dealer.hand_value():
            print("\nHUMAN WINS!")
            round_result = "human wins"
        elif human.hand_value() < dealer.hand_value():
            print("\nDEALER WINS!")
            round_result = "dealer wins"
        else:
            print("\nIt's a TIE!")
            round_result = "tie"

    # collect bet
    if round_result == "human wins":
        human.add_money(bet)
    elif round_result == "dealer wins":
        human.remove_money(bet)

    # empty player hands
    human.hand = []
    dealer.hand = []
