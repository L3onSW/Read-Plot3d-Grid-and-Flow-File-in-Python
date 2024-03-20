#!/opt/anaconda3/bin/python
# ======================================================================
# fortranのunformatted形式のPLOT3Dファイルの格子(grid)と流れ場(flow)を読み込む
# (ただし,シングルグリッド,IBLANKなしにのみ対応)
#
# Created on 2024/03/19, author: L3onSW
# ======================================================================
import read_plot3d

real_precision = "single"  # 実数の型: 単精度なら"single" or 倍精度なら"double"
record_marker_byte = 4  # レコードマーカのバイトサイズ: 4 or 8
endian = "little"  # バイトオーダ: "little" or "big"

grid_file = "./sample_plot3d.grid"  # 格子ファイル
flow_file = "./sample_plot3d.flow"  # 流れ場ファイル

# 格子ファイルと流れ場ファイルのフォーマットを取得
format = read_plot3d.format_setting(real_precision, record_marker_byte, endian)
# 格子(grid)の読み込み
grid = read_plot3d.read_grid(grid_file, format)
# 流れ場(flow)の読み込み
flow, parameter = read_plot3d.read_flow(flow_file, format)


# 簡単に結果を表示してみる
print(format.items())  # 辞書formatのキーと値のペアを表示
print(format["int type"])  # 辞書formatの中でキー"int type"に対応する値を表示

print(grid.shape)  # 格子ファイルのサイズ(jmax, kmax, lmax, 3)

print(flow.shape)  # 流れ場ファイルのサイズ(jmax, kmax, lmax, 5)

print(parameter.items())  # 辞書parameterのキーと値のペアを表示
print(parameter["Mach number"])  # 辞書parameterの中でキー"Mach number"に対応する値を表示
