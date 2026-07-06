print("โปรเเกรมสูตรคูณ v2")
number = int(input("สูตรคูณที่ค้องการทราบ คือ เเม่ "))
number2 = int(input("ถึงเเม่ที่ "))
for n in range (number,number2 + 1):
    print("\nสูตรคูณ เเม่",n,"คือ")
    for i in range (1,13):
      print(n,"*",i,"=",n * i)
print("\nจัดทำโดย นายกฤษณพงศ์ เกิดเหมาะ")