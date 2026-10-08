# Tic-Tac-Toe

משחק לוח <span style="color:blue">3</span>x<span style="color:blue">3</span> בטרמינל עם הסימנים `#` ו-`@`, בשני מצבים: שני שחקנים או משחק מול המחשב.

## הרצה

```bash
python Tictactoe.py
```

## איך משחקים

<span style="color:blue">1.</span> בחרו מצב:
- <span style="color:blue">1</span> — שני שחקנים
- <span style="color:blue">2</span> — מול המחשב

<span style="color:blue">2.</span> במשחק מול המחשב אפשר לבחור `#` (מתחיל) או `@`.

<span style="color:blue">3.</span> בכל תור בוחרים משבצת לפי מספרים <span style="color:blue">1</span>–<span style="color:blue">9</span>:

<pre>
<span style="color:blue">1</span> | <span style="color:blue">2</span> | <span style="color:blue">3</span>
--+---+--
<span style="color:blue">4</span> | <span style="color:blue">5</span> | <span style="color:blue">6</span>
--+---+--
<span style="color:blue">7</span> | <span style="color:blue">8</span> | <span style="color:blue">9</span>
</pre>

<span style="color:blue">4.</span> מנצחים בשורה, עמודה או אלכסון. אם הלוח מלא בלי ניצחון — תיקו.

## קובץ

- `Tictactoe.py` — הלוגיקה, התור, והמחשב (minimax)
