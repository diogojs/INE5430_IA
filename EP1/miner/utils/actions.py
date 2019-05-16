def reverse_actions(actions: list) -> list:
    rev = []
    if len(actions) > 0:
        for act in actions[::-1]:
            rev.append(reverse(act))
    return rev


def reverse(action):
    if (action == 'E'):
        return 'D'
    if (action == 'D'):
        return 'E'
    if (action == 'B'):
        return 'C'
    if (action == 'C'):
        return 'B'
    return None
