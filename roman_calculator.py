import tkinter as tk
from tkinter import messagebox

SMALL_FONT_STYLE = ("Courier", 12, "bold")
LARGE_FONT_STYLE = ("Courier", 30, "bold")
DIGITS_BUTTONS_FONT_STYLE = ("Courier", 28, "bold")
OTHER_BUTTONS_FONT_STYLE = ("Courier", 20, "bold")


class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("360x540")
        self.root.resizable(True, False)
        self.root.title("Be like a Roman!")
        # self.root.iconbitmap("icon.ico")
        self.total_arabic_expression = ""
        self.total_roman_expression = ""
        self.current_expression = ""
        self.is_roman_number_too_big = False
        self.display_frame = self.create_display_frame()
        self.arabic_total, self.roman_total, self.current = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=30)
            self.buttons_frame.columnconfigure(i, weight=30)
        self.roman_buttons = {
            "C": (2, 1), "D": (2, 2), "M": (2, 3),
            "V": (3, 1), "X": (3, 2), "L": (3, 3),
            "I": (4, 2)
        }
        self.nums_dictionary = {"I": 1, "V": 5, "X": 10,
                                "L": 50, "C": 100, "D": 500, "M": 1000}
        self.operations = {"÷": "/", "x": "*", "-": "-", "+": "+"}
        self.create_roman_digits_buttons()
        self.create_operation_buttons()
        self.create_equal_button()
        self.create_delete_button()
        self.create_clear_button()
        self.create_help_button()
        self.binds()

    def create_display_frame(self):
        frame = tk.Frame(self.root, bg="grey")
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        total_arabic_label = tk.Label(self.display_frame, text="0", anchor=tk.E,
                                      bg="#EF4E50", fg="white", padx=24, font=SMALL_FONT_STYLE,  wrapleng =340)
        total_arabic_label.pack(expand=True, fill="both")
        total_roman_label = tk.Label(self.display_frame, text="Nullus", anchor=tk.E,
                                     bg="#F05F61", fg="white", padx=24, font=SMALL_FONT_STYLE, wrapleng =340)
        total_roman_label.pack(expand=True, fill="both")
        current_label = tk.Label(self.display_frame, text="Nullus", anchor=tk.E,
                                 bg="white", fg="black", padx=24, font=LARGE_FONT_STYLE)
        current_label.pack(expand=True, fill="both")

        return total_arabic_label, total_roman_label, current_label

    def create_buttons_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=False, fill="both")
        return frame

    def roman_to_arabic(self, roman_num):
        arabic_num = 0
        for n in range(len(roman_num)-1):
            left = roman_num[n]
            right = roman_num[n+1]
            if self.nums_dictionary[left] < self.nums_dictionary[right]:
                arabic_num -= self.nums_dictionary[left]
            else:
                arabic_num += self.nums_dictionary[left]
        arabic_num += self.nums_dictionary[roman_num[-1]]
        return arabic_num

    def arabic_to_roman(self, result):
        roman_nums = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X", 20: "XX", 30: "XXX", 40: "XL", 50: "L", 60: "LX",
                      70: "LXX", 80: "LXXX", 90: "XC", 100: "C", 200: "CC", 300: "CCC", 400: "CD", 500: "D", 600: "DC", 700: "DCC", 800: "DCCC", 900: "CM", 1000: "M"
                      }

        arabic_num = int(round(result, 0))
        if arabic_num == 0:
            self.total_roman_expression += " = Nullus"
            self.current_expression = "Nullus"
            return self.total_roman_expression, self.current_expression
        roman_num = ""
        if arabic_num < 0:
            roman_num += "-"
            arabic_num = -arabic_num
        if arabic_num//1000 != 0:
            count = arabic_num//1000
            if count > 10:
                roman_num += f"M*({count})"
                self.is_roman_number_too_big = True
                arabic_num -= 1000*count
            else:
                for i in range(0, count):
                    roman_num += "M"
                    arabic_num -= 1000
        if arabic_num//100 != 0:
            count = arabic_num//100*100
            arabic_num -= count
            roman_num += roman_nums[count]
        if arabic_num//10 != 0:
            count = arabic_num//10*10
            arabic_num -= count
            roman_num += roman_nums[count]
        if arabic_num > 0:
            roman_num += roman_nums[arabic_num]
        self.total_roman_expression += f" = {roman_num}"
        self.current_expression = roman_num

    def add_to_expression(self, value):
        if self.is_roman_number_too_big:
            self.current_expression =""
            self.is_roman_number_too_big = False
            self.update_current_label()
        self.current_expression += value
        self.update_current_label()

    def append_operator(self, operator):
        self.total_arabic_expression += str(
            self.roman_to_arabic(self.current_expression))
        self.total_arabic_expression += operator
        self.current_expression += operator
        self.total_roman_expression += self.current_expression
        self.current_expression = ""
        self.update_current_label()
        self.update_total_roman_label()
        self.update_total_arabic_label()

    def evaluate(self):
        self.total_arabic_expression += str(
            self.roman_to_arabic(self.current_expression))
        self.total_roman_expression += self.current_expression

        result = eval(self.total_arabic_expression)
        self.total_arabic_expression += f" = {str(result)}"
        self.arabic_to_roman(result)
        self.update_total_arabic_label()
        self.update_total_roman_label()
        self.update_current_label()
        self.total_arabic_expression = ""
        self.total_roman_expression = ""

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_current_label()

    def clear(self):
        self.total_arabic_expression = ""
        self.total_roman_expression = ""
        self.current_expression = ""
        self.arabic_total.config(text="0")
        self.roman_total.config(text="Nullus")
        self.current.config(text="Nullus")

    def help(self):
        messagebox.showinfo(title=f"O tempŏra! O mores!",
                            message="Be aware, that true Romans didn't use negative numerals and zero! Nor decimal point.\nHence all division results are rounded. But you still can get negative numbers.\n\nLabels:\nTop label presents expression in arabic numbers for understang what is goin on.\nSecond label - expression in roman numbers.")

    def create_roman_digits_buttons(self):
        for d, grid in self.roman_buttons.items():
            b = tk.Button(self.buttons_frame, text=d, bg="white", font=DIGITS_BUTTONS_FONT_STYLE,
                          borderwidth=0, command=lambda x=d: self.add_to_expression(x))
            b.grid(row=grid[0], column=grid[1], padx=2, pady=2, sticky=tk.NSEW)

    def create_operation_buttons(self):
        c = 1
        for o in self.operations:
            b = tk.Button(self.buttons_frame, text=o, bg="#F05F61", fg="white", font=OTHER_BUTTONS_FONT_STYLE,
                          borderwidth=0, command=lambda x=self.operations[o]: self.append_operator(x))
            b.grid(row=1, column=c, padx=1, pady=1, sticky=tk.NSEW)
            c += 1

    def create_equal_button(self):
        b = tk.Button(self.buttons_frame, text="=", bg="#F05F61", fg="white",
                      font=OTHER_BUTTONS_FONT_STYLE, borderwidth=0, command=self.evaluate)
        b.grid(columnspan=2, row=4, column=3, padx=1, pady=1, sticky=tk.NSEW)

    def create_delete_button(self):
        b = tk.Button(self.buttons_frame, text="⌫", bg="#F05F61", fg="white",
                      font=OTHER_BUTTONS_FONT_STYLE, borderwidth=0, command=self.backspace)
        b.grid(row=3, column=4, padx=1, pady=1, sticky=tk.NSEW)

    def create_clear_button(self):
        b = tk.Button(self.buttons_frame, text="C", bg="#F05F61", fg="white",
                      font=OTHER_BUTTONS_FONT_STYLE, borderwidth=0, command=self.clear)
        b.grid(row=2, column=4, padx=1, pady=1, sticky=tk.NSEW)

    def create_help_button(self):
        b = tk.Button(self.buttons_frame, text="?", bg="#F05F61", fg="white",
                      font=OTHER_BUTTONS_FONT_STYLE, borderwidth=0, command=self.help)
        b.grid(row=4, column=1, padx=1, pady=1, sticky=tk.NSEW)

    def binds(self):
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Delete>", lambda e: self.clear())

        num_binds = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
                     "VI": 6, "VII": 7, "VII": 8, "IX": 9, "X": 10}
        for key in num_binds:
            self.root.bind(
                num_binds[key], lambda e, operator=key: self.add_to_expression(operator))
        for key in self.nums_dictionary:
            self.root.bind(key.lower(), lambda e,
                           digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.root.bind(self.operations[key], lambda e, operator=key: self.append_operator(
                self.operations[operator]))

    def update_total_label(self, expression):
        for symbol, operator in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        return expression

    def update_total_arabic_label(self):
        expression = self.update_total_label(self.total_arabic_expression)
        self.arabic_total.config(text=expression)

    def update_total_roman_label(self):
        expression = self.update_total_label(self.total_roman_expression)
        self.roman_total.config(text=expression)

    def update_current_label(self):
        self.current.config(text=self.current_expression)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RomCalc = Calculator()
    RomCalc.run()
