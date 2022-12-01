from questionary import prompt

questions = [
    {
        'type': 'text',
        'name': 'phone',
        'message': "What's your phone number",
    },
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }
]

answers = prompt(questions)
