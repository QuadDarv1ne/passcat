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

## Лицензия

Этот код распространяется под свободной лицензией [license](LICENSE.txt), вы welcome to fork it.

Словари находятся в директории `passcat/wordlists/`.
Основной код — в `passcat/passcat.py`.