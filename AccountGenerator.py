#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import string
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


# ------------------ تولید داده تصادفی ------------------

def random_hex(length: int) -> str:
    return ''.join(random.choice("0123456789ABCDEF") for _ in range(length))


def random_digits(length: int) -> str:
    if length == 1:
        return random.choice(string.digits)
    first = random.choice("123456789")
    rest = ''.join(random.choice(string.digits) for _ in range(length - 1))
    return first + rest


def build_json(hex_len=64, uid_len=10):
    payload = {
        "guest_account_info": {
            "com.garena.msdk.guest_password": random_hex(hex_len),
            "com.garena.msdk.guest_uid": random_digits(uid_len)
        }
    }
    return json.dumps(payload, ensure_ascii=False)


# ------------------ برنامه اصلی ------------------

def main():
    os.system("clear" if os.name != "nt" else "cls")

    console.print(Panel("[bold cyan] starting [/bold cyan]\n"
                        "Made with  by @Franciszw\n"
                        "Edited by @Shayaan_Dev",
                        title="🔥Acc Generator FF🔥", expand=False))

    # ساخت پوشه 777
    folder = "777"
    if not os.path.exists(folder):
        os.makedirs(folder)
        console.print(f"[green]file :[/green] {folder}")
    else:
        console.print(f"[yellow]file :[/yellow] {folder}")

    file_path = os.path.join(folder, "Acc.txt")

    # پرسیدن تعداد
    try:
        count = int(Prompt.ask("[yellow]number 1 to 50000 [/yellow]"))
    except:
        console.print("[bold red]!!![/bold red]")
        return

    # نمایش اطلاعات
    console.print(Panel(f"[green]output:[/green] {file_path}\n"
                        f"[green] number:[/green] {count}\n\n"
                        "[white]under construction[/white]",
                        title="start", expand=False))

    time.sleep(1)

    # نوشتن خطوط
    for i in range(1, count + 1):
        js = build_json()

        # متن مرتب‌تر و خواناتر
        formatted = (
            f"===== ACCOUNT {i} =====\n"
            f"{js}\n\n"
        )

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(formatted)

        console.print(f"[bold green]({i}/{count})[/bold green] completed")

        time.sleep(0.05)

    console.print(Panel("[bold green]✔[/bold green]\n"
                        f" [yellow]{file_path}[/yellow] completed.",
                        title="completed", expand=False))


if __name__ == "__main__":
    main()
