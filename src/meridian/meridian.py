#!python

import numpy
import asyncio
import socket
from contextlib import closing
from enum import Enum
import datetime

class PadState(Enum):
    START : bool
    SELECT : bool
    UP : bool
    RIGHT : bool
    DOWN : bool
    LEFT : bool
    L1 : bool
    L2 : bool
    L3 : bool
    R1 : bool
    R2 : bool
    R3 : bool
    D : bool
    B : bool
    A : bool
    C : bool
    L_STICK_HORIZONTAL : int
    L_STICK_VERTICAL : int
    L_ANALOG_STICK : int
    R_STICK_HORIZONTAL : int
    R_STICK_VERTICAL : int
    R_ANALOG_STICK : int

class MasterCommand(Enum):
    TORQUE_ALL_OFF          = 0         # すべてのサーボトルクをオフにする（脱力）
    UPDATE_YAW_CENTER       = 10002     # センサの推定ヨー軸を現在値でゼロに
    ENTER_TRIM_MODE         = 10003     # トリムモードに入る(現在不使用)
    CLEAR_SERVO_ERROR_ID    = 10004     # 通信エラーのサーボのIDをクリア
    BOARD_TRANSMIT_ACTIVE   = 10005     # ボードが定刻で送信を行うモード（デフォルト設定.PC側が受信待ち）
    BOARD_TRANSMIT_PASSIVE  = 10006     # ボードが受信を待ち返信するモード（PC側が定刻送信）
    RESET_MRD_TIMER         = 10007     # フレーム管理時計mrd_t_milを現在時刻にリセット

class Net:
    MESSAGE_SIZE = 90                   # Meridim配列の長さ(デフォルトは90)
    is_debug = False                    # デバッグモードのフラグ
    _send_ip="localhost"                # 送信先のIPアドレス
    _send_port=22224                    # 送信先のポート番号
    _send_data = [0] * MESSAGE_SIZE     # 送信するデータ
    _receive_data = [0] * MESSAGE_SIZE  # 受信するデータ
    _is_receiving = False               # 受信中のフラグ

    def set_master_command(self, command : MasterCommand):
        # マスターコマンドを設定する
        self._send_data[0] = command.value
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set master command: {command.name}")
    def set_acceleration(self, x, y, z):
        # 加速度センサ値を設定する
        self._send_data[2] = int(x)
        self._send_data[3] = int(y)
        self._send_data[4] = int(z)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set acceleration: x={x}, y={y}, z={z}")
    def set_gyro(self, x, y, z):
        # ジャイロセンサ値を設定する
        self._send_data[5] = int(x)
        self._send_data[6] = int(y)
        self._send_data[7] = int(z)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set gyro: x={x}, y={y}, z={z}")
    def set_magnet(self, x, y, z):
        # 磁気コンパス値を設定する
        self._send_data[8] = int(x)
        self._send_data[9] = int(y)
        self._send_data[10] = int(z)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set magnet: x={x}, y={y}, z={z}")
    def set_temperature(self, temp):
        # 温度センサ値を設定する
        self._send_data[11] = int(temp)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set temperature: {temp}")
    def set_dmp_direction(self, roll, pitch, yaw):
        # DMP推定方向値を設定する
        self._send_data[12] = int(roll)
        self._send_data[13] = int(pitch)
        self._send_data[14] = int(yaw)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set DMP direction: roll={roll}, pitch={pitch}, yaw={yaw}")
    def set_remote_buttons(self, buttons, stick_l, stick_r, l2r2analog):
        # TODO: ボタンの定義する
        # リモコンボタン、スティック、アナログ値を設定する
        self._send_data[15] = int(buttons)
        self._send_data[16] = int(stick_l)
        self._send_data[17] = int(stick_r)
        self._send_data[18] = int(l2r2analog)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set remote buttons: buttons={buttons}, stick_l={stick_l}, stick_r={stick_r}, l2r2analog={l2r2analog}")
    def set_remote_buttons(self, button: PadState):
        self._send_data[15] = (   1 if button.SELECT else 0) \
                            + (   2 if button.R3 else 0) + (   4 if button.L3 else 0) \
                            + (   8 if button.START else 0) \
                            + (  16 if button.UP else 0) + (  32 if button.RIGHT else 0) + (  64 if button.DOWN else 0) + ( 128 if button.LEFT else 0) \
                            + ( 256 if button.L2 else 0) + ( 512 if button.R2 else 0) \
                            + (1024 if button.L1 else 0) + (2048 if button.R1 else 0) \
                            + (4096 if button.B else 0)  + (8192 if button.D else 0) + (16384 if button.A else 0) + (32768 if button.C else 0)
        self._send_data[16] = ((int(button.L_STICK_HORIZONTAL) & 0xFF) << 8) | (int(button.L_STICK_VERTICAL) & 0xFF)
        self._send_data[17] = ((int(button.R_STICK_HORIZONTAL) & 0xFF) << 8) | (int(button.R_STICK_VERTICAL) & 0xFF)
        self._send_data[18] = ((int(button.R_ANALOG_STICK)     & 0xFF) << 8) | (int(button.L_ANALOG_STICK)   & 0xFF)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set remote buttons: buttons={buttons}, stick_l={stick_l}, stick_r={stick_r}, l2r2analog={l2r2analog}")


    def set_mrd_motion_frames(self, frames, stop_frames):
        # モーション設定のフレーム数を設定する
        self._send_data[19] = ((int(frames) & 0xFF) << 8) | (int(stop_frames) & 0xFF)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set MRD motion frames: frames={frames}, stop_frames={stop_frames}")
    def set_mrd_motion_data(self, index, motion_command1, motion_command2, value):
        if index < 0 or index >= 30:
            raise ValueError("Index out of range")
        self._send_data[(index*2) + 20] = ((int(motion_command1) & 0xFF) << 8) | (int(motion_command2) & 0xFF)
        self._send_data[(index*2) + 21] = int(value)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set MRD motion data: index={index}, data={data}")
    def set_mrd_user_data(self, index, data):
        # 80 から
        # ユーザーデータを設定する
        if index < 0 or index >= 8:
            #raise ValueError("Index out of range")
            return False
        self._send_data[index + 80] = int(data)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set MRD user data: index={index}, data={data}")
    def set_error_code(self, error_code):
        # エラーコードを設定する
        self._send_data[88] |= int(error_code)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set error code: {error_code}")
    def clear_error_code(self):
        # エラーコードをクリアする
        self._send_data[88] = 0
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Clear error code")

    def _set_checksum(self, data):
        # チェックサムを設定する
        checksum = 0
        for i in range(0, Net.MESSAGE_SIZE - 1):
            checksum += data[i]
        checksum = checksum & 0xFFFF
        # 2の補数で設定
        data[Net.MESSAGE_SIZE - 1] = ((~checksum)+1) & 0xFFFF
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Set checksum: {checksum}")
    def _check_checksum(self, data):
        # チェックサムを確認する
        checksum = 0
        for i in range(0, Net.MESSAGE_SIZE):
            checksum = (checksum + data[i]) & 0xFFFF
        if(checksum & 0xFFFF) != 0:
            return False
        else:
            return True

    def __init__(self, send_ip, send_port=22224):
        self._receive_data = numpy.zeros(Net.MESSAGE_SIZE, dtype=numpy.uint16)
        self._send_data = numpy.zeros(Net.MESSAGE_SIZE, dtype=numpy.uint16)
        self._send_ip = send_ip
        self._send_port = send_port
        if self.is_debug:
            print(f"{datetime.datetime.now()} : IP address set to {self._send_ip} and port set to {self._send_port}")

    def start_receive_message(self, ip="localhost", port=22222):
        self._is_receiving = False
        asyncio.run(self._receive(ip, port))

    def send(self):
        data = self._send_data
        # バッファーから送信データを詰め込む
        index = self._receive_data[1] if self._send_data[1] > self._send_data[1] else self._send_data[1]
        data[1] = index + 1 if index <= 59998 else index - 59999
        self._send_data[1] = data[1]
        self._set_checksum(data)        # チェックサム計算する
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.sendto(data, (self._send_ip, self._send_port))
            if self.is_debug:
                print(f"{datetime.datetime.now()} : Sent data to {self._send_ip}:{self._send_port}")
        return self._send_data

    def receive(self):
        # 受信データを設定する
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Received data: {self._receive_data}")
        data = self._receive_data
        if self._receive_data[1] > self._send_data[1]:
            self._send_data = data
        return data

    async def _receive(self, ip, port):
        await asyncio.sleep(1)
        if self.is_debug:
            print(f"{datetime.datetime.now()} : Listening on {ip}:{port}")
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind((ip, port))
            if self.is_debug:
                print(f"Listening on {self._receive_send_ip}:{self._receive_port}")
            self._is_receiving = True
            while self._is_receiving:
                data, addr = sock.recvfrom(Net.MESSAGE_SIZE)
                if len(data) == Net.MESSAGE_SIZE:
                    if(self._check_checksum(data)):
                        self._receive_data = numpy.frombuffer(data, dtype=numpy.uint16)
                        if self.is_debug:
                            print(f"{datetime.datetime.now()} :Received data from {addr}: {self._receive_data}")
                    else:
                        if self.is_debug:
                            print(f"{datetime.datetime.now()} :Received data checksum error.")
                else:
                    if self.is_debug:
                        print(f"{datetime.datetime.now()} :Received data length mismatch.")
