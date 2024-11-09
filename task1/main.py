from typing import Generator


def sequence_generator(number: int) -> Generator:
    count = 0
    for i in range(1, number+1):
        for j in range(i):
            count += 1
            if count > number:
                return
            yield str(i)


if __name__ == '__main__':
    while True:
        n = input('Введите целое положительное число: ').strip()
        if n.isalpha() or int(n) <= 0:
            print(f'{n} не является целым положительным числом!'
                  'Попробуйте снова.')
        else:
            n = int(n)
            break

print(''.join(sequence_generator(n)))
