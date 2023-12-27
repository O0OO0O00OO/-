^Enter::
CoordMode, Mouse , Screen
delay := 20
__ClickX:=753
__ClickY:=1064
__ClickTimes:=1
Click %__ClickX%, %__ClickY%, %__ClickTimes%
Sleep % delay
Send, !e
Sleep % delay
Send, s
Sleep % delay
Send, !e
Sleep % delay
Send, a
Sleep % delay
__ClickX:=1860
__ClickY:=940
__ClickTimes:=1
Click %__ClickX%, %__ClickY%, %__ClickTimes%
Sleep % 4000
Send, !e
Sleep % delay
Send, s
Sleep % delay
Send, !e
Sleep % delay
Send, p
Sleep % delay
Send, w
Sleep % delay
;縮小
__ClickX:=753
__ClickY:=1064
__ClickTimes:=1
Click %__ClickX%, %__ClickY%, %__ClickTimes%
Sleep % delay
__ClickX:=14
__ClickY:=209
__ClickTimes:=5
Click %__ClickX%, %__ClickY%, %__ClickTimes%
Sleep % delay
Send, ^v
Sleep % delay
Send, {Enter}
Sleep % delay
Send, ^s
Sleep % delay
Sleep % delay
__ClickX:=1832
__ClickY:=49
__ClickTimes:=1
Click %__ClickX%, %__ClickY%, %__ClickTimes%
Return


^Esc::
CoordMode, Mouse , Screen
MouseGetPos, 滑鼠座標X, 滑鼠座標Y
Msgbox % "現在滑鼠座標為: " . 滑鼠座標X . ", " . 滑鼠座標Y
Return


