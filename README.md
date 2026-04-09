# README

### Limit Evaluator Practice App
This Streamlit application helps students practice evaluating limits involving square roots and rational expressions of the form:

$$\lim_{x \to -1} \sqrt{\frac{x + 1}{x^2 + cx + b}}$$

### How it Works
* **Indeterminate Forms:** The app generates random coefficients $b$ and $c$ that ensure the expression evaluates to $0/0$ at $x = -1$.
* **Clean Solutions:** The values are mathematically constrained so that the limit always simplifies to a clean fraction $1/a$ for a specific integer $a$.

### Installation & Setup
1. Clone the repository:
   ```
   git clone https://github.com/luwke1/learning-limits-streamlit.git
   cd learning-limits-streamlit
   ```
2. Install the required libraries:
   ```
   pip install streamlit sympy
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```
### Features
* Random Equation Generation: Each time the app runs, it displays a new equation.
* User Input: Accepts answers in fractional ("1/2") or decimal form.
* Feedback: Provides immediate correct/incorrect feedback with a step-by-step solution.
