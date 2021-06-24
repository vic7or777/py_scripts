# Quake II textures program modification
 Makes textures more contrasting for a better competition experience.

## RU description
Скрипты для автоматизированной модификации текстур и скинов.
Позволяет сделать более контрастное изображение, путем наложения цвета на оригинальные текстуры.
Цвет определяется автоматически из самой текстуры.
Для моделей игроков и предметов цвет скина задается в тексте скрипта.
В отличии от picmip не приводит к замыливанию.
На выходе генерируется пак файлы.

## Example screenshots
### blend 85% textures vs original
pak9_monocolor_blend_0.85.pak + mdl_colored.pak
![pak9_monocolor_blend_0.85.pak](https://github.com/vic7or777/py_scripts/blob/main/quake2%20textures/pic/quake017.png?raw=true)
original textures
![original textures](https://github.com/vic7or777/py_scripts/blob/main/quake2%20textures/pic/quake018.png?raw=true)

### blend 100% textures vs original picmiped
pak9_monocolor_blend_1.00.pak + mdl_colored.pak
![pak9_monocolor_blend_1.00.pak](https://github.com/vic7or777/py_scripts/blob/main/quake2%20textures/pic/quake019.png?raw=true)
original textures + gl_picmip 10
![original textures + gl_picmip 10](https://github.com/vic7or777/py_scripts/blob/main/quake2%20textures/pic/quake020.png?raw=true)
