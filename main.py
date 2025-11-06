from rich.console import Console
from rich.table import Table
from rich.text import Text
from JingHua import User
import threading
import config
import time


def show_delay(func, *args, **kwargs):
    start_time = time.time()

    func_return = func(*args, **kwargs)
    delay_ms = int((time.time() - start_time) * 1000)

    if delay_ms < 150:
        delay_style = "bold green"
    elif delay_ms < 300:
        delay_style = "bold yellow"
    else:
        delay_style = "bold red"

    delay_part = Text(f"{delay_ms:3d}ms", style=delay_style)
    console.print(delay_part, func_return)


if __name__ == "__main__":
    console = Console()

    user = User()
    user.login(config.USERNAME, config.PASSWORD)

    courses = user.get_course_list()
    table = Table(title="课程列表")

    table.add_column("序号", justify="right", style="cyan")
    table.add_column("课程名称", style="magenta")
    table.add_column("主讲老师", style="green")

    for i, course in enumerate(courses):
        table.add_row(str(i + 1), course["name"], course["teacherName"])

    console.print(table)

    while True:
        try:
            choice_id = int(console.input("[yellow]选择课程: [/yellow]")) - 1
        except ValueError:
            console.print("[red]请输入正确的序号![/red]")
        else:
            console.print("[yellow]即将开始抢答, "
                          "按 [bold red]Ctrl+C[/bold red] 终止程序[/yellow]")
            time.sleep(1)
            break

    while True:
        t = threading.Thread(
            target=show_delay,
            args=(user.quick_response, courses[choice_id]["id"])
        )
        t.start()
        time.sleep(config.QUICK_RESPONSE_INTERVAL)
