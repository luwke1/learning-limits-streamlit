import streamlit as st
import random
import sympy as sp

st.set_page_config(page_title="Limit Evaluator Practice")

# Basic state initialization
if 'a' not in st.session_state:
    st.session_state.a = random.randint(1, 10)
    st.session_state.b = st.session_state.a**2 + 1
    st.session_state.c = st.session_state.b + 1

st.title("Solve the limit:")

a = st.session_state.a
b = st.session_state.b
c = st.session_state.c

st.latex(rf"\lim_{{x \to -1}} \sqrt{{\frac{{x + 1}}{{x^2 + {c}x + {b}}}}}")

st.write("---")

user_input = st.text_input("Your answer (e.g., 1/2, 0.5):")

if st.button("Submit Answer"):
    try:
        # Better evaluation using sympy
        correct_answer = sp.Rational(1, a)
        user_parsed = sp.sympify(user_input)
        
        if sp.simplify(user_parsed - correct_answer) == 0:
            st.success(f"Correct! The limit is 1/{a}.")
            
            if st.button("Next Problem"):
                del st.session_state['a']
                st.rerun()
        else:
            st.error("Incorrect.")
    except Exception:
         st.warning("Please enter a valid mathematical answer.")