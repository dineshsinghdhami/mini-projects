import tkinter as tk
from tkinter import ttk, messagebox

LINEAR_UNITS = {
    "Length": {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.344,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
    },
    "Weight": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.45359237,
        "Ounce": 0.028349523125,
        "Tonne": 1000.0,
    },
    "Area": {
        "Square meter": 1.0,
        "Square kilometer": 1_000_000.0,
        "Square centimeter": 0.0001,
        "Square foot": 0.09290304,
        "Square yard": 0.83612736,
        "Acre": 4046.8564224,
        "Hectare": 10000.0,
    },
}


def convert_temperature(value, from_unit, to_unit):
    """Convert a temperature value between Celsius, Fahrenheit and Kelvin."""

    # Convert the source value to Celsius.
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        raise ValueError("Unknown temperature unit.")

    # Convert Celsius to the target unit.
    if to_unit == "Celsius":
        return celsius
    if to_unit == "Fahrenheit":
        return (celsius * 9 / 5) + 32
    if to_unit == "Kelvin":
        return celsius + 273.15

    raise ValueError("Unknown temperature unit.")


class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("560x430")
        self.root.resizable(False, False)

        self.categories = {
            "Length": list(LINEAR_UNITS["Length"].keys()),
            "Weight": list(LINEAR_UNITS["Weight"].keys()),
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Area": list(LINEAR_UNITS["Area"].keys()),
        }

        self.category_var = tk.StringVar(value="Length")
        self.from_unit_var = tk.StringVar()
        self.to_unit_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Result will appear here")

        self.create_widgets()
        self.update_units()

        # Pressing Enter runs the conversion.
        self.root.bind("<Return>", lambda event: self.convert())

    def create_widgets(self):
        title_label = ttk.Label(
            self.root,
            text="Unit Converter",
            font=("Arial", 22, "bold"),
        )
        title_label.pack(pady=(22, 8))

        subtitle_label = ttk.Label(
            self.root,
            text="Select a category, enter a value, and convert it.",
            font=("Arial", 10),
        )
        subtitle_label.pack(pady=(0, 18))

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True, padx=25)

        ttk.Label(main_frame, text="Category:").grid(
            row=0, column=0, sticky="w", padx=5, pady=8
        )

        self.category_box = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=list(self.categories.keys()),
            state="readonly",
            width=27,
        )
        self.category_box.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=8)
        self.category_box.bind("<<ComboboxSelected>>", self.update_units)

        ttk.Label(main_frame, text="Value:").grid(
            row=1, column=0, sticky="w", padx=5, pady=8
        )

        self.value_entry = ttk.Entry(
            main_frame,
            textvariable=self.value_var,
            font=("Arial", 12),
        )
        self.value_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=8)

        ttk.Label(main_frame, text="From:").grid(
            row=2, column=0, sticky="w", padx=5, pady=8
        )

        self.from_unit_box = ttk.Combobox(
            main_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=20,
        )
        self.from_unit_box.grid(row=2, column=1, sticky="ew", padx=5, pady=8)

        ttk.Label(main_frame, text="To:").grid(
            row=3, column=0, sticky="w", padx=5, pady=8
        )

        self.to_unit_box = ttk.Combobox(
            main_frame,
            textvariable=self.to_unit_var,
            state="readonly",
            width=20,
        )
        self.to_unit_box.grid(row=3, column=1, sticky="ew", padx=5, pady=8)

        swap_button = ttk.Button(
            main_frame,
            text="Swap",
            command=self.swap_units,
        )
        swap_button.grid(row=2, column=2, rowspan=2, padx=8, pady=8, sticky="ns")

        convert_button = ttk.Button(
            main_frame,
            text="Convert",
            command=self.convert,
        )
        convert_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=15)

        clear_button = ttk.Button(
            main_frame,
            text="Clear",
            command=self.clear,
        )
        clear_button.grid(row=4, column=2, sticky="ew", padx=5, pady=15)

        result_frame = ttk.LabelFrame(main_frame, text="Conversion Result", padding=15)
        result_frame.grid(
            row=5,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=5,
            pady=(5, 10),
        )

        result_label = ttk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 14, "bold"),
            anchor="center",
            wraplength=430,
        )
        result_label.pack(fill="x")

        main_frame.columnconfigure(1, weight=1)

        self.value_entry.focus()

    def update_units(self, event=None):
        category = self.category_var.get()
        units = self.categories[category]

        self.from_unit_box["values"] = units
        self.to_unit_box["values"] = units

        self.from_unit_var.set(units[0])
        self.to_unit_var.set(units[1] if len(units) > 1 else units[0])
        self.result_var.set("Result will appear here")

    def convert(self):
        raw_value = self.value_var.get().strip()

        if not raw_value:
            messagebox.showwarning("Missing Value", "Please enter a value to convert.")
            self.value_entry.focus()
            return

        try:
            value = float(raw_value)
        except ValueError:
            messagebox.showerror(
                "Invalid Value",
                "Please enter a valid number, such as 10, 5.5, or -20.",
            )
            self.value_entry.focus()
            return

        category = self.category_var.get()
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        try:
            if category == "Temperature":
                result = convert_temperature(value, from_unit, to_unit)
            else:
                factors = LINEAR_UNITS[category]
                base_value = value * factors[from_unit]
                result = base_value / factors[to_unit]

            formatted_result = f"{result:,.10g}"
            self.result_var.set(
                f"{value:,.10g} {from_unit} = {formatted_result} {to_unit}"
            )

        except (KeyError, ValueError) as error:
            messagebox.showerror("Conversion Error", str(error))

    def swap_units(self):
        old_from = self.from_unit_var.get()
        old_to = self.to_unit_var.get()

        self.from_unit_var.set(old_to)
        self.to_unit_var.set(old_from)

        if self.value_var.get().strip():
            self.convert()

    def clear(self):
        self.value_var.set("")
        self.result_var.set("Result will appear here")
        self.value_entry.focus()


def main():
    root = tk.Tk()

    # Use a clean built-in ttk theme when available.
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")

    UnitConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
