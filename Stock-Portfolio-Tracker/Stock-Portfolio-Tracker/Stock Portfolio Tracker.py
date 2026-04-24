
prices = {"AAPL": 180, "TSLA": 250, "GOOGL": 120, "AMZN": 100}    

n = int(input("How many different stocks do you have? "))

portfolio = {} 

for i in range(n):
    stock = input("Enter stock name: ").upper()
    if stock in prices:
        qty = int(input("Enter quantity: "))
        portfolio[stock] = qty
    else:
        print("Soory, We don't have that stock available at the movement.")


total = 0
print("\nYour Stocks:")
for stock in portfolio:
    value = prices[stock] * portfolio[stock]
    print(stock, ":", portfolio[stock], "shares x $", prices[stock], "=", value)
    total += value

print("\nTotal Investment Value: $", total)


save = input("Do you want to save this? (yes/no) ").lower()
if save == "yes":
    f = open("portfolio.txt", "w")
    f.write("Your Portfolio:\n")
    for stock in portfolio:
        value = prices[stock] * portfolio[stock]
        f.write(stock + ": " + str(portfolio[stock]) + " shares x $" + str(prices[stock]) + " = " + str(value) + "\n")
    f.write("\nTotal Investment Value: $" + str(total))
    f.close()
    print("Saved to portfolio.txt")
