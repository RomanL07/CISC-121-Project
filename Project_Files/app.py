import gradio as gr
import Deck as dk
import random as rand

#Demonstrates basics of insertion sort
ins_arr = []
#Show final product
d1 = dk.deck()
#Show how suits are sorted
d2 = dk.deck()
#Show how values are sorted
d3 = dk.deck()
#Show how the whole deck gets sorted
d4 = dk.deck()


def generate_arr(length: int=15) -> list:
    '''Generates a standard list of 15. Allows for implementation of variable size lists'''
    arr = []
    arr_length = length
    for i in range(arr_length):
        arr.append(rand.randint(1, 30))

    return arr

#Button Functions for first Block
def create_deck() -> list:
    '''Generates the cards of the deck under the Basic Deck Tab'''
    if len(d1.get_deck())!=0:
        return [d1.display_deck(), "Deck Already Created"]
    d1.generate_deck()
    return [d1.display_deck(), "Deck Generated"]

def clear_deck() -> list:
    '''Truncates the cards of the deck under the Basic Deck Tab'''

    if len(d1.get_deck())==0:
        return [d1.display_deck(), "Deck Already Cleared"]
    d1.clear()
    return [d1.display_deck(), "Deck Cleared"]

def shuffle_deck() -> list:
    '''Randomizes the positions of the cards of the deck under the Basic Deck Tab'''

    if len(d1.get_deck())==0:
        return [d1.display_deck(), "Deck is empty"]
    d1.shuffle_deck()
    return [d1.display_deck(), "Deck Shuffled"]

def sort_deck() -> list:
    '''Uses insertion sort to sort the cards by suit then value of the deck under the Basic Deck Tab'''

    if len(d1.get_deck())==0:
        return [d1.display_deck(), "Deck is empty"]
    if d1.is_deck_sorted():
        return [d1.display_deck(), "Deck Already Sorted"]
    d1.sort_suits()
    d1.sort_values()
    return [d1.display_deck(), "Deck Sorted"]

#AI Disclaimer: the html was created by AI, but added functionality for sublists when sorting the full deck in the final tab
def highlight_array_elements(arr: list, target_index: int, current_index: int=None, moved_index: int=None, sublist: list=None) -> str:
    """Create HTML with highlighted array elements"""
    html_elements = []
    if moved_index is None:
        moved_index = []
    if sublist is None:
        sublist = []
    for i, value in enumerate(arr):
        style = "padding: 8px 12px; margin: 2px; border-radius: 4px;"
        
        if i == target_index:
            style += "background-color: #ff6b6b; color: white; font-weight: bold;"  # Red for targets
        elif i == current_index:
            style += "background-color: #7fff6e; color: white;"  # Green for current
        elif i in moved_index:
            style += "background-color: #45b7d1; color: white;"  # Blue for searching range
        elif i in sublist:
            style += "background-color: #ffd663; color: white;"  # Orange for sublist range
        else:
            style += "background-color: #f8f9fa; color: #333; border: 1px solid #ddd;"
        
        html_elements.append(f'<span style="{style}">{value}</span>')
    
    return f'<div style="display: flex; flex-wrap: wrap;">{"".join(html_elements)}</div>'

#AI Disclaimer: The basic logic for updating HTML and properly working buttons was created by AI, but modified by me to work for each list
#Base logic for each tab has been copied over to match each object
def create_sorting_visualizer() -> gr.Blocks:
    '''Creates the entire interface of the program'''

    with gr.Blocks() as demo:
        #AI Disclaimer: AI generated HTML to hide textbox in the slider to prevent users from entering values out of bounds
        gr.HTML("""
    <style>
        /* Hide number input in sliders */
        input[type="number"] {
            display: none !important;
        }
        
        /* Make slider fill available space */
        .gradio-slider input[type="range"] {
            width: 100%;
        }
    </style>
    """)
        gr.Markdown("# Sorting a Deck of Cards using Insertion Sort")
        #Creates all the states for each sorting visualization
        ins_arr_insertion_steps_state = gr.State([])
        suit_insertion_steps_state = gr.State([])
        value_insertion_steps_state = gr.State([])
        deck_insertion_steps_state = gr.State([])
        
        with gr.Tab("Insertion Sort"):
            gr.Markdown("# How does Insertion Sort work?")
            gr.Markdown("### Insertion sort starts by taking the second value of a list, and 'inserts' it in the correct position.\n"
            "### In order to place it correctly, it starts at the target's index and searches backwards through the list until the next number is smaller than the target value.\n" \
            "### Due to the way it sorts the list left of the target value, we can assume the left side is always sorted")
            
            ins_arr_insertion_slider = gr.Slider(0, 1, value=0, step=1, label="Step")
            ins_arr_insertion_display = gr.HTML()
            with gr.Row():
                ins_arr_insertion_desc = gr.Textbox(label="Description", interactive=False)
                shuffle_btn = gr.Button("Shuffle List")

            gr.Markdown("### Notice how when duplicate values emerge, the right duplicate value never goes past the left duplicate value")
            gr.Markdown("- This is called **stable** sorting")
            gr.Markdown("### In the next few tabs, this page will use insertion sort to demonstrate sorting a deck of cards!")
            
            def update_ins_arr_insertion(steps: gr.State, step: str) -> str | str:
                '''Updates the states of the sorting process of the Insertion Sort Tab'''
                if not steps or len(steps) == 0:
                    return "Please shuffle first!", "No data available"

                # Validate and clamp step number
                try:
                    step_num = int(float(step))  # Handle both int and float
                except (gr.Error, ValueError, TypeError):
                    step_num = 0

                max_step = len(steps) - 1
                step_num = max(0, min(max_step, step_num))

                step_idx = min(int(step), len(steps)-1)
                data = steps[step_idx]
                html = highlight_array_elements(
                    data["array"],
                    data["target_index"], 
                    data["current_index"],
                    data["moved_index"]
                )
                return html, data["description"]
            

            ins_arr_insertion_slider.input(
                update_ins_arr_insertion,
                inputs=[ins_arr_insertion_steps_state, ins_arr_insertion_slider],
                outputs=[ins_arr_insertion_display, ins_arr_insertion_desc]
            )
            def on_shuffle() -> list: 
                '''Shuffles the ins_arr list on button press'''
                new_steps = sort_ins_arr_visualization()  # This creates new steps
                max_steps = max(0, len(new_steps) - 1)
                    
                return [
                    new_steps,  # Update state
                    gr.Slider(maximum=max_steps, value=0),  # Update slider
                    *update_ins_arr_insertion(new_steps, 0)  # Update display
                ]
                
            shuffle_btn.click(
                fn=on_shuffle,
                outputs=[ins_arr_insertion_steps_state, ins_arr_insertion_slider, ins_arr_insertion_display, ins_arr_insertion_desc]
            )
                
            # USE DEDICATED INITIALIZATION FUNCTION
            def initialize() -> list:
                '''Initializes all of the functionality for the Insertion Sort tab'''
                new_steps = sort_ins_arr_visualization()  # Use the dedicated function
                max_steps = max(0, len(new_steps) - 1)
                display_html, display_desc = update_ins_arr_insertion(new_steps, 0)
                    
                return [
                    new_steps,
                    gr.Slider(maximum=max_steps, value=0),
                    display_html,
                    display_desc
                ]
                
            demo.load(
                fn=initialize,
                outputs=[ins_arr_insertion_steps_state, ins_arr_insertion_slider, ins_arr_insertion_display, ins_arr_insertion_desc]
            )

        with gr.Tab("Basic Deck"):
            gr.Markdown("## A card is attributed with a suit and a value.")
            gr.Markdown("#### Test the buttons below and view the deck getting sorted.")
            output = gr.Textbox(lines=2, label="Deck")
            with gr.Row():
                with gr.Column():
                    desc = gr.Textbox(interactive=False, label="Description")
                with gr.Column():
                    generate_btn = gr.Button("Generate Deck")
                    generate_btn.click(fn=create_deck, inputs=None, outputs=[output, desc])

                    clear_btn = gr.Button("Clear Deck")
                    clear_btn.click(fn=clear_deck, inputs=None, outputs=[output, desc])
                with gr.Column():
                    shuffle_btn = gr.Button("Shuffle Deck")
                    shuffle_btn.click(fn=shuffle_deck, inputs=None, outputs=[output, desc])

                    sort_btn = gr.Button("Sort Deck")
                    sort_btn.click(fn=sort_deck, inputs=None, outputs=[output, desc])
            
            gr.Markdown("## While it's interesting to watch the deck get sorted, it doesn't tell us what's going on behind the scenes")
            gr.Markdown("## The next tab goes in depth on how the deck gets sorted")
        with gr.Tab("Visualization Breakdown"):
            gr.Markdown("## <span style=color:#ff6b6b>Red</span> denotes the target value we want to sort")
            gr.Markdown("## <span style=color:#7fff6e>Green</span> denotes the searching value to find the correct sorted position")
            gr.Markdown("## <span style=color:#45b7d1>Blue</span> denotes the area already searched through")
            with gr.Tab("Sorting Suits"):
                gr.Markdown("## We want to sort by suits first to correctly bundle all of the cards")
                gr.Markdown("### Suits are sorted by the following:\n" \
                "1. Spades **(S)**\n" \
                "2. Clubs **(C)**\n"
                "3. Hearts **(H)**\n" \
                "4. Diamonds **(D)**\n")
                gr.Markdown("### Suits are abbreviated to their first letter and values are unspecified with 'X'")
                gr.Markdown("#### Notice how we sort the suits but the values remain unsorted\n")
                suit_insertion_slider = gr.Slider(0, 1, value=0, step=1, label="Step")
                suit_insertion_display = gr.HTML()
                
                with gr.Row():
                    suit_insertion_desc = gr.Textbox(label="Description", interactive=False)
                    shuffle_btn = gr.Button("Shuffle Deck")
                def update_suit_insertion(steps: gr.State, step: str) -> str | str:
                    '''Updates the states of the sorting process of the Sorting Suits tab of the Visualization Tab'''
                    if not steps or len(steps) == 0:
                        return "Please shuffle first!", "No data available"
                    step_idx = min(int(step), len(steps)-1)
                    data = steps[step_idx]
                    html = highlight_array_elements(
                        data["array"],
                        data["target_index"], 
                        data["current_index"],
                        data["moved_index"]
                    )
                    return html, data["description"]
                
                suit_insertion_slider.change(
                    update_suit_insertion,
                    inputs=[suit_insertion_steps_state, suit_insertion_slider],
                    outputs=[suit_insertion_display, suit_insertion_desc]
                )

                def on_shuffle() -> list:
                    '''Shuffles the d2 list on button press and regenerates the insertion sort steps of the list'''
                    new_steps = sort_suit_visualization()  # This creates new steps
                    max_steps = max(0, len(new_steps) - 1)
                    
                    return [
                        new_steps,  # Update state
                        gr.Slider(maximum=max_steps, value=0),  # Update slider
                        *update_suit_insertion(new_steps, 0)  # Update display
                    ]
                
                shuffle_btn.click(
                    fn=on_shuffle,
                    outputs=[suit_insertion_steps_state, suit_insertion_slider, suit_insertion_display, suit_insertion_desc]
                )
                
                # USE DEDICATED INITIALIZATION FUNCTION
                def initialize() -> list:
                    '''Initializes all of the functionality for the Sorting Suits tab of the Visualization Breakdown tab'''
                    new_steps = sort_suit_visualization()  # Use the dedicated function
                    max_steps = max(0, len(new_steps) - 1)
                    display_html, display_desc = update_suit_insertion(new_steps, 0)
                    
                    return [
                        new_steps,
                        gr.Slider(maximum=max_steps, value=0),
                        display_html,
                        display_desc
                    ]
                
                demo.load(
                    fn=initialize,
                    outputs=[suit_insertion_steps_state, suit_insertion_slider, suit_insertion_display, suit_insertion_desc]
                )
            with gr.Tab("Sorting Values"):
                gr.Markdown("## Now that suits are sorted, we must now sort each the values in each suit")
                gr.Markdown("### Values are sorted by the following:\n" \
                "1. Ace **(A)**\n" \
                "2. Two **(2)**\n"
                "3. Three **(3)**\n" \
                "4. Four **(4)**\n" \
                "5. Five **(5)**\n" \
                "6. Six **(6)**\n" \
                "7. Seven **(7)**\n" \
                "8. Eight **(8)**\n" \
                "9. Nine **(9)**\n" \
                "10. Ten **(10)**\n" \
                "11. Jack **(J)**\n" \
                "12. Queen **(Q)**\n" \
                "13. King **(K)**\n")
                gr.Markdown("### Values are abbreviated to their number or first letter and suits are unspecified with 'X'")
                
                value_insertion_slider = gr.Slider(0, 1, value=0, step=1, label="Step")
                value_insertion_display = gr.HTML()
                with gr.Row():
                    value_insertion_desc = gr.Textbox(label="Description", interactive=False)
                    shuffle_btn = gr.Button("Shuffle Deck")
                def update_value_insertion(steps: gr.State, step: str) -> str | str:
                    '''Updates the states of the sorting process of the Sorting Values tab of the Visualization Tab'''

                    if not steps or len(steps) == 0:
                        return "Please shuffle first!", "No data available"
                    step_idx = min(int(step), len(steps)-1)
                    data = steps[step_idx]
                    html = highlight_array_elements(
                        data["array"],
                        data["target_index"], 
                        data["current_index"],
                        data["moved_index"]
                    )
                    return html, data["description"]
                
                value_insertion_slider.change(
                    update_value_insertion,
                    inputs=[value_insertion_steps_state, value_insertion_slider],
                    outputs=[value_insertion_display, value_insertion_desc]
                )
                
                def on_shuffle() -> list:
                    '''Shuffles the d3 list on button press and regenerates the insertion sort steps of the list'''
                    new_steps = sort_value_visualization()  # This creates new steps
                    max_steps = max(0, len(new_steps) - 1)
                    
                    return [
                        new_steps,  # Update state
                        gr.Slider(maximum=max_steps, value=0),  # Update slider
                        *update_value_insertion(new_steps, 0)  # Update display
                    ]
                
                shuffle_btn.click(
                    fn=on_shuffle,
                    outputs=[value_insertion_steps_state, value_insertion_slider, value_insertion_display, value_insertion_desc]
                )
                
                # USE DEDICATED INITIALIZATION FUNCTION
                def initialize() -> list:
                    '''Initializes all of the functionality for the Sorting Values tab of the Visualization Breakdown tab'''
                    new_steps = sort_value_visualization()  # Use the dedicated function
                    max_steps = max(0, len(new_steps) - 1)
                    display_html, display_desc = update_value_insertion(new_steps, 0)
                    
                    return [
                        new_steps,
                        gr.Slider(maximum=max_steps, value=0),
                        display_html,
                        display_desc
                    ]
                
                demo.load(
                    fn=initialize,
                    outputs=[value_insertion_steps_state, value_insertion_slider, value_insertion_display, value_insertion_desc]
                )

            with gr.Tab("Sorting Full Deck"):
                gr.Markdown("## Now let's put it all together")
                with gr.Row():
                    gr.Markdown("### Suits are sorted by the following:\n" \
                        "1. Spades **(S)**\n" \
                        "2. Clubs **(C)**\n"
                        "3. Hearts **(H)**\n" \
                        "4. Diamonds **(D)**\n")
                    gr.Markdown("### Values are sorted by the following:\n" \
                        "1. Ace **(A)**\n" \
                        "2. Two **(2)**\n"
                        "3. Three **(3)**\n" \
                        "4. Four **(4)**\n" \
                        "5. Five **(5)**\n" \
                        "6. Six **(6)**\n" \
                        "7. Seven **(7)**\n" \
                        "8. Eight **(8)**\n" \
                        "9. Nine **(9)**\n" \
                        "10. Ten **(10)**\n" \
                        "11. Jack **(J)**\n" \
                        "12. Queen **(Q)**\n" \
                        "13. King **(K)**\n")
                gr.Markdown("### Cards are first sorted by suit, then each suit is sorted internally, in place")
                gr.Markdown("### When the deck begins sorting values, <span style=color:#ffd663>Orange</span> denotes the suit being sorted")
                
                deck_insertion_slider = gr.Slider(0, 1, value=0, step=1, label="Step")
                deck_insertion_display = gr.HTML()
                
                with gr.Row():
                    deck_insertion_desc = gr.Textbox(label="Description", interactive=False)
                    shuffle_btn = gr.Button("Shuffle Deck")
                def update_deck_insertion(steps: gr.State, step: str) -> str | str:
                    if not steps or len(steps) == 0:
                        return "Please shuffle first!", "No data available"
                    step_idx = min(int(step), len(steps)-1)
                    data = steps[step_idx]
                    html = highlight_array_elements(
                        data["array"],
                        data["target_index"], 
                        data["current_index"],
                        data["moved_index"],
                        data["sublist"]
                    )
                    return html, data["description"]
                
                deck_insertion_slider.change(
                    update_deck_insertion,
                    inputs=[deck_insertion_steps_state, deck_insertion_slider],
                    outputs=[deck_insertion_display, deck_insertion_desc]
                )

                def on_shuffle() -> list:
                    '''Shuffles the d4 list on button press and regenerates the insertion sort steps of the list'''

                    new_steps = sort_deck_visualization()  # This creates new steps
                    max_steps = max(0, len(new_steps) - 1)
                    
                    return [
                        new_steps,  # Update state
                        gr.Slider(maximum=max_steps, value=0),  # Update slider
                        *update_deck_insertion(new_steps, 0)  # Update display
                    ]
                
                shuffle_btn.click(
                    fn=on_shuffle,
                    outputs=[deck_insertion_steps_state, deck_insertion_slider, deck_insertion_display, deck_insertion_desc]
                )
                
                # USE DEDICATED INITIALIZATION FUNCTION
                def initialize():
                    '''Initializes all of the functionality for the Sorting Full Deck tab of the Visualization Breakdown tab'''

                    new_steps = sort_deck_visualization()  # Use the dedicated function
                    max_steps = max(0, len(new_steps) - 1)
                    display_html, display_desc = update_deck_insertion(new_steps, 0)
                    
                    return [
                        new_steps,
                        gr.Slider(maximum=max_steps, value=0),
                        display_html,
                        display_desc
                    ]
                
                demo.load(
                    fn=initialize,
                    outputs=[deck_insertion_steps_state, deck_insertion_slider, deck_insertion_display, deck_insertion_desc]
                )
        
    return demo

#AI Disclaimer: AI created the steps.append() function, but has been modified by me to fit insertion sort
#The logic is the same for every sort_<>_visualization() function, just modified to work with suits, values, both, or neither
def sort_ins_arr_visualization() -> list:
    '''Sorts and generates the steps of ins_arr in the Insertion Sort tab'''
    global ins_arr
    if len(ins_arr)!=0:
        ins_arr.clear()
    ins_arr = generate_arr()
    steps = []
    n = len(ins_arr)
    
    i=1
    while i<n:
        target=ins_arr[i]
        j=i-1
        while j>=0 and target<ins_arr[j]:
            steps.append({
                "array": ins_arr.copy(),
                "description": f"Comparing {target} and {ins_arr[j]}",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j, i)),
                "step": f"Step {len(steps) + 1}"
            })
            j-=1
        if j==i-1:
            steps.append({
                "array": ins_arr.copy(),
                "description": f"{target} is already greater than {ins_arr[j]}",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        elif j==-1:
            steps.append({
                "array": ins_arr.copy(),
                "description": f"{target} is at the front of the list",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        else:
            steps.append({
                "array": ins_arr.copy(),
                "description": f"{target} is greater than or equal to {ins_arr[j]}",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        ins_arr.insert(j+1, target)
        ins_arr.pop(i+1)
        
        steps.append({
            "array": ins_arr.copy(),
            "description": f"inserting {target} at index {j+1} and moving remaining elements over",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "step": f"Step {len(steps) + 1}"
            })
        i+=1
    steps.append({
        "array": ins_arr.copy(),
        "description": f"The list is fully sorted",
        "target_index": [],
        "current_index": [],
        "moved_index": [],
        "sublist": [],
        "step": f"Step {len(steps) + 1}"
        })
    return steps

def sort_suit_visualization() -> list:
    '''Sorts and generates the steps of d2 in the Sorting Suits tab of the Visualization Breakdown tab'''
    arr = d2.get_deck()
    if len(arr)!=0:
        arr.clear()
        
    d2.generate_suits()
    d2.shuffle_deck()
    steps = []
    n = len(arr)
    
    i=1
    while i<n:
        target=arr[i]
        target_val = target.get_suit()
        j=i-1
        while j>=0 and target_val<arr[j].get_suit():
            steps.append({
                "array": arr.copy(),
                "description": f"Comparing {target.get_suit_name()} and {arr[j].get_suit_name()}",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j, i)),
                "step": f"Step {len(steps) + 1}"
            })
            j-=1
        if j==-1:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} reached the front of the list",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        elif j==i-1 and arr[j].get_suit()==target_val:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} is already with its suit",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        elif arr[j].get_suit()!=target_val:
            steps.append({
                "array": arr.copy(),
                "description": f"{target.get_suit_name()} is higher priority than {arr[j].get_suit_name()}",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        else:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} found its suit",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        
        arr.insert(j+1, target)
        arr.pop(i+1)

        steps.append({
            "array": arr.copy(),
            "description": f"inserting {target.get_suit_name()} at index {j+1} and moving remaining elements over",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "step": f"Step {len(steps) + 1}"
            })
        i+=1
    steps.append({
        "array": arr.copy(),
        "description": f"The suits are fully sorted",
        "target_index": [],
        "current_index": [],
        "moved_index": [],
        "sublist": [],
        "step": f"Step {len(steps) + 1}"
        })
    return steps

def sort_value_visualization() -> list:
    '''Sorts and generates the steps of d3 in the Sorting Values tab of the Visualization Breakdown tab'''

    arr = d3.get_deck()
    if len(arr)!=0:
        arr.clear()
        
    d3.generate_values()
    d3.shuffle_deck()
    steps = []
    n = len(arr)
    i=1
    while i<n:
        target=arr[i]
        target_val = target.get_value()
        j=i-1
        while j>=0 and target_val<arr[j].get_value():
            steps.append({
                "array": arr.copy(),
                "description": f"Comparing {target.get_value_name()} and {arr[j].get_value_name()}",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j, i)),
                "step": f"Step {len(steps) + 1}"
            })
            j-=1
        if j==-1:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} reached the front of the deck",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "step": f"Step {len(steps) + 1}"
            })
        elif j==i-1:
            steps.append({
            "array": arr.copy(),
            "description": f"{target.get_value_name()} is already greater than {arr[j].get_value_name()}",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "step": f"Step {len(steps) + 1}"
            })
        else:
            steps.append({
            "array": arr.copy(),
            "description": f"{target.get_value_name()} is greater than {arr[j].get_value_name()}",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "step": f"Step {len(steps) + 1}"
            })
        arr.insert(j+1, target)
        arr.pop(i+1)
        steps.append({
            "array": arr.copy(),
            "description": f"inserting {target} at index {j+1} and moving remaining elements over",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "step": f"Step {len(steps) + 1}"
            })
        i+=1

    steps.append({
        "array": arr.copy(),
        "description": f"The values are fully sorted",
        "target_index": [],
        "current_index": [],
        "moved_index": [],
        "sublist": [],
        "step": f"Step {len(steps) + 1}"
        })
    return steps

def sort_deck_visualization() -> list:
    '''Sorts and generates the steps of d4 in the Sorting Full Deck tab of the Visualization Breakdown tab'''
    arr = d4.get_deck()
    if len(arr)!=0:
        arr.clear()
        
    d4.generate_deck()
    d4.shuffle_deck()
    steps = []
    n = len(arr)
    i=1

    #sort by suit first
    while i<n:
        target=arr[i]
        target_val = target.get_suit()
        j=i-1
        while j>=0 and target_val<arr[j].get_suit():
            steps.append({
                "array": arr.copy(),
                "description": f"Comparing {target.get_suit_name()} and {arr[j].get_suit_name()}",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j, i)),
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
            })
            j-=1
        if j==-1:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} reached the front of the list",
                "target_index": i,
                "current_index": j,
                "moved_index": list(range(j+1, i+1)),
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
            })
        elif j==i-1 and arr[j].get_suit()==target_val:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} is already with its suit",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
            })
        elif arr[j].get_suit()!=target_val:
            steps.append({
                "array": arr.copy(),
                "description": f"{target.get_suit_name()} is higher priority than {arr[j].get_suit_name()}",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
            })
        else:
            steps.append({
                "array": arr.copy(),
                "description": f"{target} found its suit",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
            })
        
        arr.insert(j+1, target)
        arr.pop(i+1)

        steps.append({
            "array": arr.copy(),
            "description": f"inserting {target.get_suit_name()} at index {j+1} and moving remaining elements over",
            "target_index": i,
            "current_index": j+1,
            "moved_index": list(range(j+1, i+1)),
            "sublist": [],
            "step": f"Step {len(steps) + 1}"
            })
        i+=1
    steps.append({
        "array": arr.copy(),
        "description": f"The suits are fully sorted",
        "target_index": [],
        "current_index": [],
        "moved_index": [],
        "sublist": [],
        "step": f"Step {len(steps) + 1}"
        })
    i=1
    suit_length = len(arr)//4
    n=suit_length

    #sort by value next
    for x in range(1, 5):
        while i<n:
            target=arr[i]
            target_val = target.get_value()
            j=i-1
            while j>=0 and target_val<arr[j].get_value() and target.get_suit()==arr[j].get_suit():
                steps.append({
                    "array": arr.copy(),
                    "description": f"Comparing {target.get_value_name()} and {arr[j].get_value_name()}",
                    "target_index": i,
                    "current_index": j,
                    "moved_index": list(range(j, i)),
                    "sublist": list(range(n-suit_length, n)),
                    "step": f"Step {len(steps) + 1}"
                })
                j-=1
                
            if j==i-1:
                if j==n-suit_length-1:
                    steps.append({
                        "array": arr.copy(),
                        "description": f"{target.get_value_name()} is already at the front of its suit",
                        "target_index": i,
                        "current_index": j,
                        "moved_index": list(range(j, i)),
                        "sublist": list(range(n-suit_length, n)),
                        "step": f"Step {len(steps) + 1}"
                    })
                else:   
                    steps.append({
                        "array": arr.copy(),
                        "description": f"{target.get_value_name()} is already greater than {arr[j].get_value_name()}",
                        "target_index": i,
                        "current_index": j,
                        "moved_index": list(range(j, i)),
                        "sublist": list(range(n-suit_length, n)),
                        "step": f"Step {len(steps) + 1}"
                    })
            else:
                if j==n-suit_length-1:
                    steps.append({
                        "array": arr.copy(),
                        "description": f"{target} reached the front of its suit",
                        "target_index": i,
                        "current_index": j,
                        "moved_index": list(range(j, i)),
                        "sublist": list(range(n-suit_length, n)),
                        "step": f"Step {len(steps) + 1}"
                    })
                else:
                    steps.append({
                        "array": arr.copy(),
                        "description": f"{target.get_value_name()} is greater than {arr[j].get_value_name()}",
                        "target_index": i,
                        "current_index": j,
                        "moved_index": list(range(j, i)),
                        "sublist": list(range(n-suit_length, n)),
                        "step": f"Step {len(steps) + 1}"
                    })
            arr.insert(j+1, target)
            arr.pop(i+1)
            steps.append({
                "array": arr.copy(),
                "description": f"inserting {target} at index {j+1} and moving remaining elements over",
                "target_index": i,
                "current_index": j+1,
                "moved_index": list(range(j+1, i+1)),
                "sublist": list(range(n-suit_length, n)),
                "step": f"Step {len(steps) + 1}"
                })
            i+=1

        n+=suit_length
        i+=1
    steps.append({
                "array": arr.copy(),
                "description": f"The deck is fully sorted",
                "target_index": [],
                "current_index": [],
                "moved_index": [],
                "sublist": [],
                "step": f"Step {len(steps) + 1}"
                })
    return steps

#Runs app
demo = create_sorting_visualizer()
demo.launch(share=True)
