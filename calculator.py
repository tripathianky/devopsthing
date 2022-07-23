num1 = int(input("Enter number1: "))
num2 = int(input("Enter number2: "))
opr = input("Enter the valid operation like (+, -, * OR / ): ")

if opr == "+":
    print(num1 + num2)
elif opr == "-":
    print(num1-num2)
elif opr == "*":
    print(num1*num2)
elif opr == "/":
    print(num1/num2)
else:
    print("Invalid Operator")

