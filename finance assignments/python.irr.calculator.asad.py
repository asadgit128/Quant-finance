# 1. Ask for choice
choice = input("Type '1' for example values or '2' to enter manually: ")

if choice == '1':
    cash_flows = [-1000, 300, 400, 500, 600]
    print(f"Using examples: {cash_flows}")
else:
    # Get manual input (comma separated)
    raw_input = input("Enter cash flows separated by commas (e.g., -1000, 200, 500): ")
    cash_flows = [float(x.strip()) for x in raw_input.split(",")]

# 2. The IRR math (Bisection Method)
low, high = -1.0, 2.0
for _ in range(100):
    rate = (low + high) / 2
    npv = sum(cf / (1 + rate)**t for t, cf in enumerate(cash_flows))
    if npv > 0:
        low = rate
    else:
        high = rate

# 3. Output result
print(f"The IRR is: {rate:.2%}")