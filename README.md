# CISC-121-Project
My CISC-121 final project. This is a Python app that showcases how insertion sort works on a deck of cards.

**Decomposition: What smaller steps form your chosen algorithm?**

Insertion Sort:
  - First element is assumed to be sorted, take the second index as the starting target value
  - Backwards linear search from the target value index
  - Insertion of the target value at the correct spot
  - In a deck of cards, the suits is to be sorted first, then values must be sorted within each suit

**Pattern Recognition: How does it repeatedly reach, compare, or swap values?**
- The first element is assumed to be sorted, so the next value is assigned to the target value.
- Backwards linear search is performed to compare the target value to the rest of the list to the left
- The target value is inserted when the searching index reaches a value less than or equal to the target value, shifting over the rest of the list to the right
- Both suits and values are sorted the same way, but values must have special bounds within its original list for each suit

**Abstraction: Which details of the process should be shown to the user and how to show it, and which details should be discarded (i.e., not shown)?**
- When sorting the suits, we pay attention to only the suit. We can worry about sorting the values after all the suits are grouped accordingly
- When sorting the values, sublist constraints must be placed so the algorithm knows the bounds of the sorting
- Since a standard deck of cards contains 4 suits and 13 cards per suit, the typical length of the deck is 52 cards, so sublist bounds can be hardcoded
- Colour coding each index accordingly, red for target, green for search, and blue for the area between the target and search index. Also orange to mark sublists

**Algorithm Design: How will input → processing → output flow to and from the user?
Including the use of the graphical user interface (GUI).**
- All input is done through buttons and sliders. Buttons are used to shuffle and alter the deck, while sliders go through the steps of sorting the list
- The user may not enter any of their own values, as Gradio raised errors are not possible to circumvent, even the textbox in the slider is removed to prevent the app from crashing when the user tries to enter steps outside of its range
