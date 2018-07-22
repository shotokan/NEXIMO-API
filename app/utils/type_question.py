"""
este modulo ayuda a la verificacion de las preguntas, y su tipo
"""
TYPE_QUESTIONS = {
    1: 'BOOL',
    2: 'M-ONE',
    3: 'M-MTONE',
    4: 'M-ALL'
}


def is_bool(corrects, wrong):
    if len(corrects) == 1 and len(wrong) == 1:
        return True
    return False


def is_m_one(corrects, wrong):
    if len(corrects) == 1 and len(wrong) >= 1:
        return True
    return False


def is_m_mtone(corrects, wrong):
    if len(corrects) >= 1 and len(wrong) >= 1:
        return True
    return False


def is_m_all(corrects, wrong):
    if len(corrects) >= 1 and len(wrong) == 0:
        return True
    return False


def bool_answer(user_answers, answers):
    print(user_answers, answers)
    a = set(user_answers)
    b = set(answers)
    if len(user_answers) == 1 and len(a.intersection(b)) == 1:
        return True
    return False


def m_mtone(user_answers, answers):
    print("IN MORE THAN")
    print(user_answers, answers)
    a = set(user_answers)
    b = set(answers)
    print(a.intersection(b))
    if 1 <= len(user_answers) <= len(answers) and len(a.intersection(b)) >= 1:
        return True
    return False


def m_one(user_answers, answers):
    print("IN ONE")
    print(user_answers, answers)
    a = set(user_answers)
    b = set(answers)
    if len(user_answers) == 1 and len(a.intersection(b)) == 1:
        return True
    return False


def m_all(user_answers, answers):
    a = set(user_answers)
    b = set(answers)
    if len(user_answers) == len(answers) and len(b - a) == 0:
        return True
    return False
