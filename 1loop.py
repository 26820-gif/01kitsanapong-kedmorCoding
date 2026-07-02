import random
number = random.randint(1,100)
print("เกมทาบเลข")
playernumber = 0
while playernumber != number:
    playernumber = int(input("เลขที่เดา"))
    if playernumber > number :
          print("มากไป\n")
    elif playernumber < number :
          print("น้อยไป\n")
    else :
          print("ถูกต้อง\n") 