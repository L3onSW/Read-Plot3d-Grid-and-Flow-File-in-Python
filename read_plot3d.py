#!/opt/anaconda3/bin/python
# ======================================================================
# fortranのunformatted形式のPLOT3Dファイルの格子(grid)と流れ場(flow)を読み込む
# (ただし,シングルグリッド,IBLANKなしにのみ対応)
#
# Created on 2022/01/07, author: L3onSW
# ======================================================================
import sys
import numpy as np


def format_setting(real_precision, record_marker_byte, endian):
    format = {}
    """format_setting
    Plot3d形式のfortran unformattedファイルを
    開くために必要なフォーマットを辞書formatに格納

    Args:
        real_precision (str):
            実数の型(単精度なら"single", 倍精度なら"double")
        record_marker_byte (int):
            レコードマーカのバイトサイズ(4 or 8)
        endian (str):
            バイトオーダ(リトルエンディアンなら"little", ビッグエンディアンなら"big")

    Returns:
        format (dict):
            Plot3d形式のfortran unformattedファイルを開くために必要なフォーマット
                format["record marker type"] = "<i" or ">i" or "<q" or ">q"
                format["int type"] = "<i" or ">i"
                format["int byte length"] = 4
                format["real type"] = "<f" or ">f" or "<d" or ">d"
                format["real byte length"] = 4 or 8

    記号の見方は以下の通り
        > ビッグエンディアン(big endian: 桁の大きい方から順番に格納)
        < リトルエンディアン(little endian: 桁の小さい方から順番に格納)
        i 整数型(int型)
        f 単精度浮動小数点型(float型)
        d 倍精度浮動小数点型(double型)
        q 整数型(long long型)
        バイト数: 4 or 8
            (ちなみに,1 byte = 8 bit なので,
             4 byte = 32 bit, 8 byte = 64 bit)
    """
    # ------------------------------------------------------------------
    # レコードマーカ(record marker)について以下を定める
    # # 型(int型 or long long型)
    # # バイトオーダ(リトルエンディアン or ビッグエンディアン)
    # ------------------------------------------------------------------
    if record_marker_byte == 4:
        if endian == "little":
            format["record marker type"] = "<i"
        elif endian == "big":
            format["record marker type"] = ">i"
        else:
            print("変数endianには\"big\"か\"little\"を代入してください")
            sys.exit(1)
    elif record_marker_byte == 8:
        if endian == "little":
            format["record marker type"] = "<q"
        elif endian == "big":
            format["record marker type"] = ">q"
        else:
            print("変数endianには\"big\"か\"little\"を代入してください")
            sys.exit(1)
    else:
        print("変数record_marker_byteには4か8を代入してください")
        sys.exit(1)
    # ------------------------------------------------------------------
    # 整数について以下を定める
    # # 型(int型)
    # # バイト数(4)
    # # バイトオーダ(リトルエンディアン or ビッグエンディアン)
    # ------------------------------------------------------------------
    if endian == "little":
        format["int type"] = "<i"
        format["int byte length"] = 4
    elif endian == "big":
        format["int type"] = ">i"
        format["int byte length"] = 4
    else:
        print("変数endianには\"big\"か\"little\"を代入してください")
        sys.exit(1)
    # ------------------------------------------------------------------
    # 実数について以下を定める
    # # 型(単精度浮動小数点型(float型) or 倍精度浮動小数点型(double型))
    # # バイト数(4 or 8)
    # # バイトオーダ(リトルエンディアン or ビッグエンディアン)
    # ------------------------------------------------------------------
    if real_precision == "single":
        if endian == "little":
            format["real type"] = "<f"
            format["real byte length"] = 4
        elif endian == "big":
            format["real type"] = ">f"
            format["real byte length"] = 4
        else:
            print("変数endianには\"big\"か\"little\"を代入してください")
            sys.exit(1)
    elif real_precision == "double":
        if endian == "little":
            format["real type"] = "<d"
            format["real byte length"] = 8
        elif endian == "big":
            format["real type"] = ">d"
            format["real byte length"] = 8
        else:
            print("変数endianには\"big\"か\"little\"を代入してください")
            sys.exit(1)
    else:
        print("変数real_precisionには", end="")
        print("\"single\"か\"double\"を代入してください")
        sys.exit(1)
    # ------------------------------------------------------------------
    # 結果を戻り値として返す
    # ------------------------------------------------------------------
    return format


def read_grid(grid_file, format):
    """read_grid
    格子を読み込む

    Args:
        grid_file (str): 拡張子を含む格子ファイルへのパス
        format (dict): 関数format_settingの戻り値の辞書

    Returns:
        grid: (jmax,kmax,lmax,3)の格子
    """
    int_byte_length = 4  # int型のbyte長
    dimension = 3  # 次元数(2にしても2次元で使えないが次元に関係する部分を示している)
    with open(grid_file, "r") as f:
        # --------------------------------------------------------------
        # 空間サイズ読み込み
        # --------------------------------------------------------------
        # 空間サイズ(格子サイズ)読み込み前のレコードマーカ
        record_marker_header = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 空間サイズ(格子サイズ)読み込み前のレコードマーカが正しく読めない場合は異常終了
        if record_marker_header != int_byte_length*dimension:
            print("変数record_marker_byteの値が違うようです")
            print("正しいレコードマーカのバイト数を指定してから", end="")
            print("再度実行してください")
            sys.exit(1)
        # 空間サイズ(格子サイズ)読み込み
        jmax = int(np.fromfile(f, dtype=format["int type"], count=1))
        kmax = int(np.fromfile(f, format["int type"], count=1))
        lmax = int(np.fromfile(f, dtype=format["int type"], count=1))
        # 空間サイズ(格子サイズ)読み込み後のレコードマーカ
        record_marker_footer = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # --------------------------------------------------------------
        # 格子(grid)読み込み
        # --------------------------------------------------------------
        # 格子(grid)読み込み前のレコードマーカ
        record_marker_header = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 格子(grid)が書き込まれている部分の長さをdata_lengthに格納
        data_length = jmax * kmax * lmax * dimension
        # 格子(grid)読み込み
        grid = \
            np.fromfile(f, dtype=format["real type"], count=data_length)
        # 格子(grid)読み込み後のレコードマーカ
        record_marker_footer = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 格子(grid)読み込み前後のレコードマーカが異なる場合は異常終了する
        if record_marker_header != record_marker_footer:
            print("変数real_precisionの値が違うようです")
            print("正しい実数の精度(単精度 or 倍精度)を指定してから", end="")
            print("再度実行してください")
            sys.exit(1)
    # ------------------------------------------------------------------
    # 読み込んだgridを[jmax,kmax,lmax,3]型に変換
    # ------------------------------------------------------------------
    grid = np.reshape(grid, [jmax, kmax, lmax, dimension], order='F')
    # ------------------------------------------------------------------
    # grid(格子)を返す
    # ------------------------------------------------------------------
    return grid


def read_flow(flow_file, format):
    """read_flow
    流れ場を読み込む

    Args:
        grid_file (str): 拡張子を含む格子ファイルへのパス
        format (dict): 関数format_settingの戻り値の辞書

    Returns:
        flow: (jmax,kmax,lmax,5)の流れ場(シミュレーション結果)
        parameter (dict): マッハ数,迎角,レイノルズ数,繰り返し回数
    """
    parameter = {}
    int_byte_length = 4  # int型のbyte長
    dimension = 3  # 次元数(2にしても2次元で使えないが次元に関係する部分を示している)
    # fnameで指定したファイルを読み込みモード(r)で開く
    with open(flow_file, 'r') as f:
        # --------------------------------------------------------------
        # 空間サイズ(jmax,kmax,lmax)読み込み
        # --------------------------------------------------------------
        # 空間サイズ(格子サイズ)読み込み前のレコードマーカ
        record_marker_header = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 空間サイズ(格子サイズ)読み込み前のレコードマーカが正しく読めない場合は異常終了
        if record_marker_header != int_byte_length*dimension:
            print("変数record_marker_byteの値が違うようです")
            print("正しいレコードマーカのバイト数を指定してから", end="")
            print("再度実行してください")
            sys.exit(1)
        # 空間サイズ(格子サイズ)読み込み
        jmax = int(np.fromfile(f, dtype=format["int type"], count=1))
        kmax = int(np.fromfile(f, dtype=format["int type"], count=1))
        lmax = int(np.fromfile(f, dtype=format["int type"], count=1))
        # 空間サイズ(格子サイズ)読み込み後のレコードマーカ
        record_marker_footer = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # --------------------------------------------------------------
        # パラメータ(マッハ数,迎角,レイノルズ数,繰り返し回数)読み込み
        # --------------------------------------------------------------
        # パラメータ(マッハ数,迎角,レイノルズ数,繰り返し回数)読み込み前のレコードマーカ
        record_marker_header = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # マッハ数(Mach number)
        parameter["Mach number"] = \
            np.fromfile(f, dtype=format["real type"], count=1)
        # 迎角(angle of attack)
        parameter["angle of attack"] = \
            np.fromfile(f, dtype=format["real type"], count=1)
        # レイノルズ数(Reynolds number)
        parameter["Reynolds number"] = \
            np.fromfile(f, dtype=format["real type"], count=1)
        # 繰り返し回数
        parameter["iterations"] = \
            np.fromfile(f, dtype=format["int type"], count=1)
        # パラメータ(マッハ数,迎角,レイノルズ数,繰り返し回数)読み込み後のレコードマーカ
        record_marker_footer = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # パラメータ読み込み前後のレコードマーカが異なる場合は異常終了する
        if record_marker_header != record_marker_footer:
            print("変数real_precisionの値が違うようです")
            print("正しい実数の精度(単精度 or 倍精度)を指定してから", end="")
            print("再度実行してください")
            sys.exit(1)
        # ------------------------------------------------------------------
        # 流れ場(flow)読み込み
        # ------------------------------------------------------------------
        # 空間サイズ(格子サイズ)読み込み前のレコードマーカ
        record_marker_header = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 流れ場(flow)が書き込まれている部分の長さをdata_lengthに格納
        data_length = jmax * kmax * lmax * 5
        # 流れ場(flow)読み込み
        flow = \
            np.fromfile(f, dtype=format["real type"], count=data_length)
        # 流れ場(flow)読み込み後のレコードマーカ
        record_marker_footer = \
            np.fromfile(f, dtype=format["record marker type"], count=1)
        # 流れ場(flow)読み込み前後のレコードマーカが異なる場合は異常終了する
        if record_marker_header != record_marker_footer:
            print("変数real_precisionの値が違うようです")
            print("正しい実数の精度(単精度 or 倍精度)を指定してから", end="")
            print("再度実行してください")
            sys.exit(1)
    # ------------------------------------------------------------------
    # 読み込んだ流れ場(flow)を[jmax,kmax,lmax,5]型に変換
    # ------------------------------------------------------------------
    flow = np.reshape(flow, [jmax, kmax, lmax, 5], order='F')
    # ------------------------------------------------------------------
    # 流れ場(flow)と
    # パタメータ(マッハ数,迎角,レイノルズ数,繰り返し回数)の辞書(parameter)
    # を返す
    # ------------------------------------------------------------------
    return flow, parameter
