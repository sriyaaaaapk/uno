import random
#card setup
colors = ['Red', 'Yellow', 'Green', 'Blue'] # All the possible card colours
specials = ['Skip', 'Reverse', 'Draw Two']  # Colorued special cards
wilds = ['Wild', 'Wild Draw Four']          # Colourless wild cards
numbers = list(range(0, 10))  #cards range from 0 to 9

#making a deck
def create_deck():
    deck = []
    for color in colors:
        deck.append(f'{color} 0') #one zero per colour
        for num in range(1, 10):
            deck.extend([f'{color} {num}'] * 2) #two of each number 
        for special in specials:
            deck.extend([f'{color} {special}'] * 2) #two of special card
    for wild in wilds:
        deck.extend([wild] * 4)
    random.shuffle(deck)
    return deck

#player gets 7 cards
def deal_cards(deck, num_players=2, cards_per_player=7):
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_player):
        for hand in hands:
            hand.append(deck.pop())
    return hands

#turns cards into a NUMBERED list
def show_hand(hand):
    return '\n'.join(f"{idx+1}: {card}" for idx, card in enumerate(hand))

#allowsyou to get colour of the card
def get_color(card):
    if card.startswith('Wild'):
        return None
    return card.split(' ')[0]

#allows you to get value of a card
def get_value(card):
    if card.startswith('Wild'):
        return card  # Wild or Wild Draw Four
    return ' '.join(card.split(' ')[1:])

#checks if the card can be played
def can_play(card, top_card, current_color):
    # Wilds can always be played
    if card.startswith('Wild'):
        return True
    card_color = get_color(card)
    card_value = get_value(card)
    top_value = get_value(top_card)
    # Check if color matches current color or value matches top card value
    return card_color == current_color or card_value == top_value

#choose colour when wild card is played
def choose_color():
    while True:
        color = input("Choose a color (Red, Yellow, Green, Blue): ").capitalize()
        if color in colors:
            return color
        else:
            print("Invalid color choice. Try again.")

 # Shows current hand, checks which cards are playable, lets player pick a card or draw
 # If a Wild is played, asks for a colour
 # Returns: the card played (or None), the new current colour, and the updated deck
def player_turn(player_num, player_hand, top_card, deck, current_color):
    print(f"\nPlayer {player_num + 1}'s turn.")
    print(f"Top card on discard pile: {top_card} (Current color: {current_color})")
    print("Your hand:")
    print(show_hand(player_hand))

    playable_indices = [i for i, card in enumerate(player_hand) if can_play(card, top_card, current_color)]
    if playable_indices:
        while True:
            choice = input("Choose a card number to play or 'd' to draw a card: ").strip()
            if choice.lower() == 'd':
                if deck:
                    drawn_card = deck.pop()
                    player_hand.append(drawn_card)
                    print(f"You drew: {drawn_card}")
                    if can_play(drawn_card, top_card, current_color):
                        play_after_draw = input("Play the drawn card? (y/n): ").strip().lower()
                        if play_after_draw == 'y':
                            player_hand.pop()
                            return drawn_card, current_color, deck
                    return None, current_color, deck
                else:
                    print("Deck is empty, cannot draw.")
                    return None, current_color, deck
            elif choice.isdigit():
                idx = int(choice) - 1
                if idx in playable_indices:
                    played_card = player_hand.pop(idx)
                    print(f"You played: {played_card}")

                    # Handle wild cards - choose color
                    if played_card.startswith('Wild'):
                        new_color = choose_color()
                        print(f"Color changed to {new_color}")
                        return played_card, new_color, deck
                    else:
                        # Normal card played - update color
                        new_color = get_color(played_card)
                        return played_card, new_color, deck
                else:
                    print("That card can't be played. Choose a playable card or draw.")
            else:
                print("Invalid input. Enter the card number or 'd' to draw.")
    else:
        print("No playable cards, you must draw.")
        if deck:
            drawn_card = deck.pop()
            player_hand.append(drawn_card)
            print(f"You drew: {drawn_card}")
            if can_play(drawn_card, top_card, current_color):
                play_after_draw = input("Play the drawn card? (y/n): ").strip().lower()
                if play_after_draw == 'y':
                    player_hand.pop()
                    # Handle wild drawn card
                    if drawn_card.startswith('Wild'):
                        new_color = choose_color()
                        print(f"Color changed to {new_color}")
                        return drawn_card, new_color, deck
                    else:
                        return drawn_card, get_color(drawn_card), deck
            return None, current_color, deck
        else:
            print("Deck empty, no cards to draw.")
            return None, current_color, deck

#win check
def check_winner(player_hand, player_num):
    if len(player_hand) == 0:
        print(f"\nPlayer {player_num + 1} wins! 🎉")
        return True
    return False

def main():
    deck = create_deck() #full UNO deck
    players = deal_cards(deck) #deal 7 cards each
    discard_pile = [deck.pop()] #puts first card to start the game
    current_color = get_color(discard_pile[-1])
    print(f"Starting card: {discard_pile[-1]} (Color: {current_color})")

    current_player = 0 #player 1 starts
    direction = 1 #use in reverse card
    skip_next = False
    draw_cards = 0

    while True:
        # Skipping logic
        # Handling Draw Two or Wild Draw Four
        # Call player_turn()
        # Handle played card effects (Skip, Reverse, Draw Two, Wild Draw Four)
        # Check if player won
        # Switch to next player
        if skip_next:
            print(f"Player {current_player + 1}'s turn is skipped!")
            skip_next = False
            current_player = (current_player + direction) % 2
            continue

        # If player must draw cards due to Draw Two or Wild Draw Four
        if draw_cards > 0:
            print(f"Player {current_player + 1} must draw {draw_cards} cards!")
            for _ in range(draw_cards):
                if deck:
                    players[current_player].append(deck.pop())
                else:
                    print("Deck empty, cannot draw more cards.")
            draw_cards = 0
            current_player = (current_player + direction) % 2
            continue

        played_card, new_color, deck = player_turn(current_player, players[current_player], discard_pile[-1], deck, current_color)

        if played_card:
            discard_pile.append(played_card)
            current_color = new_color

            value = get_value(played_card)

            # Handle special cards
            if value == 'Skip':
                skip_next = True
            elif value == 'Reverse':
                direction *= -1
                # With 2 players reverse acts like skip
                if len(players) == 2:
                    skip_next = True
            elif value == 'Draw Two':
                draw_cards = 2
                skip_next = True
            elif value == 'Wild Draw Four':
                draw_cards = 4
                skip_next = True
            # Wild just changes color, no extra effect

            if check_winner(players[current_player], current_player):
                break
        else:
            # No card played, keep current color
            pass

        current_player = (current_player + direction) % 2

if __name__ == "__main__":
    main()
