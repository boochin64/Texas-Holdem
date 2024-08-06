import random
import time
from math import ceil
from statistics import mode

handsize = 5
n = "play"
rank_values = {'2': 2, 
               '3': 3, 
               '4': 4, 
               '5': 5, 
               '6': 6, 
               '7': 7, 
               '8': 8, 
               '9': 9, 
               '10': 10, 
               'Jack': 11, 
               'Queen': 12, 
               'King': 13, 
               'Ace': 14}
running_total = 0

class exitfunc(Exception):
  pass

class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank
    #initiates card
  def __repr__(self):
    return f'{self.rank} of {self.suit}'
    #returns card as string

class Hand:
  def __init__(self):
    self.cards = []
    #initiates hand
  def __repr__(self):
    return ', '.join(map(str, self.cards))
    #returns hand as string
  def draw_card(self, card):
    self.cards.append(card)
    #adds card to hand
  def draw(self, deck, number):
    for _ in range(number):
      self.draw_card(deck.pop())
    #draws card from deck
  def is_flush(self):
    suits = [card.suit for card in self.cards]
    return any(suits.count(i) >= 5 for i in suits)
    #checks if hand is a flush
  def flush_high_card(self):
    x = None
    suits = [card.suit for card in self.cards]
    temp_cards = self.cards
    for suit in suits:
      if suits.count(suit) >= 5:
        x = suit
    for card in temp_cards:
      if card.suit != x:
        temp_cards.remove(card)
    ranks = sorted(rank_values[card.rank] for card in temp_cards)
    ranks.reverse()
    return ranks
    #returns the flush in order of rank
  def is_straight(self):
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    unique_ranks = sorted(set(ranks))
    for i in range(len(unique_ranks) - 4):
      if unique_ranks[i+4] - unique_ranks[i] == 4:
        return True
    if {14, 2, 3, 4, 5}.issubset(set(ranks)):
      return True
    return False
    #checks if hand is a straight
  def straight_high_card(self):
    list = []
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    unique_ranks = sorted(set(ranks))
    unique_ranks.reverse()
    if {14, 2, 3, 4, 5}.issubset(set(ranks)):
      list = [14, 5, 4, 3, 2]
      return list
    for i in unique_ranks:
      for j in range(5):
        if i-j in unique_ranks:
          list.append(i-j)
        else:
          list = []
          break
      if list:
        return list
    return list
    #returns the straight in order of rank
  def is_royal(self):
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    if {10, 11, 12, 13, 14}.issubset(set(ranks)):
      return True
    return False
    #checks if hand is royal
  def card_count(self):
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    pairs = []
    while ranks:
      pairs.append(ranks.count(ranks[0]))
      ranks[:] = (value for value in ranks if value != ranks[0])
    return pairs
    #returns the number of each card in hand
  def high_card_count(self):
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    ranks.reverse()
    pairs = []
    while ranks:
      pairs.append(mode(ranks))
      ranks[:] = (value for value in ranks if value != mode(ranks))
    return pairs
    #returns the value of each card in hand by order of frequency
  def get_score(self):
    score = 0
    if self.is_straight() and self.is_flush() and self.is_royal():
      score = 9
    elif self.is_flush() and self.is_straight():
      score = 8
    elif any(number >= 4 for number in self.card_count()):
      score = 7
    elif 3 in self.card_count() and 2 in self.card_count():
      score = 6
    elif self.is_flush():
      score = 5
    elif self.is_straight():
      score = 4
    elif 3 in self.card_count():
      score = 3
    elif self.card_count().count(2) == 2:
      score = 2
    elif 2 in self.card_count():
      score = 1
    return score
    #returns the score of the hand
  def high_card_score(self):
    global handsize
    score = []
    if self.is_straight() and self.is_flush() and self.is_royal():
      score = [14, 13, 12, 11, 10]
    elif self.is_flush() and self.is_straight():
      score = self.straight_high_card()
    elif any(number >= 4 for number in self.card_count()) \
    or 3 in self.card_count() and 2 in self.card_count():
      score = self.high_card_count()
      handsize = 2
    elif self.is_flush():
      score = self.flush_high_card()
    elif self.is_straight():
      score = self.straight_high_card()
    elif 3 in self.card_count() or self.card_count().count(2) == 2: 
      score = self.high_card_count()
      handsize = 3
    elif 2 in self.card_count():
      score = self.high_card_count()
      handsize = 4
    else:
      score = self.high_card_count()
    if score is None:
      score = []
    while len(score) > handsize:
      score.pop()
    return score
    #returns the score of hand in case of tie
  def print_score(self, i):
    hand_rankings = {
      9: 'Royal Flush',
      8: 'Straight Flush',
      7: 'Four of a Kind',
      6: 'Full House',
      5: 'Flush',
      4: 'Straight',
      3: 'Three of a Kind',
      2: 'Two Pair',
      1: 'Pair',
      0: f'High Card - {self.print_high_card(self.high_card())}'
    }
    return hand_rankings[i]
    #prints the score of hand
  def high_card(self):
    ranks = sorted(rank_values[card.rank] for card in self.cards)
    return ranks[-1]
    #returns the highest card in hand
  def print_high_card(self, i):
    ranks = {
      2: 'Two',
      3: 'Three',
      4: 'Four',
      5: 'Five',
      6: 'Six',
      7: 'Seven',
      8: 'Eight',
      9: 'Nine',
      10: 'Ten',
      11: 'Jack',
      12: 'Queen',
      13: 'King',
      14: 'Ace'
    }
    return ranks[i]
    #prints rank of card off number

def make_deck():
  suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
  ranks = ['2', '3', '4', '5', '6', '7' ,'8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
  deck = [Card(suit, rank) for suit in suits for rank in ranks]
  random.shuffle(deck)
  return deck
  #creates deck of cards
def betone(bet1, bet2, pocket2):
  global running_total
  print(f"Your bet: {bet1}")
  print(f"Opponent's bet: {bet2}")
  x = input()
  if x.isdigit():
    x = int(x)
    if x + bet1 < bet2:
      print("Insufficient")
      bet1 = betone(bet1, bet2, pocket2)
    else:
      bet1 += x
  elif x == "fold":
    print(f"Opponent had {pocket2}. You lose ${bet1}.")
    ai_talk("win", 100)
    running_total -= bet1
    raise exitfunc
  elif x == "check":
    if bet1 < bet2:
      print("Not possible right now")
      bet1 = betone(bet1, bet2, pocket2)
  elif x == "call":
    if bet1 >= bet2:
      print("Not possible right now")
      bet1 = betone(bet1, bet2, pocket2)
    else:
      bet1 = bet2
  elif x == "all in":
    bet1 = "all in"
  else:
    print("Invalid input")
    bet1 = betone(bet1, bet2, pocket2)
  return bet1
  #player bet
def bettwo(bet1, bet2, pocket2, board, total2):
  global running_total
  handscore = total2.get_score() - board.get_score()
  y = random.randint(0, 14)    
  if bet1 == "all in":
    if handscore == 0 and y <= 4:
      print(f"Opponent folds. They had {pocket2}. You win ${bet2}.")
      ai_talk("fold", 100)
      running_total += bet2
      raise exitfunc
    else:
      print(f"Opponent calls. They have {pocket2}.")
      ai_talk("all in", 100)
      ai_talk("trash", 10)
      bet2 = "all in"
      time.sleep(3)
  elif bet1 > bet2:
    if handscore == 0 and y <= 4 or bet1-bet2 >= bet2/1.2 and handscore == 0 and y <= 7:
      print(f"Opponent folds. They had {pocket2}. You win ${bet2}.")
      ai_talk("fold", 100)
      running_total += bet2
      raise exitfunc
    elif handscore >= 1 and y <= 4 or handscore >= 3 and y <= 9 or y <= 1:
      n = bet2 - bet1
      while bet2 <= bet1:
        e = ceil(bet1/random.randint(2, 6))
        bet2 += e
        n += e
      print(f"Opponent reraises {n} to {bet2}.")
      ai_talk("raise", 50)
      ai_talk("trash", 10)
    else:
      print("Opponent calls.")
      ai_talk("call", 20)
      ai_talk("trash", 10)
      bet2 = bet1
  else:
    if handscore >= 1 and y <= 7 or handscore >= 3 or y <= 1:
      if handscore >= 3 or y <= 1:
        e = ceil(bet1/random.randint(1, 3))
      else:  
        e = ceil(bet1/random.randint(2, 6))
      bet2 += e
      print(f"Opponent raises {e} to {bet2}.")
      ai_talk("raise", 50)
      ai_talk("trash", 10)
    else:
      print("Opponent checks.")
      ai_talk("check", 20)
      ai_talk("trash", 10)
  return bet2
  #betting ai
def ai_talk(type, chance):
  x = random.randint(0, 100)
  c = random.randint(0, 3)
  if x > chance:
    return
  if type == "call":
    if c == 0 or c == 1:
      print("\033[32mI think you're bluffing.\033[37m")
    else:
      print("\033[32mI'm confident.\033[37m")
  if type == "trash":
    if c == 0:
      print("\033[32mBe prepared to lose a lot of money.\033[37m")
    elif c == 1:
      print("\033[32mIt's too late to take that back you know.\033[37m")
    elif c == 2:
      print("\033[32mI knew you were going to do that.\033[37m")
    elif c == 3:
      print("\033[32mYou're going to make me rich.\033[37m")
  elif type == "raise":
    if c == 0:
      print("\033[32mI have something! ...Or do I?\033[37m")
    elif c == 1:
      print("\033[32mCall it. I dare you.\033[37m")
    elif c == 2:
      print("\033[32mIt might be best to fold...\033[37m")
    elif c == 3:
      print("\033[32mThat's a lot of money you know.\033[37m")
  elif type == "fold":
    if c == 0:
      print("\033[32mDamn.\033[37m")
    elif c == 1:
      print("\033[32mYeah I'm not doing that.\033[37m")
    elif c == 2:
      print("\033[32mIf you bluffed...\033[37m")
    elif c == 3:
      print("\033[32mIt was the safe choice.\033[37m")
  elif type == "check":
    if c == 0 or c == 1:
      print("\033[32mNothing to see here.\033[37m")
    elif c == 2 or c== 3:
      print("\033[32mI'm playing it safe.\033[37m")
  elif type == "win":
    if c == 0:
      print("\033[32mHa!\033[37m")
    elif c == 1:
      print("\033[32mTry harder next time I guess :/\033[37m")
    elif c == 2:
      print("\033[32mYou're not very good at this are you?\033[37m")
    elif c == 3:
      print("\033[32mOooooh... that money is mine now.\033[37m")
  elif type == "lose":
    if c == 0:
      print("\033[32mDang.\033[37m")
    elif c == 1:
      print("\033[32mSo close!\033[37m")
    elif c == 2:
      print("\033[32mI think you dealt these cards wrong.\033[37m")
    elif c == 3:
      print("\033[32mI can't prove you cheated, but you did.\033[37m")
  elif type == "all in":
    if c == 0:
      print("\033[32mBold move.\033[37m")
    elif c == 1:
      print("\033[32mHuh.\033[37m")
    elif c == 2:
      print("\033[32mRisky...\033[37m")
    elif c == 3:
      print("\033[32mAre you sure?\033[37m")
  elif type == "tie":
    if c == 0:
      print("\033[32mWell played.\033[37m")
    elif c == 1:
      print("\033[32mI think I won that...\033[37m")
    elif c == 2:
      print("\033[32mLet's just say you lost.\033[37m")
    elif c == 3:
      print("\033[32mHuh.\033[37m")
  #ai voicelines
def start_game():
  global running_total
  deck = make_deck()
  pocket1 = Hand()
  board = Hand()
  total1 = Hand()
  pocket2 = Hand()
  total2 = Hand()
  pocket1.draw(deck, 2)
  pocket2.draw(deck, 2)
  bet1 = 10
  bet2 = 20
  print(f"Pocket: {pocket1}")
  if bet1 == "all in":
    time.sleep(3)
  else:
    bet1 = betone(bet1, bet2, pocket2)
    bet2 = bettwo(bet1, bet2, pocket2, board, pocket2)
    while bet1 != bet2:
      bet1 = betone(bet1, bet2, pocket2)
      if bet1 == bet2:
        break
      bet2 = bettwo(bet1, bet2, pocket2, board, pocket2)
  board.draw(deck, 3)
  total2.cards = pocket2.cards + board.cards
  print(f"\nFlop: {board}")
  if bet1 == "all in":
    time.sleep(3)
  else:
    bet1 = betone(bet1, bet2, pocket2)
    bet2 = bettwo(bet1, bet2, pocket2, board, total2)
    while bet1 != bet2:
      bet1 = betone(bet1, bet2, pocket2)
      if bet1 == bet2:
        break
      bet2 = bettwo(bet1, bet2, pocket2, board, total2)
  board.draw(deck, 1)
  total2.cards = pocket2.cards + board.cards
  print(f"\nTurn: {board}")
  if bet1 == "all in":
    time.sleep(3)
  else:
    bet1 = betone(bet1, bet2, pocket2)
    bet2 = bettwo(bet1, bet2, pocket2, board, total2)
    while bet1 != bet2:
      bet1 = betone(bet1, bet2, pocket2)
      if bet1 == bet2:
        break
      bet2 = bettwo(bet1, bet2, pocket2, board, total2)
  board.draw(deck, 1)
  total2.cards = pocket2.cards + board.cards
  print(f"\nRiver: {board}")
  if bet1 == "all in":
    time.sleep(3)
  else:
    bet1 = betone(bet1, bet2, pocket2)
    bet2 = bettwo(bet1, bet2, pocket2, board, total2)
    while bet1 != bet2:
      bet1 = betone(bet1, bet2, pocket2)
      if bet1 == bet2:
        break
      bet2 = bettwo(bet1, bet2, pocket2, board, total2)
    print(f"\nOpponent had: {pocket2}")
  total1.cards = pocket1.cards + board.cards
  print(f"You got: {total1.print_score(total1.get_score())}")
  print(f"Opponent got: {total2.print_score(total2.get_score())}")
  print("\n")
  if total1.get_score() > total2.get_score():
    if bet1 == "all in":
      print("You win it all.")
      ai_talk("lose", 100)
      running_total = "all win"
    else:
      print(f"You win ${bet2}.")
      ai_talk("lose", 100)
      running_total += int(bet2)
  elif total1.get_score() < total2.get_score():
    if bet1 == "all in":
      print("You lose it all.")
      ai_talk("win", 100)
      running_total = "all lose"
    else:
      print(f"You lose ${bet1}.")
      ai_talk("win", 100)
      running_total -= int(bet1)
  else:
    total1.high_card_score()
    for i in range(handsize):
      if total1.high_card_score()[i] > total2.high_card_score()[i]:
        if bet1 == "all in":
          print("You win it all.")
          ai_talk("lose", 100)
          running_total = "all win"
        else:
          print(f"You win ${bet2}.")
          ai_talk("lose", 100)
          running_total += int(bet2)
        raise exitfunc
      elif total1.high_card_score()[i] < total2.high_card_score()[i]:
        if bet1 == "all in":
          print("You lose it all.")
          ai_talk("win", 100)
          running_total = "all lose"
        else:
          print(f"You lose ${bet1}.")
          ai_talk("win", 100)
          running_total -= int(bet1)
        raise exitfunc
    print("Split pot.")
    ai_talk("tie", 100)
  #starts game
def start_game_call():
  try:
    start_game()
  except exitfunc:
    if running_total == "all win":
      print("You have won it all.")
      input("Enter to leave.")
      exit()
    elif running_total == "all lose":
      print("You have lost it all.")
      input("Enter to leave.")
      exit()
    print(f"You have ${running_total}.")
    n = input("Exit to leave and play to play again.\n")
    if n == "exit":
      exit()
    else:
      print("\n")
      start_game_call()

  if running_total == "all win":
    print("You have won it all.")
    input("Enter to leave.")
    exit()
  elif running_total == "all lose":
    print("You have lost it all.")
    input("Enter to leave.")
    exit()
  print(f"You have ${running_total}.")
  n = input("Exit to leave and play to play again.\n")
  if n == "exit":
    exit()
  else:
    print("\n")
    start_game_call()
  #recursively starts game

start_game_call()