print("โปรเเกรมคำนวณคะเเนนเฉลี่ย\n ")
mathscore = int(input("คะเเนนวิชาคณิตศาสคร์ 0-100 "))
sciencescore = int(input("คะเเนนวิชาวิทยาศาสตร์ 0-100 "))
thaiscore = int(input("คะเเนนวิชาภาษาไทย 0-100 "))
totalscore = (mathscore + sciencescore + thaiscore)
averagescore = totalscore/3
print("\nคะเเนนรวมที่ได้ คือ ",totalscore,"คะเเนน")
print("คะเเนนเฉลี่ยที่ได้ คือ ", int(averagescore) ,"คะเเนน")
if averagescore < 60 : 
    print("อยู่ในเกณฑ์ ควรปรับปรุง")
elif averagescore < 80 : 
    print("อยู่ในเกณฑ์ ผ่าน")
elif averagescore : 
    print("อยู่ในเกณฑ์ ดีเยี่ยม")
print("จัดทำโดย นายกฤษณพงศ์ เกิดเหมาะ ม.4/4 เลขที่ 1 ")