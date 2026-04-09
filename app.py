import streamlit as st
import random
import sympy as sp

# ==========================================
# 1. Streamlit State Management & Problem Generation
# ==========================================

def reset_game():
    """Clears session state and reruns the app to generate a fresh problem."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def initialize_state():
    """Initializes the session states for when a."""
    if 'a' not in st.session_state:
        generate_problem()
    if 'show_steps' not in st.session_state:
        st.session_state.show_steps = False
    if 'status' not in st.session_state:
        st.session_state.status = 'unanswered'

def generate_problem():
    """Generates a new set of values for a, b, and c and resets UI state variables."""

    # Random number between 1 and 10 for an easy calculation
    a = random.randint(1, 10)
    
    # Calculate b and c 
    b = a**2 + 1
    c = b + 1
    
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.c = c
    st.session_state.show_steps = False
    st.session_state.status = 'unanswered'

# ==========================================
# 2. Evaluation Logic
# ==========================================

def check_answer(user_input, correct_a):
    """Parses the user input and compares it to the correct fraction."""
    try:
        # Convert the correct answer to a sympy Rational or Float
        correct_answer = sp.Rational(1, correct_a)
        
        # Parse user input using sympy
        user_parsed = sp.sympify(user_input)
        
        # Compare mathematical equivalence
        return sp.simplify(user_parsed - correct_answer) == 0
    except Exception:
        # If sympify fails (e.g., user typed letters), it's invalid/incorrect
        return False

# ==========================================
# 3. Visual Explanation (Step-by-Step)
# ==========================================

def show_step_by_step():
    """Displays the step-by-step mathematical breakdown of the limit."""
    a = st.session_state.a
    b = st.session_state.b
    c = st.session_state.c
    
    st.markdown("### Step-by-Step Solution")
    
    st.markdown("**Step 1: Recognize the indeterminate form**")
    st.write("If we directly substitute $x = -1$ into the expression, we get:")
    st.latex(r"\sqrt{\frac{(-1) + 1}{(-1)^2 + " + str(c) + r"(-1) + " + str(b) + r"}} = \sqrt{\frac{0}{0}}")
    st.write("Because it evaluates to $0/0$, we need to factor the denominator.")
    st.write("---")
    st.markdown("**Step 2: Factor the quadratic denominator**")
    st.write(f"We need to factor $x^2 + {c}x + {b}$. We look for two numbers that multiply to ${b}$ and also add to ${c}$.")
    st.write(f"Those numbers are $1$ and ${b}$.")
    st.latex(rf"x^2 + {c}x + {b} = (x + 1)(x + {b})")
    st.write("---")
    st.markdown("**Step 3: Simplify the limit**")
    st.write("Substitute the factored denominator back into the limit and cancel the common $(x + 1)$ term:")
    st.latex(rf"\lim_{{x \to -1}} \sqrt{{\frac{{x + 1}}{{(x + 1)(x + {b})}}}} = \lim_{{x \to -1}} \sqrt{{\frac{{1}}{{x + {b}}}}}")
    st.write("---")
    st.markdown("**Step 4: Evaluate the simplified limit**")
    st.write("Now, substitute $x = -1$ into the simplified expression:")
    st.latex(rf"\sqrt{{\frac{{1}}{{-1 + {b}}}}} = \sqrt{{\frac{{1}}{{{b - 1}}}}}")
    st.write("---")
    st.markdown("**Step 5: Final Calculation**")
    st.write(f"Simplify this fraction using the rule of square roots:")
    st.latex(rf"\sqrt{{\frac{{1}}{{{b - 1}}}}} = \frac{{1}}{{\sqrt{{{b - 1}}}}} = \frac{{1}}{{{a}}}")

# ==========================================
# 4. Main Application UI
# ==========================================

def main():
    st.set_page_config(page_title="Limit Evaluator Practice", page_icon="🧮")

    initialize_state()

    problem_id = f"{st.session_state.a}_{st.session_state.b}_{st.session_state.c}"
    
    st.title("Solve the limit:")
    
    # Display the equation based on current session state
    c = st.session_state.c
    b = st.session_state.b
    a = st.session_state.a
    st.latex(rf"\lim_{{x \to -1}} \sqrt{{\frac{{x + 1}}{{x^2 + {c}x + {b}}}}}")
    
    st.write("---")
    
    # Determine if input should be locked
    is_locked = st.session_state.status != 'unanswered'
    
    # User Input - Disabled if they already submitted
    user_input = st.text_input(
        "Your answer (e.g., 1/2):", 
        key=f"input_{problem_id}", 
        disabled=is_locked
    )

    # Logic for checking the users answer when they submit, then updating the session state to reflect whether they were correct or not
    if not is_locked:
        if st.button("Submit Answer"):
            if user_input.strip() != "":
                if check_answer(user_input, a):
                    st.session_state.status = "correct"
                else:
                    st.session_state.status = "incorrect"
                st.rerun()
            else:
                st.warning("Please enter an answer.")
    
    # When the user answers correctly we display a success message, the correct answer, and buttons to either try a new problem or reveal the step-by-step solution
    if st.session_state.status == "correct":
        st.success(f"🎉 **Correct!** Excellent work. The limit is $1/{a}$.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Next Problem"):
                reset_game()
        with col2:
            if st.button("📖 View Steps"):
                st.session_state.show_steps = True

    # When the user answer incorrectly we display an encouraging message and buttons to either try a new problem or reveal the step-by-step solution  
    elif st.session_state.status == "incorrect":
        st.error("❌ **Not quite right.**")
        st.info("Don't worry! Limits can be tricky. You can review the solution below or try a fresh problem to practice again.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset & Try New Problem"):
                reset_game()
        with col2:
            if st.button("📖 Reveal Step-by-Step"):
                st.session_state.show_steps = True

    # If the user clicks the reveal step-by-step answer button we show the solution steps and allow student to generate a new problem
    if st.session_state.show_steps:
        show_step_by_step()
        if st.button("Got it! Next Problem", key="bottom_next"):
            reset_game()

if __name__ == "__main__":
    main()