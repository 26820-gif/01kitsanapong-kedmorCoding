print("โปรเเกรมตรวจสอบสถานะความเร็วรถ")
speed = int(input("่ค่าความเร็วรถ(km/h) "))
print("ความเร็ว",speed,"อยู่ในสถานะ")
if speed < 81 :
    print("ปลอดภัย")
elif speed < 101 :
    print("เตือน")
elif speed < 121 :
    print("เสี่ยงถูกปรับ")
else :
    print("ผิดกฎหมาย(ปรับทันที)")