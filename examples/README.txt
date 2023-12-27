1. 如何操作

打開兩個powershell
一個去 cd downloads/carla0.9.15/windowsnoeditor
另一個去 cd downloads/carla0.9.15/windowsnoeditor/pythonapi/examples
再第一個shell中，./carlaue4.exe
會到ue4啟動後，有畫面了，就可以把它視窗最小化
接著去另一個shell，python3 ./manual_traffic.py
接著會跳出兩個視窗，一個是全黑的操作視窗，另一個是車前鏡頭
將操作視窗一道螢幕下方，鏡頭畫面移到上方後，將滑鼠點擊操作視窗，即可開始開車
w: 前進
s:右轉
a:左轉
d:煞車
當今天發現開始恍神後，測試人員按下p鍵，在車子前方將出現行人
駕駛須躲避或是煞車，若躲過了，測試人員可重複使用p鍵呼叫出行人擋在車前
若撞到，在shell中會顯示從行人出現到撞到他花了多久時間。

2. 修改code
修改方向盤: 去#start ticking那邊會有throttle, brake, steer等值
可以修改數值以利測試，但不要太大避免車子過於敏感失控
修改行人出現: 去#start ticking的p鍵中的pedestrian function中的數值，
現在是1.5秒的距離出現，可視情況修改
修改車子限速: 去#limit speed中將20m/s調高或是調低。
改變天氣/背景: 去#town weather 修改數值，可參考carla waeather。

3. 除錯
無法連線: 打開工作管理員，將ue4結束工作，同時確認服務那邊是否有其他ue4 application都關掉了沒，
確認網路連線，重新開exe，再重新使用api連線
無法操作車子: 確認滑鼠有點擊到黑色的操作視窗，不然就重開一遍
