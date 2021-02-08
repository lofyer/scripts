#!/usr/bin/env python3

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog, print_container, yes_no_dialog
from prompt_toolkit.widgets import Frame, TextArea

result_modules = checkboxlist_dialog(
    title="CyberKube Provision Tool",
    text="Select roles to install.",
    values=[
        ("management", "Management"),
        ("gitlab", "Gitlab"),
        ("harbor", "Harbor"),
        ("store", "Store"),
    ],
).run()

if result_modules:
    message_dialog(
        title="Ready to go.",
        text="You selected: %s\nGreat choice sir !" % ",".join(result_modules),
    ).run()
else:
    message_dialog("Nothing.").run()

result_yes_no = yes_no_dialog(
    title="Yes/No dialog example", text=str(result_modules)
).run()

print_container(
    Frame(
        TextArea(text="Hello world!\n"),
        title="Stage: parse",
    )
)