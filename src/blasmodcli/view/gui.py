
class ChoiceGUI:

    def __init__(self, game_title: str):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.title("Blasphemous Mod Installer")
        self.root.attributes("-type", "dialog")

        self.launch_modded: bool | None = None
        self.remember_until_next_reboot = tk.BooleanVar()

        self.question_label = tk.Label(self.root, text=f"How do you want to start {game_title}?")
        self.question_label.pack()

        self.remember_checkbox = tk.Checkbutton(
            self.root,
            text="Remember this choice for this game until next reboot.",
            variable=self.remember_until_next_reboot
        )
        self.remember_checkbox.pack()

        self.choices = tk.Frame(self.root)
        self.vanilla_button = tk.Button(self.choices, text="Vanilla", command=self.chose_launch_vanilla)
        self.vanilla_button.pack(side="left")
        self.modded_button = tk.Button(self.choices, text="Modded", command=self.chose_launch_modded)
        self.modded_button.pack(side="right")
        self.modded_button.focus()
        self.choices.pack()

    def chose_launch_modded(self):
        self.launch_modded = True
        self.root.destroy()

    def chose_launch_vanilla(self):
        self.launch_modded = False
        self.root.destroy()

    def mainloop(self):
        self.root.mainloop()
