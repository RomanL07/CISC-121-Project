# CISC-121-Project
My CISC-121 final project. This is a Python app that showcases how insertion sort works on a deck of cards.

# Insertion Sort:
Flowchart of sorting a deck using insertion sort:
<img width="732" height="1012" alt="Deck Sorting" src="https://github.com/user-attachments/assets/e5057697-c06f-45e6-a84e-52e6b7caa1d6" />

## **Decomposition: What smaller steps form your chosen algorithm?**
  - First element is assumed to be sorted, take the second index as the starting target value
  - Backwards linear search from the target value index
  - Insertion of the target value at the correct spot
  - In a deck of cards, the suits is to be sorted first, then values must be sorted within each suit

## **Pattern Recognition: How does it repeatedly reach, compare, or swap values?**
- The first element is assumed to be sorted, so the next value is assigned to the target value.
- Backwards linear search is performed to compare the target value to the rest of the list to the left
- The target value is inserted when the searching index reaches a value less than or equal to the target value, shifting over the rest of the list to the right
- Both suits and values are sorted the same way, but values must have special bounds within its original list for each suit

## **Abstraction: Which details of the process should be shown to the user and how to show it, and which details should be discarded (i.e., not shown)?**
- When sorting the suits, we pay attention to only the suit. We can worry about sorting the values after all the suits are grouped accordingly
- When sorting the values, sublist constraints must be placed so the algorithm knows the bounds of the sorting
- Since a standard deck of cards contains 4 suits and 13 cards per suit, the typical length of the deck is 52 cards, so sublist bounds can be hardcoded
- Colour coding each index accordingly, red for target, green for search, and blue for the area between the target and search index. Also orange to mark sublists

## **Algorithm Design: How will input → processing → output flow to and from the user?
Including the use of the graphical user interface (GUI).**
- All input is done through buttons and sliders. Buttons are used to shuffle and alter the deck, while sliders go through the steps of sorting the list
- The user may not enter any of their own values, as Gradio raised errors are not possible to circumvent, even the textbox in the slider is removed to prevent the app from crashing when the user tries to enter steps outside of its range

## Steps to Run
1. Ensure Python version 3 is installed. Project was made on Python version 3.14
2. Install newest Gradio package. Projcet was made on Gradio version 6.0.2
3. Run app.py. as deck.py is a module that app.py depends on to run
4. app.py can be run locally or on huggingface

## Hugging Face Link

https://huggingface.co/spaces/CSM2/CISC121_Project

## Author & Acknowledgment
**Roman Labuda**: Author of the project
