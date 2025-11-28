# Sequential Contrast and Uniformity Sequence

## 1. 来源 (Location)
7.5.15, 7.5.19, 7.5.23

## 2. 用途 (Purpose)
测量SDR顺序对比度及均匀性。

## 3. 特性 (Characteristics)
全白画面。亮度目标 48 cd/m² (CV 65535)。

## 4. 验证方法 (Verification)
**软件验证：**
```bash
identify -verbose <文件名>.tiff | grep -A 2 "min:"
python3 -c "import numpy as np; from PIL import Image; img=np.array(Image.open('<文件名>.tiff')); print(f'最小:{img.min()}, 最大:{img.max()}, 平均:{img.mean():.0f}')"
```
所有值应接近65535（允许量化误差）。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `Sequential_Contrast_and_Uniformity_Sequence.tiff`
