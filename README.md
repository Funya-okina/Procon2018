# 概要

procon29

## runServer.py
### 起動方法
依存ライブラリ，ソフトウェアのインストール
まずはpython用
```
pip install pillow
pip install opencv-python
pip install pyzbar
pip install qrcode
pip install numpy
pip install eel
```
OSによってはzbarというソフトウェアをインストールしておかないとライブラリ参照にエラーが出ます．  
  
ArchLinux
```
sudo pacman -S zbar
```
Mac OS (ネット情報．動作未確認)
```
brew install zbar
```

全部できたら
```
python runServer.py
```

これで起動できる．

## クラス達
### Server
runServer.py内で宣言．サーバーのUIと通信のためのクラス．
### decodeQR, encodeQR
QRLib.py内で宣言．QRコード生成と読み込みの処理を行う．
### Board
Board.py内で宣言．盤面情報を管理するクラス．
