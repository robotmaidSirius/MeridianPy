# MeridianPy

PythonでMeridianと接続するためのライブラリです

## インストール方法

```bash
pip install -U ./
```


## 関数一覧

| 関数                                                                | 説明                                 |
| ------------------------------------------------------------------- | ------------------------------------ |
| set_master_command(command : MasterCommand)                         | マスターコマンドを指定する           |
| set_acceleration(x, y, z)                                           | 加速度センサーの値を設定する         |
| set_gyro(x, y, z)                                                   | ジャイロセンサーの値を設定する       |
| set_magnet(x, y, z)                                                 | 磁気センサーの値を設定する           |
| set_temperature(temp)                                               | 温度を設定する                       |
| set_dmp_direction(roll, pitch, yaw)                                 | DMP値を設定する                      |
| set_remote_buttons(button : PadState)                               | PADのボタン値を設定する              |
| set_mrd_motion_frames(frames, stop_frames)                          | モーションフレームを設定する         |
| set_mrd_motion_data(index, motion_command1, motion_command2, value) | モーション（サーボ）の情報を設定する |
| set_mrd_user_data(index, data)                                      | 任意のユーザ用データを設定する       |
| set_error_code(error_code)                                          | エラーコードを設定する               |
| clear_error_code()                                                  | 設定したエラーコードを解除する       |
| start_receive_message(ip="localhost", port=22222)                   | 受信ポートをオープンする             |
| send()                                                              | 設定したデータを送信する             |
| receive()                                                           | 受信したデータを取得する             |

