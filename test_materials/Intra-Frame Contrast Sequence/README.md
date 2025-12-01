# Intra-Frame Contrast Sequence

## 1. 来源 (Location)

7.5.8

## 2. 用途 (Purpose)

测量帧内对比度（棋盘格对比度）。

## 3. 特性 (Characteristics)
帧内对比度对准图。详见第7.5.19节。

## 4. 验证方法 (Verification)

**目视检查：** 确认图像为4x4黑白相间棋盘格。

**软件验证：**

```bash
# 采样左上角白色块和相邻黑色块
python3 -c "import numpy as np; from PIL import Image; img=np.array(Image.open('<文件名>.tiff')); h,w=img.shape[:2]; bh,bw=h//4,w//4; white=img[bh//2,bw//2]; black=img[bh//2,bw+bw//2]; print(f'白块:{white.max()}, 黑块:{black.max()}')"
```

白块应接近65535，黑块应接近0。

## 5. 素材状态 (Material Status)

✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `Intra-Frame_Contrast_Sequence.tiff`

### 2K Aiming Target (Intra-Frame Contrast Target)

用于仪器对准的 2K 目标图。

* **尺寸**: 2048 x 1080
* **背景**: RGB (50, 50, 50)
* **内容**: 4x4 十字准星 + 数字标号 + 中央标题
* **文件路径**: `Intra-Frame_Contrast_Target_2K.tiff`