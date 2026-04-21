import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Test")
root.geometry("600x200")

frame = ctk.CTkFrame(root)
frame.pack(padx=10, pady=10, fill="x")

btn_start = ctk.CTkButton(frame, text="开始输入", width=100, height=38)
btn_start.pack(side="right", padx=5, pady=10)

btn_pause = ctk.CTkButton(frame, text="暂停输入", width=100, height=38)
btn_pause.pack(side="right", padx=5, pady=10)

btn_resume = ctk.CTkButton(frame, text="继续输入", width=100, height=38)
btn_resume.pack(side="right", padx=5, pady=10)

btn_stop = ctk.CTkButton(frame, text="停止输入", width=100, height=38)
btn_stop.pack(side="right", padx=5, pady=10)

root.mainloop()