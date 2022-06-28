# Micro Stocker Helpers

Серия скриптов для улучшения опыта работы с микростоками (фотобанками). 

## Shutterstock Keywords

Добавляет ключевые слова, которые можно выделить и скопировать, для каждой работы на шаттерстоке.
Добавляет позицию работы в рейтинге на [m-rank](https://m-rank.net) для векторных работ и показывает дату загрузки.

Как это выглядит:

![Shutterstock Keywords](https://github.com/TpuPyku/MicroStockerHelpers/blob/master/images/shutter.png)

### Как использовать скрипт
  - Скопировать скрипт
  - Установить расширение для браузера [Tampermonkey](http://tampermonkey.net/) 
    - Create new script... -> Вставить -> Сохранить
  - После обновления страницы скрипт работает.

## Canva Key

Утилита для переноса метаданных с .JPG файлов на .PNG для последующей зарузки их на Канву.
Потенциально скрипт должен работать при установленном Python 3 на Win, Linux, Mac. Проверенно только на Windows.

Скомпилированный для Windows x64 - [скачать](https://github.com/TpuPyku/MicroStockerHelpers/blob/master/Canva/CanvaKey/bin)

### Как использовать
  - Подготовить файлы для переноса. Имена у пар jpg и png должны быть одинаковые (bear1.jpg, bear1.png; frog.jpg, frog.png).
  - Скопировать файлы, сделать бекап. Очень редко, но иногда файлы портятся.
  - Запустить утилиту.
  - Выбрать папку с jpg файлами.
  - Выбрать папку с png файлами.
  - Папки не обязательно разные, файлы могут лежать в одной.
  - Нажать Start.
  - Возможно дополнительно придётся скачать модуль [Exiv2](https://exiv2.org/) и разархивировать в CanvaKey/exiv2/Windows(ваша система)/exiv2.exe и exiv2.dll. Он есть в дистрибутиве, но вдруг эта информация пригодиться.

  Как это выглядит:

![Canva Key](https://github.com/TpuPyku/MicroStockerHelpers/blob/master/images/canva.png)

PS: Когда-нибудь дойдут руки прикрутить перенос меты в .EPS, есть возможность через [ExifTool](https://exiftool.org)...
