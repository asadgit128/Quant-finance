press = int(input('Press 1 for EXAMPLE values, Press 2 to enter MANUALLY: '))

if press == 1:
    # Example Scenario: Let's give them a standard real estate deal
    intialCost = 10000.0
    rate = 0.10
    earn = [2000, 2000, 3000, 4000, 5000]
    print("\nRunning Example: $10k Investment at 10% ")

elif press == 2:
    # Manual Scenario: The user provides the data
    intialCost = float(input('Enter initial cost: '))
    rate = float(input('Enter the rate (ex. 0.10): '))
    years = int(input('How many years? '))
    earn = []
    for i in range(years):
        val = float(input(f'Year {i+1} profit: '))
        earn.append(val)
else:
    print("Invalid choice. Exiting program.")
    exit() # This closes the program cleanly

# --- THE CALCULATION ENGINE (Shared by both choices) ---
totalPresentValue = sum([earn[i] / (1 + rate)**(i + 1) for i in range(len(earn))])
npv = totalPresentValue - intialCost

print(f'\nFinal NPV: ${npv:.2f}')
if npv > 0:
    print('Verdict: Safe to invest!')
elif npv < 0:
    print('Verdict: No profit, stay away.')