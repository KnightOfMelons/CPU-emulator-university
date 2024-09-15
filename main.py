# ПРИМЕР КОМАНД, С КОТОРЫМИ ПРОВОДИЛ ТЕСТИРОВАНИЕ:

#     "PUSH 2",  # Помещаем 2 на стек
#     "PUSH 3",  # Помещаем 3 на стек
#     "ADD",  # Складываем верхние два элемента на стеке
#     "PUSH 5",  # Помещаем 5 на стек
#     "ADD",  # Складываем результат с 5

# Память (фон-неймановская архитектура)
memory = []

# Стек
stack = []


# Функция для выполнения инструкций
def execute_instruction(instruction):
    # Разбиваем инструкцию на команду и операнды (если есть)
    parts = instruction.split()
    mnemonic = parts[0].upper()  # Приводим команду к нижнему регистру

    # Эмуляция инструкции
    if mnemonic == "PUSH":
        # PUSH <imm> - помещаем значение в стек
        if len(parts) != 2 or not parts[1].isdigit():
            print("Ошибка: неверная команда PUSH")
            return
        value = int(parts[1])
        stack.append(value)

    elif mnemonic == "ADD":
        # ADD - складываем два верхних элемента стека
        if len(stack) < 2:
            print("Ошибка: недостаточно элементов в стеке для выполнения операции 'add'")
            return
        b = stack.pop()  # Снимаем верхний элемент
        a = stack.pop()  # Снимаем следующий элемент
        result = a + b  # Складываем
        stack.append(result)  # Помещаем результат обратно на стек

    elif mnemonic == "CLEAR":
        # CLEAR - очищаем стек
        stack.clear()
        print("Стек очищен.")

    elif mnemonic == "EXIT":
        # EXIT - завершение программы
        print("\n=== Завершение программы. ===")
        return "exit"

    else:
        print(f"Инструкция '{mnemonic}' не поддерживается")


# Основной цикл ввода команд
while True:
    # Получаем команду от пользователя
    command = input("\nСписок команд на выбор:\n\nPUSH <значение_в_цифрах>\nADD\nCLEAR (очищает стек от значений)\n"
                    "EXIT (выход из программы)\n\nВаша команда: ")

    # Выполняем команду
    if execute_instruction(command) == "exit":
        break

    # Выводим текущий стек после каждой команды
    print(f"\n=== Текущий стек: {stack} ===")
