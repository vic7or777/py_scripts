# Quake II model's skins program modification
 Makes model's skins more contrasting for a better competition experience.

mdl_colored.py         - apply solid color with transparency
mdl_multicolored.py    - apply many colors by mask with transparency

## RU description
Скрипты для автоматизированной модификации текстур и скинов.
Позволяет сделать более контрастное изображение моделей, путем наложения цвета на оригинальные текстуры.
Цвет текстур для моделей игроков и предметов цвет задается в тексте скрипта.
На выходе генерируется пак файл.

mdl_colored.py       - закрашивает всю текстуру сплошным цветом с заданной прозрачностью.
mdl_multicolored.py  - закрашивает части текстуру по маске с заданной прозрачностью. В пак добавляется сам скрипт и исходные файлы.
                       Если распаковать пак, изменить цвета в тексте mdl_multicolored.py и запустить его, то пак пересоберется с новой раскраской.

## Example screenshots
### mdl_multicolored.py
![female skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake001.png?raw=true)
![male skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake002.png?raw=true)
![items skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake003.png?raw=true)
![ammo skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake004.png?raw=true)

### mdl_colored.py
![items skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake005.png?raw=true)
![ammo skin](https://github.com/vic7or777/py_scripts/blob/main/quake2%20models/pic/quake006.png?raw=true)
