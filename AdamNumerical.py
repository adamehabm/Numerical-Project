import sympy as sp 

def C_Sol(method, f, a=None, b=None, x0=None, x1=None, tol=None, max_iter=None, df=None, error_type="percentage", n=None):
    steps = []
    iteration = 1
    c_old = None 

    while True:
        if method == "bisection":
            c = (a + b) / 2
        elif method == "false_position":
            c = a - (f(a) * (b - a)) / (f(b) - f(a))
        elif method == "secant":
            c = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        elif method == "newton":
            c = x0 - f(x0) / df(x0)
        else:
            raise ValueError("Invalid method selected.")

        abs_error = abs(c - c_old) if c_old is not None else float('inf')
        perc_error = (abs_error / abs(c) * 100) if c_old is not None and c != 0 else float('inf')

        if method == "secant":
            steps.append({
                "Iteration": iteration,
                "x0": round(x0, 5),
                "f(x0)": round(f(x0), 5),
                "x1": round(x1, 5),
                "f(x1)": round(f(x1), 5),
                "c": round(c, 5),
                "Absolute Error": round(abs_error, 5) if abs_error != float('inf') else "N/A",
                "Percentage Error": round(perc_error, 5) if perc_error != float('inf') else "N/A"
            })
        elif method in ["bisection", "false_position"]:
            steps.append({
                "Iteration": iteration,
                "a": round(a, 5),
                "b": round(b, 5),
                "f(a)": round(f(a), 5),
                "f(b)": round(f(b), 5),
                "c": round(c, 5),
                "f(c)": round(f(c), 5),
                "Absolute Error": round(abs_error, 5) if abs_error != float('inf') else "N/A",
                "Percentage Error": round(perc_error, 5) if perc_error != float('inf') else "N/A"
            })
        elif method == "newton":
            steps.append({
                "Iteration": iteration,
                "x0": round(x0, 5),
                "f(x0)": round(f(x0), 5),
                "f'(x0)": round(df(x0), 5),
                "c": round(c, 5),
                "Absolute Error": round(abs_error, 5) if abs_error != float('inf') else "N/A",
                "Percentage Error": round(perc_error, 5) if perc_error != float('inf') else "N/A"
            })

        if ((tol is not None and 
            ((error_type == "absolute" and abs_error <= tol) or 
             (error_type == "percentage" and perc_error <= tol))) or
            (max_iter is not None and iteration >= max_iter) or
            (n is not None and c_old is not None and str(c)[:str(c).find('.') + n + 1] == str(c_old)[:str(c_old).find('.') + n + 1])):
            return c, steps

        if method in ["bisection", "false_position"]:
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        elif method == "secant":
            x0, x1 = x1, c
        elif method == "newton":
            x0 = c

        c_old = c
        iteration += 1

def show_steps(method_name, root, steps):
    print(f"\nMethod: {method_name}")
    if root is not None:
        print(f"Root found: {float(root):.5f}\n")
        if method_name == "Secant":
            titles = ["Iteration", "x0", "f(x0)", "x1", "f(x1)", "c", "Absolute Error", "Percentage Error"]
        elif method_name == "Newton":
            titles = ["Iteration", "x0", "f(x0)", "f'(x0)", "c", "Absolute Error", "Percentage Error"]
        else:
            titles = ["Iteration", "a", "b", "f(a)", "f(b)", "c", "f(c)", "Absolute Error", "Percentage Error"]

        print(" ".join([f"{title:<15}" for title in titles]))
        print("-" * (len(titles) * 15))

        for step in steps:
            print(" ".join([f"{step.get(title, 'N/A'):<15}" for title in titles]))
    else:
        print("The method did not converge to a solution within the given tolerance or iterations.")

def main():
    print("Welcome to my Numerical Program!")
    while True:
        try:
            expr = input("Enter the function f(x): ").strip() 
            x = sp.symbols('x')
            f_expr = sp.sympify(expr)
            if not f_expr.free_symbols == {x}:
                raise ValueError("The function must be in terms of 'x'. Please try again.")
            break
        except Exception as e:
            print(f"Invalid expression: {e}. Please try again.")

    f = sp.lambdify(x, f_expr)
    df = sp.lambdify(x, sp.diff(f_expr, x))

    methods = ["bisection", "false_position", "secant", "newton"]
    print("Choose a method:")
    print("1. Bisection Method")
    print("2. False Position Method")
    print("3. Secant Method")
    print("4. Newton Method")

    choice = int(input("Enter your choice (1-4): ")) - 1

    if choice not in range(len(methods)): 
        print("Invalid choice. Please select a number between 1 and 4.")
        exit() 
        
    print("Select stopping condition:")
    print("1. Tolerance only")
    print("2. Maximum iterations only")
    print("3. Correct to n decimal places")
    input_choice = int(input("Enter your choice (1-3): "))
    if input_choice not in [1, 2, 3]:
        print("Invalid choice. Please select a number between 1 and 3.")
        exit() 

    tol, max_iter, n = None, None, None
    if input_choice == 1:
        tol = float(input("Enter the tolerance: "))
    elif input_choice == 2:
        max_iter = int(input("Enter the maximum number of iterations: "))
    elif input_choice == 3:
        n = int(input("Enter n (up to 5 please): "))

    error_type = "percentage"
    if input_choice == 1:
        print("Select the error type:")
        print("1. Absolute Error")
        print("2. Percentage Error")
        error_choice = int(input("Enter your choice (1 or 2): "))
        error_type = "absolute" if error_choice == 1 else "percentage"
        if error_choice not in [1, 2]:
            print("Invalid choice. Please select a number between 1 and 2.")
            exit()

    if choice == 0 or choice == 1:
        a = float(input("Enter the lower bound (a): "))
        b = float(input("Enter the upper bound (b): "))
        if f(a) * f(b) > 0:
            print("Error: f(a) and f(b) must have opposite signs. Please enter valid bounds.")
            exit()
        method = methods[choice]
        root, steps = C_Sol(method, f, a=a, b=b, tol=tol, max_iter=max_iter, error_type=error_type, n=n)
    elif choice == 2:
        x0 = float(input("Enter the first initial guess (x0): "))
        x1 = float(input("Enter the second initial guess (x1): "))
        root, steps = C_Sol("secant", f, x0=x0, x1=x1, tol=tol, max_iter=max_iter, error_type=error_type, n=n)
    elif choice == 3:
        x0 = float(input("Enter the initial guess (x0): "))
        root, steps = C_Sol("newton", f, x0=x0, tol=tol, max_iter=max_iter, df=df, error_type=error_type, n=n)
    else:
        print("Invalid choice. Please select a valid method.")
        return

    show_steps(methods[choice].title(), root, steps)

main()
