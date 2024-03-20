# Read-Plot3d-Grid-and-Flow-File-in-Python
Plot3d形式の格子ファイルと流れ場ファイルをPythonで読み込むためのプログラムです。

## 使用方法
### 実行方法
1. 以下のような[example.py][example.py-url]を作成し、同じディレクトリに[read_plot3d.py][read_plot3d.py-url]を置きます。
2. `python example.py`などで実行します。
```Python
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
```
### 実行結果
実行結果例は以下のようになります。
```Console
L3on@MacBook:Read-Plot3d-Grid-and-Flow-File-in-Python$ python example.py 
dict_items([('record marker type', '<i'), ('int type', '<i'), ('int byte length', 4), ('real type', '<f'), ('real byte length', 4)])
<i
(100, 100, 50, 3)
(100, 100, 50, 5)
dict_items([('Mach number', array([0.2], dtype=float32)), ('angle of attack', array([20.], dtype=float32)), ('Reynolds number', array([6500000.], dtype=float32)), ('iterations', array([0], dtype=int32))])
[0.3]
```

## 参考文献
1. ["Plot3d File Format for Grid and Solution Files". NPARC Alliance CFD Verification and Validation Web Site. (参照: 2024-03-19).][plot3d-NASA-url]
2. ["numpy.fromfile". NumPy v1.26 Manual. (参照: 2024-03-19).][NumPy-np.fromfile-url]

<!-- 使用したリンク -->
[Plot3d-NASA-url]: https://www.grc.nasa.gov/www/wind/valid/plot3d.html
[NumPy-np.fromfile-url]: https://numpy.org/doc/stable/reference/generated/numpy.fromfile.html
[example.py-url]: https://github.com/L3onSW/Read-Plot3d-Grid-and-Flow-File-in-Python/blob/master/example.py
[read_plot3d.py-url]: https://github.com/L3onSW/Read-Plot3d-Grid-and-Flow-File-in-Python/blob/master/read_plot3d.py
