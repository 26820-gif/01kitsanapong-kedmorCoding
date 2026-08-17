import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ระบบจัดการงาน")
        self.geometry("380x680")
        self.configure(bg="#ffffff")
        self.resizable(False, False)

        # ข้อมูลงานตัวอย่าง
        today = datetime.now().date()
        self.tasks = [
            {
                "title": "งานที่ 1",
                "subject": "วิชาที่ 1",
                "assign_date": today.strftime("%d/%m/%Y"),
                "due_date": today + timedelta(days=3), # เหลือ 3 วัน (สีส้ม)
                "details": "ทำแบบฝึกหัดท้ายบทที่ 3",
                "expanded": False
            },
            {
                "title": "งานที่ 2",
                "subject": "วิชาที่ 2",
                "assign_date": (today - timedelta(days=2)).strftime("%d/%m/%Y"),
                "due_date": today + timedelta(days=1), # เหลือ 1 วัน (สีแดง / เลื่อนขึ้นบน)
                "details": "เตรียมสไลด์นำเสนอหน้าชั้นเรียน",
                "expanded": False
            }
        ]

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # 1. ส่วนหัว (ส่วนโปรไฟล์)
        profile_frame = tk.Frame(self, bg="#ff7f36", height=70)
        profile_frame.pack(fill="x", padx=20, pady=(20, 10))
        profile_frame.pack_propagate(False)

        # รูปโปรไฟล์ (วงกลม)
        avatar_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#ff7f36", highlightthickness=0)
        avatar_canvas.pack(side="left", padx=10)
        avatar_canvas.create_oval(3, 3, 47, 47, fill="#e0e0e0", outline="")
        avatar_canvas.create_text(25, 25, text="รูปผู้ใช้", font=("Tahoma", 9), fill="#444444")

        # ข้อความชื่อผู้ใช้
        user_lbl = tk.Label(profile_frame, text="ข้อมูลผู้ใช้", font=("Tahoma", 13, "bold"), fg="white", bg="#ff7f36")
        user_lbl.pack(side="left", padx=10)

        # 2. ปุ่มเพิ่มงาน (+)
        add_btn = tk.Button(self, text="+", font=("Tahoma", 16, "bold"), bg="#ff7f36", fg="white",
                            activebackground="#e66c25", activeforeground="white", bd=0, relief="flat",
                            width=3, height=1, command=self.open_add_dialog, cursor="hand2")
        add_btn.pack(pady=5)

        # 3. พื้นที่แสดงรายการงาน (Scrollable Frame)
        container = tk.Frame(self, bg="#ffffff")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.task_list_frame = tk.Frame(self.canvas, bg="#ffffff")

        self.task_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw", width=320)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def sort_tasks(self):
        # จัดเรียงงาน: เหลือเวลา <= 1 วัน ให้ขึ้นก่อน และเรียงตามกำหนดส่ง
        today = datetime.now().date()
        def sort_key(task):
            days_left = (task["due_date"] - today).days
            is_urgent = 0 if days_left <= 1 else 1
            return (is_urgent, task["due_date"])
        
        self.tasks.sort(key=sort_key)

    def refresh_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        self.sort_tasks()
        today = datetime.now().date()

        for idx, task in enumerate(self.tasks):
            days_left = (task["due_date"] - today).days
            is_urgent = days_left <= 1

            # เปลี่ยนสีแถบ: สีแดงเมื่อเหลือเวลา <= 1 วัน, สีส้มตามปกติ
            card_bg = "#d9381e" if is_urgent else "#ff7f36"

            card = tk.Frame(self.task_list_frame, bg="#ffffff", pady=5)
            card.pack(fill="x", expand=True)

            # แถบหลักของงาน
            main_row = tk.Frame(card, bg=card_bg, height=45)
            main_row.pack(fill="x", expand=True)
            main_row.pack_propagate(False)

            # ชื่องาน (กดเพื่อเปิด/ปิด รายละเอียด)
            title_text = f"{task['title']} ({task['subject']})"
            title_lbl = tk.Label(main_row, text=title_text, font=("Tahoma", 10, "bold"),
                                 fg="white", bg=card_bg, anchor="w", cursor="hand2")
            title_lbl.pack(side="left", padx=15, fill="both", expand=True)
            title_lbl.bind("<Button-1>", lambda e, i=idx: self.toggle_details(i))

            # ปุ่ม "เสร็จงาน"
            done_btn = tk.Button(main_row, text="เสร็จงาน", font=("Tahoma", 9, "bold"),
                                 bg="#ffffff", fg="#333333", bd=0, relief="flat", padx=10,
                                 command=lambda i=idx: self.complete_task(i), cursor="hand2")
            done_btn.pack(side="right", padx=10)

            # รายละเอียดเพิ่มเติม (แสดงเมื่อถูกกด)
            if task.get("expanded", False):
                detail_frame = tk.Frame(card, bg="#111111", pady=10, padx=10)
                detail_frame.pack(fill="x", expand=True)

                # ฝั่งซ้าย: รายละเอียดงาน
                desc_box = tk.Frame(detail_frame, bg="#f3ab7c", width=170, height=55)
                desc_box.pack(side="left", fill="both", expand=True, padx=(0, 5))
                desc_box.pack_propagate(False)

                desc_lbl = tk.Label(desc_box, text=f"รายละเอียดงาน\n{task['details']}",
                                    font=("Tahoma", 8), bg="#f3ab7c", fg="#222222", justify="left", anchor="nw")
                desc_lbl.pack(fill="both", padx=8, pady=5)

                # ฝั่งขวา: วันที่สั่ง/วันที่ส่ง
                date_box = tk.Frame(detail_frame, bg="#111111")
                date_box.pack(side="right", padx=5)

                lbl_assign = tk.Label(date_box, text=f"วันที่สั่ง {task['assign_date']}",
                                      font=("Tahoma", 8), fg="white", bg="#111111")
                lbl_assign.pack(anchor="e")

                due_str = task['due_date'].strftime("%d/%m/%Y")
                lbl_due = tk.Label(date_box, text=f"วันที่ส่ง {due_str}",
                                   font=("Tahoma", 8), fg="white", bg="#111111")
                lbl_due.pack(anchor="e")

    def toggle_details(self, index):
        self.tasks[index]["expanded"] = not self.tasks[index].get("expanded", False)
        self.refresh_task_list()

    def complete_task(self, index):
        del self.tasks[index]
        self.refresh_task_list()

    def open_add_dialog(self):
        # หน้าต่างเพิ่มงาน (Popup Dialog)
        dialog = tk.Toplevel(self)
        dialog.title("เพิ่มงาน")
        dialog.geometry("340x480")
        dialog.configure(bg="#ffffff")
        dialog.grab_set()

        tk.Label(dialog, text="หน้าตาส่วน (เพิ่มงาน)", font=("Tahoma", 14, "bold"),
                 fg="#ff7f36", bg="#ffffff").pack(pady=15)

        # ส่วนใส่วันที่ส่ง
        date_frame = tk.Frame(dialog, bg="#ff7f36", pady=8, padx=10)
        date_frame.pack(fill="x", padx=25, pady=5)

        tk.Label(date_frame, text="ใส่วันที่ส่ง (DD/MM/YYYY)", font=("Tahoma", 9, "bold"),
                 fg="white", bg="#ff7f36").pack(anchor="w")
        
        default_due = (datetime.now().date() + timedelta(days=1)).strftime("%d/%m/%Y")
        date_entry = tk.Entry(dialog, font=("Tahoma", 10), justify="center")
        date_entry.insert(0, default_due)
        date_entry.pack(fill="x", padx=25, pady=(2, 10))

        # ชื่องาน/รายละเอียด
        tk.Label(dialog, text="ชื่องาน / รายละเอียด:", font=("Tahoma", 9, "bold"), bg="#ffffff").pack(anchor="w", padx=25)
        title_entry = tk.Entry(dialog, font=("Tahoma", 10))
        title_entry.pack(fill="x", padx=25, pady=(2, 10))

        # เลือกวิชา
        tk.Label(dialog, text="เลือกวิชา", font=("Tahoma", 11, "bold"), bg="#ffffff").pack(pady=(5, 5))

        selected_subject = tk.StringVar(value="วิชาที่ 1")
        grid_frame = tk.Frame(dialog, bg="#ffffff")
        grid_frame.pack(padx=20, pady=5)

        subjects = ["วิชาที่ 1", "วิชาที่ 2", "วิชาที่ 3", "อื่นๆ ...."]
        for idx, subj in enumerate(subjects):
            r, c = divmod(idx, 2)
            btn = tk.Radiobutton(grid_frame, text=subj, value=subj, variable=selected_subject,
                                 indicatoron=0, width=12, height=2, bg="#f3ab7c", selectcolor="#ff7f36",
                                 fg="black", font=("Tahoma", 9, "bold"), bd=0)
            btn.grid(row=r, column=c, padx=5, pady=5)

        def save_task():
            date_str = date_entry.get().strip()
            task_name = title_entry.get().strip() or "งานใหม่"
            try:
                due_date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                new_task = {
                    "title": task_name,
                    "subject": selected_subject.get(),
                    "assign_date": datetime.now().date().strftime("%d/%m/%Y"),
                    "due_date": due_date_obj,
                    "details": f"งานวิชา {selected_subject.get()}",
                    "expanded": False
                }
                self.tasks.append(new_task)
                self.refresh_task_list()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกวันที่ในรูปแบบ DD/MM/YYYY ให้ถูกต้อง (เช่น 25/08/2026)")

        save_btn = tk.Button(dialog, text="ตกลง", font=("Tahoma", 11, "bold"), bg="#ff7f36", fg="white",
                             bd=0, command=save_task, cursor="hand2", width=15, height=1)
        save_btn.pack(pady=15)

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()