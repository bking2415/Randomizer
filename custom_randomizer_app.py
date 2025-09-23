import streamlit as st
import random
import pandas as pd
import math
import time

# Set the title and page configuration
st.set_page_config(page_title="Customizable Randomizer", layout="wide")
st.title('Randomizer')
st.write("Add options, set weights, and either pick a single winner or create a ranked draft list.")

# ---
# ## Session State Initialization
# ---
if 'options' not in st.session_state:
    st.session_state.options = [1, 2]
if 'weight_method_radio' not in st.session_state:
    st.session_state.weight_method_radio = 'Percentages'
if 'option_weight_pct_0' not in st.session_state and st.session_state.weight_method_radio == 'Percentages':
    st.session_state['option_weight_pct_0'] = 50.0
    st.session_state['option_weight_pct_1'] = 50.0
if 'randomization_mode' not in st.session_state:
    st.session_state.randomization_mode = "Pick a Single Winner"
if 'lottery_delay' not in st.session_state:
    st.session_state.lottery_delay = 3.0
if 'draft_list' not in st.session_state:
    st.session_state.draft_list = []
if 'power_ball_numbers' not in st.session_state:
    st.session_state.power_ball_numbers = None
if 'available_options' not in st.session_state:
    st.session_state.available_options = []
if 'available_weights' not in st.session_state:
    st.session_state.available_weights = []
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'show_balloons' not in st.session_state:
    st.session_state.show_balloons = False

# ---
# ## Core Functions
# ---
def get_current_weights():
    """Constructs the list of weights from individual widget states."""
    num_options = len(st.session_state.options)
    if st.session_state.weight_method_radio == 'Percentages':
        return [st.session_state.get(f'option_weight_pct_{i}', 0.0) for i in range(num_options)]
    else:
        return st.session_state.get('whole_weights', [1] * num_options)

def rebalance_weights_equally():
    """Equally distributes weights to sum to 100%."""
    num_options = len(st.session_state.options)
    if num_options > 0:
        new_weight = 100.0 / num_options
        for i in range(num_options):
            st.session_state[f'option_weight_pct_{i}'] = new_weight
            
def normalize_weights(changed_index=None):
    """Normalizes weights to sum to 100% while preserving their ratios."""
    num_options = len(st.session_state.options)
    
    weights = [st.session_state.get(f'option_weight_pct_{i}', 0.0) for i in range(num_options)]
    
    total = sum(weights)

    if total > 0 and not math.isclose(total, 100.0):
        for i in range(num_options):
            st.session_state[f'option_weight_pct_{i}'] = (weights[i] / total) * 100


def draft_next_selection():
    """Initializes, picks one option, and re-normalizes the rest."""
    # Initialize the draft pool on the first pick
    if not st.session_state.draft_list:
        st.session_state.available_options = st.session_state.options.copy()
        st.session_state.available_weights = current_weights.copy()
        total_weight = sum(st.session_state.available_weights)
        if total_weight > 0:
            st.session_state.available_weights = [(w / total_weight) * 100.0 for w in st.session_state.available_weights]

    if not st.session_state.available_options:
        st.warning("The draft is complete!")
        return

    # Pick the next draftee
    picked_option = random.choices(st.session_state.available_options, weights=st.session_state.available_weights, k=1)[0]
    st.session_state.draft_list.append(picked_option)

    # Remove the picked option from the available pool
    idx = st.session_state.available_options.index(picked_option)
    del st.session_state.available_options[idx]
    del st.session_state.available_weights[idx]

    # Re-normalize the remaining weights for the next round
    remaining_weights = st.session_state.available_weights
    if remaining_weights:
        total_remaining_weight = sum(remaining_weights)
        if total_remaining_weight > 0:
            st.session_state.available_weights = [(w / total_remaining_weight) * 100.0 for w in remaining_weights]

def generate_power_ball():
    """Generates and stores 5 white balls and 1 red Powerball."""
    reset_results()
    white_balls = sorted(random.sample(range(1, 70), 5))
    red_ball = random.randint(1, 26)
    st.session_state.power_ball_numbers = {'white': white_balls, 'red': red_ball}

def reset_weights():
    # If the new method is percentages, reset to even percentages
    if st.session_state.weight_method_radio == 'Percentages':
        rebalance_weights_equally()
    else:
        # For whole numbers, we still need to manage a separate state
        num_options = len(st.session_state.options)
        st.session_state.whole_weights = [1] * num_options
    reset_results()

def add_option():
    """Adds a new numerical option with an appropriate default weight."""
    new_index = len(st.session_state.options)
    st.session_state.options.append(f'{new_index + 1}')
    if st.session_state.weight_method_radio == 'Whole Numbers':
        if 'whole_weights' not in st.session_state:
            st.session_state.whole_weights = [1] * len(st.session_state.options)
        st.session_state.whole_weights.append(1)
    else:
        # For percentages, set new widget state to 0 and rebalance all
        st.session_state[f'option_weight_pct_{new_index}'] = 0.0
        rebalance_weights_equally()

def remove_option(index_to_remove):
    """Removes an option and rebalances weights if necessary."""
    if len(st.session_state.options) > 1:
        # Correctly remove the option and its weight
        del st.session_state.options[index_to_remove]

        if st.session_state.weight_method_radio == 'Percentages':
            # Remove the weight input from session state
            del st.session_state[f'option_weight_pct_{index_to_remove}']
            # Rebalance weights for the remaining options
            rebalance_weights_equally()
        else:
            del st.session_state.whole_weights[index_to_remove]
        
        reset_results()

def reset_results():
    """Clears all results (winner and draft list)."""
    st.session_state.draft_list = []
    st.session_state.available_options = []
    st.session_state.available_weights = []
    st.session_state.winner = None
    st.session_state.show_balloons = False
    st.session_state.power_ball_numbers = None

# ---
# ## Main Interface Layout
# ---
main_col, results_col = st.columns([2, 1])

# This check will disable the entire setup column if Power Ball is selected
is_powerball_mode = st.session_state.randomization_mode == 'Power Ball'

with main_col:
    st.header('⚙️ Setup')
    if is_powerball_mode:
        st.info("The setup panel is disabled for Power Ball mode. Use the panel on the right to draw numbers.")
        
    tab1, tab2 = st.tabs(["Configure Options", "Import from File"])

    with tab1:
        col_settings1, col_settings2 = st.columns(2)
        with col_settings1:
            weight_method = st.radio(
                "Weighting method:",
                ('Percentages', 'Whole Numbers'),
                key='weight_method_radio',
                on_change=reset_weights,
                help="**Percentages:** Weights auto-balance to 100. **Whole Numbers:** Weights are relative.",
                disabled=is_powerball_mode
            )
        with col_settings2:
            is_lottery_mode = st.session_state.randomization_mode == 'Lottery Draft'
            help_text = "Lottery Draft is always without replacement." if is_lottery_mode else "If checked, each option can only be picked once per draft."
            
            replacement = st.checkbox(
                'Draft without replacement',
                key='replacement_checkbox',
                value=True, # In lottery mode, this is always True. Otherwise, it uses the user's choice.
                on_change=reset_results,
                help=help_text,
                disabled=is_lottery_mode or is_powerball_mode
            )
        st.markdown("---")

        st.subheader('📝 Options List')
        st.write("Options start as numbers. Click on a number to give it a custom name.")
        
        c1, c2, c3 = st.columns([4, 2, 1])
        c1.markdown("**Option Name / Number**")
        c2.markdown("**Weight**")
        c3.markdown("**Remove**")

        
        for i in range(len(st.session_state.options)):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                st.session_state.options[i] = st.text_input(
                    f'Option Name {i+1}',
                    value=st.session_state.options[i],
                    key=f'option_name_{i}',
                    label_visibility="collapsed",
                    disabled=is_powerball_mode
                )
            with col2:
                if weight_method == 'Percentages':
                    # ✅ Ensure weights are floats to avoid StreamlitMixedNumericTypesError
                    st.number_input(
                        f'Weight % {i+1}',
                        min_value=0.0,
                        max_value=100.0,
                        step=0.01,
                        format="%.2f",
                        key=f'option_weight_pct_{i}',
                        label_visibility="collapsed",
                        disabled=is_powerball_mode
                    )
                else:  # Whole Numbers
                    # ✅ Ensure weights are integers for whole number mode
                    if 'whole_weights' not in st.session_state or len(st.session_state.whole_weights) != len(st.session_state.options):
                        st.session_state.whole_weights = [1] * len(st.session_state.options)
                    st.number_input(
                        f'Weight {i+1}',
                        min_value=1,
                        step=1,
                        key=f'option_weight_whole_{i}',
                        label_visibility="collapsed",
                        disabled=is_powerball_mode
                    )
                    st.session_state.whole_weights[i] = st.session_state[f'option_weight_whole_{i}']
            with col3:
                st.button(
                    '❌',
                    key=f'remove_btn_{i}',
                    on_click=remove_option,
                    args=(i,),
                    help="Remove this option",
                    disabled=is_powerball_mode
                )
        
        st.button('➕ Add another option', on_click=add_option, use_container_width=True, disabled=is_powerball_mode)

        if weight_method == 'Percentages' and len(st.session_state.options) > 0:
            current_weights = get_current_weights()
            total_weight = sum(current_weights)

            # Display a warning/error message if the total is not 100%
            if not math.isclose(total_weight, 100.0):
                if total_weight > 100.0:
                    st.error(f"⚠️ Your weights add up to {total_weight:.2f}%, which is more than 100%.")
                else:
                    st.warning(f"⚠️ Your weights only add up to {total_weight:.2f}%, which is less than 100%.")
                
                # Always display the buttons when in 'Percentages' mode
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    st.button(
                        "🔢 Normalize Ratios",
                        on_click=normalize_weights,
                        key="normalize_button",
                        use_container_width=True,
                        help="Scale current weights to sum to 100% while keeping their proportions.",
                        disabled=is_powerball_mode
                    )
                with btn_col2:
                    st.button(
                        "⚖️ Rebalance Equally",
                        on_click=rebalance_weights_equally,
                        key="rebalance_button",
                        use_container_width=True,
                        help="Distribute 100% evenly across all options.",
                        disabled=is_powerball_mode
                    )

    with tab2:
        st.subheader('📂 Import Options from File')
        uploaded_file = st.file_uploader("Upload a CSV or TXT file with one option per row.", type=['csv', 'txt'], disabled=is_powerball_mode)
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, header=None)
                st.session_state.options = df.iloc[:, 0].astype(str).tolist()
                reset_results()
                # Default to whole numbers after import
                st.session_state.weights = [1.0] * len(st.session_state.options)
                st.success(f'Successfully imported {len(st.session_state.options)} options.')
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")

with results_col:
    st.header('🎉 Results')

    if len(st.session_state.options) < 1:
        st.info("Add at least one option to get started.")
    else:
        mode = st.radio(
            "Choose a randomization type:",
            ("Pick a Single Winner", "Create a Draft List", "Lottery Draft", "Power Ball"),
            key='randomization_mode',
            horizontal=True,
            on_change=reset_results,
            disabled=(len(st.session_state.options) < 2)
        )
        st.markdown("---")
        
        current_weights = get_current_weights() if st.session_state.weight_method_radio == 'Percentages' else st.session_state.get('whole_weights', [1]*len(st.session_state.options))

        if mode == "Pick a Single Winner":
            if len(st.session_state.options) < 1: st.warning("Please add at least one option.")
            else:
                st.button(
                    "🏆 Find the Winner!", 
                    on_click=lambda: setattr(st.session_state, 'winner', 
                    random.choices(st.session_state.options, weights=current_weights, k=1)[0]) or setattr(st.session_state, 'show_balloons', True), 
                    use_container_width=True
                )
        

        elif mode == "Create a Draft List":
            if replacement:
                max_picks = len(st.session_state.available_options) if st.session_state.draft_list else len(st.session_state.options)
            else:
                max_picks = max(len(st.session_state.available_options),100) # Arbitrary limit for drafting with replacement
            is_disabled = max_picks == 0
            num_picks = st.number_input('Number of Options to Draft', min_value=1, max_value=max(1, max_picks), value=1, disabled=is_disabled)

            def run_draft():
                reset_results()
                items_pool, weights_pool = [], []
                if replacement:
                    if not st.session_state.available_options and not st.session_state.draft_list:
                        st.session_state.available_options = st.session_state.options.copy()
                        st.session_state.available_weights = st.session_state.weights.copy()
                    items_pool, weights_pool = st.session_state.available_options, st.session_state.available_weights
                else:
                    items_pool, weights_pool = st.session_state.options, st.session_state.weights

                if not items_pool:
                    st.warning("No more options are available to draft!")
                    return

                for _ in range(num_picks):
                    if not items_pool: break
                    picked = random.choices(items_pool, weights=weights_pool, k=1)[0]
                    st.session_state.draft_list.append(picked)
                    if replacement:
                        idx = items_pool.index(picked)
                        del items_pool[idx]
                        del weights_pool[idx]

            btn_col1, btn_col2 = st.columns(2)
            btn_col1.button('🎲 Draft!', on_click=run_draft, use_container_width=True, disabled=is_disabled)
            btn_col2.button('🔄 Reset', on_click=reset_results, use_container_width=True, disabled=(not st.session_state.draft_list))
        
        elif mode == "Lottery Draft":
            st.number_input(
                'Suspense Delay (seconds)',
                min_value=0.0,
                max_value=10.0,
                step=0.5,
                key='lottery_delay',
                help="Set the duration for the dramatic reveal of each selection."
            )
            
            is_draft_complete = len(st.session_state.draft_list) == len(st.session_state.options)
            
            draft_btn_col, reset_btn_col = st.columns(2)
            with draft_btn_col:
                if st.button('Draft Next Selection', disabled=is_draft_complete, use_container_width=True):
                    pick_number = len(st.session_state.draft_list) + 1
                    with st.spinner(f"The Number {pick_number} Selection is...", show_time=True):
                        time.sleep(st.session_state.lottery_delay)
                        draft_next_selection()
                    st.rerun()
            
            with reset_btn_col:
                st.button('🔄 Reset Draft', on_click=reset_results, use_container_width=True, disabled=(not st.session_state.draft_list))
        
        elif mode == "Power Ball":
            btn1, btn2 = st.columns(2)
            btn1.button("🔴 Draw Power Ball Numbers", on_click=generate_power_ball, use_container_width=True)
            btn2.button("🔄 Reset", on_click=reset_results, use_container_width=True, disabled=(not st.session_state.power_ball_numbers))

    st.markdown("---")
    if st.session_state.winner:
        st.success(f"### The Winner is: \n ## {st.session_state.winner}")
        st.button("🔄 Reset Winner", on_click=reset_results, use_container_width=True)
        if st.session_state.get('show_balloons'):
            st.balloons()
            st.session_state.show_balloons = False

    elif st.session_state.draft_list:
        st.subheader('📋 Draft List')
        for i, item in enumerate(st.session_state.draft_list):
            st.markdown(f"**{i+1}.** {item}")
    
    elif st.session_state.power_ball_numbers:
        st.subheader("Winning Power Ball Numbers")
        white = st.session_state.power_ball_numbers['white']
        red = st.session_state.power_ball_numbers['red']
        # Format numbers with leading zeros for a consistent look
        white_str = " &nbsp; ".join(f"{num:02}" for num in white)
        red_str = f"{red:02}"

        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; border-radius: 10px; background-color: #262730;">
            <p style="font-size: 28px; font-weight: bold; letter-spacing: 5px; margin: 0;">
                {white_str} <span style="color: red;">{red_str}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif len(st.session_state.options) > 0:
        st.info("Your results will appear here.")

st.markdown("Made with💡by [BOL](https://youtube.com/@TheBOLGuide)")