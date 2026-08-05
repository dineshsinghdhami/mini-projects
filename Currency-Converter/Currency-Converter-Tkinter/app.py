import tkinter as tk
from io import BytesIO
from tkinter import ttk

import requests
from PIL import Image, ImageTk


WINDOW_WIDTH = 420
WINDOW_HEIGHT = 560

BACKGROUND = "#f5f5f5"
CARD = "#ffffff"
TEXT = "#222222"
MUTED = "#666666"
BORDER = "#dddddd"
ACCENT = "#2f5bea"
ACCENT_HOVER = "#2449bd"

CURRENCY_COUNTRIES = {
    "USD": "us",
    "EUR": "eu",
    "GBP": "gb",
    "INR": "in",
    "NPR": "np",
    "JPY": "jp",
    "CNY": "cn",
    "AUD": "au",
    "CAD": "ca",
    "CHF": "ch",
    "SGD": "sg",
    "HKD": "hk",
    "NZD": "nz",
    "KRW": "kr",
    "MXN": "mx",
    "BRL": "br",
    "ZAR": "za",
    "AED": "ae",
    "SAR": "sa",
    "THB": "th",
    "MYR": "my",
    "IDR": "id",
    "PHP": "ph",
    "VND": "vn",
    "PKR": "pk",
    "BDT": "bd",
    "LKR": "lk",
    "SEK": "se",
    "NOK": "no",
    "DKK": "dk",
    "PLN": "pl",
    "TRY": "tr",
    "RUB": "ru",
    "TWD": "tw",
}

FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.12,
    "NPR": 132.50,
    "JPY": 149.50,
    "CNY": 7.24,
    "AUD": 1.52,
    "CAD": 1.36,
    "CHF": 0.88,
    "SGD": 1.34,
    "HKD": 7.83,
    "NZD": 1.64,
    "KRW": 1342.50,
    "MXN": 17.15,
    "BRL": 4.97,
    "ZAR": 18.65,
    "AED": 3.67,
    "SAR": 3.75,
    "THB": 35.50,
    "MYR": 4.72,
    "IDR": 15650,
    "PHP": 56.80,
    "VND": 24500,
    "PKR": 278.50,
    "BDT": 110.25,
    "LKR": 325.80,
    "SEK": 10.87,
    "NOK": 10.93,
    "DKK": 6.86,
    "PLN": 4.03,
    "TRY": 32.15,
    "RUB": 92.50,
    "TWD": 32.20,
}


class CurrencyConverter:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND)

        self.amount_var = tk.StringVar(value="1")
        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="NPR")
        self.result_var = tk.StringVar(value="0.00")
        self.rate_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Loading rates...")

        self.exchange_rates = FALLBACK_RATES.copy()
        self.flag_images = {}

        self.setup_style()
        self.load_flags()
        self.load_rates()
        self.build_ui()
        self.convert()

    def setup_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            padding=6,
            font=("Segoe UI", 10),
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            bordercolor=BORDER,
            arrowcolor=TEXT,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", CARD)],
            selectbackground=[("readonly", CARD)],
            selectforeground=[("readonly", TEXT)],
        )

    def load_flags(self) -> None:
        for currency, country_code in CURRENCY_COUNTRIES.items():
            self.flag_images[currency] = self.get_flag(country_code)

    def get_flag(self, country_code: str) -> ImageTk.PhotoImage:
        try:
            response = requests.get(
                f"https://flagcdn.com/48x36/{country_code}.png",
                timeout=5,
            )
            response.raise_for_status()

            image = Image.open(BytesIO(response.content)).convert("RGBA")
            image = image.resize((30, 22), Image.Resampling.LANCZOS)
        except (requests.RequestException, OSError):
            image = Image.new("RGBA", (30, 22), "#cccccc")

        return ImageTk.PhotoImage(image)

    def load_rates(self) -> None:
        try:
            response = requests.get(
                "https://api.exchangerate-api.com/v4/latest/USD",
                timeout=5,
            )
            response.raise_for_status()

            data = response.json()
            rates = data.get("rates")

            if not isinstance(rates, dict):
                raise ValueError("Invalid API response")

            self.exchange_rates = {
                code: float(rates.get(code, FALLBACK_RATES[code]))
                for code in CURRENCY_COUNTRIES
            }

            self.status_var.set("Live rates")
        except (requests.RequestException, ValueError, TypeError):
            self.exchange_rates = FALLBACK_RATES.copy()
            self.status_var.set("Offline rates")

    def build_ui(self) -> None:
        container = tk.Frame(self.root, bg=BACKGROUND)
        container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        self.build_header(container)
        self.build_converter_card(container)
        self.build_status(container)

    def build_header(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Currency Converter",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            parent,
            text="Convert currencies using current exchange rates.",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 18))

    def build_converter_card(self, parent: tk.Frame) -> None:
        card = tk.Frame(
            parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        card.pack(fill=tk.X)

        tk.Label(
            card,
            text="Amount",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=18, pady=(18, 6))

        amount_entry = tk.Entry(
            card,
            textvariable=self.amount_var,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief=tk.FLAT,
            font=("Segoe UI", 20, "bold"),
        )
        amount_entry.pack(fill=tk.X, padx=18, ipady=8)
        amount_entry.bind("<KeyRelease>", lambda _event: self.convert())

        separator = tk.Frame(card, bg=BORDER, height=1)
        separator.pack(fill=tk.X, padx=18, pady=14)

        currencies = tk.Frame(card, bg=CARD)
        currencies.pack(fill=tk.X, padx=18)

        self.from_flag = self.build_currency_selector(
            currencies,
            "From",
            self.from_currency,
            self.on_from_changed,
        )
        self.from_flag.master.master.pack(side=tk.LEFT, fill=tk.X, expand=True)

        swap_button = tk.Button(
            currencies,
            text="⇄",
            command=self.swap_currencies,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            font=("Segoe UI", 14, "bold"),
            width=3,
        )
        swap_button.pack(side=tk.LEFT, padx=10, pady=(22, 0), ipady=4)

        self.to_flag = self.build_currency_selector(
            currencies,
            "To",
            self.to_currency,
            self.on_to_changed,
        )
        self.to_flag.master.master.pack(side=tk.LEFT, fill=tk.X, expand=True)

        result_box = tk.Frame(card, bg="#f8f9fb")
        result_box.pack(fill=tk.X, padx=18, pady=18)

        tk.Label(
            result_box,
            text="Converted amount",
            bg="#f8f9fb",
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        tk.Label(
            result_box,
            textvariable=self.result_var,
            bg="#f8f9fb",
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w", padx=14)

        tk.Label(
            result_box,
            textvariable=self.rate_var,
            bg="#f8f9fb",
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=14, pady=(4, 12))

    def build_currency_selector(
        self,
        parent: tk.Frame,
        label_text: str,
        variable: tk.StringVar,
        callback,
    ) -> tk.Label:
        wrapper = tk.Frame(parent, bg=CARD)

        tk.Label(
            wrapper,
            text=label_text,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 6))

        selector = tk.Frame(
            wrapper,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        selector.pack(fill=tk.X)

        flag = tk.Label(
            selector,
            image=self.flag_images[variable.get()],
            bg=CARD,
        )
        flag.pack(side=tk.LEFT, padx=(8, 6), pady=8)

        combo = ttk.Combobox(
            selector,
            textvariable=variable,
            values=tuple(CURRENCY_COUNTRIES),
            state="readonly",
            width=5,
        )
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), pady=4)
        combo.bind("<<ComboboxSelected>>", callback)

        return flag

    def build_status(self, parent: tk.Frame) -> None:
        status_row = tk.Frame(parent, bg=BACKGROUND)
        status_row.pack(fill=tk.X, pady=(14, 0))

        tk.Label(
            status_row,
            text="●",
            bg=BACKGROUND,
            fg="#2e9d65",
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT)

        tk.Label(
            status_row,
            textvariable=self.status_var,
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT, padx=(5, 0))

    def on_from_changed(self, _event=None) -> None:
        self.from_flag.configure(
            image=self.flag_images[self.from_currency.get()]
        )
        self.convert()

    def on_to_changed(self, _event=None) -> None:
        self.to_flag.configure(
            image=self.flag_images[self.to_currency.get()]
        )
        self.convert()

    def swap_currencies(self) -> None:
        old_from = self.from_currency.get()
        old_to = self.to_currency.get()

        self.from_currency.set(old_to)
        self.to_currency.set(old_from)

        self.from_flag.configure(
            image=self.flag_images[self.from_currency.get()]
        )
        self.to_flag.configure(
            image=self.flag_images[self.to_currency.get()]
        )

        self.convert()

    def convert(self) -> None:
        try:
            amount = float(self.amount_var.get() or 0)
            from_code = self.from_currency.get()
            to_code = self.to_currency.get()

            from_rate = self.exchange_rates[from_code]
            to_rate = self.exchange_rates[to_code]

            result = (amount / from_rate) * to_rate
            current_rate = to_rate / from_rate

            self.result_var.set(f"{result:,.2f} {to_code}")
            self.rate_var.set(
                f"1 {from_code} = {current_rate:,.4f} {to_code}"
            )
        except (ValueError, KeyError, ZeroDivisionError):
            self.result_var.set("0.00")
            self.rate_var.set("Enter a valid amount")


def main() -> None:
    root = tk.Tk()
    CurrencyConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()