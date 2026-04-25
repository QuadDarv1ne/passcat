# Passcat (на русском)

Passcat позволяет генерировать криптографически стойкие, запоминающиеся пароли-фразы.

## Установка

``pip install passcat``

## Использование

Базовое использование:

```
$ passcat
throng disregard overall trimming playpen persevere
```

Указать количество слов:

```
$ passcat 5
relight usage geologic tumbling disown
```

или

```
$ passcat --count 5
relight usage geologic tumbling disown
```

Показать доступные словари:

```
$ passcat -l

Eff
English
French
German
Indonesian
Italian
Spanish
```

Указать словарь помимо EFF:

```
$ passcat -w spanish
latitar reglamentaria apanuscadora consultable carbunclo duplicar paragueria cincoanal
```

Указать путь к альтернативному словарю:

``$ passcat -f /path/to/wordlist/file.txt``

Указать разделитель между словами (по умолчанию пробел):

```
$ passcat 3 --separator '-'
correct-horse-battery
```

Генерировать несколько фраз за раз:

```
$ passcat 2 -n 3
word1 word2
word3 word4
word5 word6
```

Капитализировать первую букву каждого слова:

```
$ passcat 2 -C
Apple Banana
Cherry Date
```

Перевести все буквы в верхний регистр:

```
$ passcat 2 -U
APPLE BANANA
CHERRY DATE
```

Комбинировать опции:

```
$ passcat 2 -n 2 -C --separator '.'
Apple.Banana
Cherry.Date
```

## Лицензия

Этот код распространяется под свободной лицензией [license](LICENSE.txt), вы welcome to fork it.

Словари находятся в директории `passcat/wordlists/`.
Основной код — в `passcat/passcat.py`.