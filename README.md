# MeridianPy

PythonでMeridianと接続するためのライブラリです

## インストール方法

```bash
# コードからインストール
pip install -U ./

# Wheelを作成してインストール
python -m build .
cd dist
pip install -U [ビルドした.whl]

# githubからインストール (タグ指定する場合は、`@v0.0.1`のようにURLに追加することで指定できます)
pip install meridian@git+https://github.com/robotmaidSirius/MeridianPy.git
```

## クラス一覧

| クラス        | 説明                   |
| ------------- | ---------------------- |
| Net           | 通信用クラス           |
| MasterCommand | マスターコマンド構造体 |
| PadState      | Padボタンクラス        |

## 関数一覧

| 関数                                                  | 説明                     |
| ----------------------------------------------------- | ------------------------ |
| Net.start_receive_message(ip="localhost", port=22222) | 受信ポートをオープンする |
| Net.send()                                            | 設定したデータを送信する |
| Net.receive()                                         | 受信したデータを取得する |

| 関数                                                                | 説明                                 |
| ------------------------------------------------------------------- | ------------------------------------ |
| Net.set_master_command(command : MasterCommand)                     | マスターコマンドを指定する           |
| Net.set_acceleration(x, y, z)                                       | 加速度センサーの値を設定する         |
| Net.set_gyro(x, y, z)                                               | ジャイロセンサーの値を設定する       |
| Net.set_magnet(x, y, z)                                             | 磁気センサーの値を設定する           |
| Net.set_temperature(temp)                                           | 温度を設定する                       |
| Net.set_dmp_direction(roll, pitch, yaw)                             | DMP値を設定する                      |
| Net.set_pad(button : PadState)                                      | PADのボタン値を設定する              |
| Net.set_motion_frames(frames, stop_frames)                          | モーションフレームを設定する         |
| Net.set_motion_data(index, motion_command1, motion_command2, value) | モーション（サーボ）の情報を設定する |
| Net.set_user_data(index, data)                                      | 任意のユーザ用データを設定する       |
| Net.set_error_code(error_code)                                      | エラーコードを設定する               |
| Net.clear_error_code()                                              | 設定したエラーコードを解除する       |
