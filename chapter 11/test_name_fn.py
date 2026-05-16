from name_fn import get_formatted_name

def test_first_last_name():
    """Do names like 'Janis Joplin' work?"""
    formatted_name = get_formatted_name('janis', 'joplin')
    assert formatted_name == 'Janis Joplin'

def test_first_middle_last_name():
    """Do names like 'Monkey D. Luffy' works?"""
    formatted_name = get_formatted_name('monkey','luffy','d.')
    assert formatted_name == 'Monkey D. Luffy'

