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


def print_hand(player, hide_one_card=False):
    print("\nYour hand:" if player.name ==
          human.name else "\nTHE DEALER's hand:")
    if hide_one_card == True:
        print(f"{player.hand[0]}"
              "\nThe other card is faced down."
              f"\nTotal value: {player.hand[0].value} + ??")
    else:
        for card in player.hand:
            print(card)
        print(f"Total value: {player.hand_value()}")


def deal_cards(n):
    for i in range(n):
        human.hit(deck)
        dealer.hit(deck)


def play_again(ask):
    output = {"y": True, "n": False}
    answer = input(f'{ask}').lower()
    while answer not in ["y", "n"]:
        answer = input(
            "\nI didn't get it. Type Y if the answer is YES and N if the answer is NO: ").lower()
    return output[answer]


def reinit_and_shuffle_deck():
    deck.__init__()
    deck.shuffle()


def empty_hands():
    human.hand = []
    dealer.hand = []


# Game Setup
print("\n\nFirst of all, what's your name?")
human = Player(input('\nEnter your name: ').upper())
dealer = Player("THE DEALER")

deck = Deck()
deck.shuffle()

print(f"\n{human.name}! What a nice name! OK, let's start right away.")
input('\n[Press Enter to continue]')

# Game on
games = 0

while True:
    # check if no more money or cards:
    if human.bankroll == 0:
        print("\nNo more money to bet! Game over!"
              f"\n\nYou ended up with ${human.bankroll}. You should sell your car and play again.\n")

        if not play_again(ask='Do you want to play again? Y/N: '):
            print(
                "\n\n\nAre you sure you want to quit? What if next time it went better?\n")
            break
        human.bankroll = 75 - games * games
        reinit_and_shuffle_deck()
        empty_hands()
        games += 1

        if human.bankroll < 1:
            print("\n\nNo more money to bet! Game over!\n")
            if not play_again(ask='Would you be interested in selling one of your organs in order to keep playing? Y/N: '):
                print(
                    "\nIt's understandable. After all, keeping our organs in their place allow us to continue gambling, right?\n")
                break
            human.bankroll = 1000
            reinit_and_shuffle_deck()
            empty_hands()
            games += 1
            print(
                f"\nYou sold one of your organs and now you have ${human.bankroll}. Excelent decision, congratulations!")
            input("\n[Press Enter to continue]")

    if len(deck.cards) < 13:
        print("\nNot enough cards to play!")
        if not play_again(ask='Shuffle and deal again? Y/N: '):
            print(
                "\nBetting money that you don't have can always end up being a good thing. Good bye!")
            break
        reinit_and_shuffle_deck()
        empty_hands()
        games += 1

    # placing the bet
    bet = 0
    betting = True
    while betting:
        try:
            bet = int(
                input(f"\nYou have ${human.bankroll}. Type the amount yo want to bet: "))
        except:
            print("\nSorry, I only accept numbers.")
        if bet > 0 and bet <= human.bankroll:
            break
        else:
            print(
                f"\nYou must place a bet higher than $0 and lower than or equal to ${human.bankroll}.")

    print(f'\nYour bet is ${bet}.')

    # round on
    round_on = True
    round_result = "..."

    # card dealing
    deal_cards(2)
    print_hand(human)
    input("\n[Press Enter to see THE DEALER's hand]")
    print_hand(dealer, hide_one_card=True)

   # human's turn
    while round_on:

        if human.hand_value() > 21:
            print("\nYou busted! THE DEALER wins this one.")
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
            print("\nTHE DEALER's turn.")
            break

    input("\n[Press Enter to continue]")

    # dealer's turn
    while round_on:
        print("\nTHE DEALER revealed his faced down card.")
        print_hand(dealer)

        input("\n[Press Enter to continue]")

        while dealer.hand_value() < 17:
            dealer.hit(deck)
            print(
                f"\nTHE DEALER drew another card. It's the {dealer.hand[-1]}.")
            print_hand(dealer)

            if dealer.hand_value() > 21:
                print(f"\nTHE DEALER busted! {human.name} WINS!")
                round_result = "human wins"
                round_on = False
                break
            input("\n[Press Enter to continue]")
        break

    # compare hands
    if round_on:
        if human.hand_value() > dealer.hand_value():
            print(f"\n{human.name} WINS!")
            round_result = "human wins"
            input("\n[Press Enter to continue]")
        elif human.hand_value() < dealer.hand_value():
            print("\nTHE DEALER WINS!")
            round_result = "dealer wins"
            input("\n[Press Enter to continue]")
        else:
            print("\nIt's a TIE!")
            round_result = "tie"
            input("\n[Press Enter to continue]")

    # collect bet
    if round_result == "human wins":
        human.add_money(bet)
    elif round_result == "dealer wins":
        human.remove_money(bet)

    # empty player hands
    empty_hands()
