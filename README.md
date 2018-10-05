# BakaevGrep

Окончательный вариант программы находится в файле grep.py

Программа не проходит два теста, а именно test_base_scenario_count и test_base_scenario_invert. Хотя при вводе данных через консоль - все работает правильно.

Но если убрать строки:
    if lol.ignore_case:
        lol.pattern = lol.pattern.lower()
        for key in range(len(strings)):
            strings[key]=strings[key].lower()
            
все тесты начинают выполняться корректно, кроме, конечно же, теста на ignore_case

P.S. возможно, так только у меня
