# Pixel Structure Pattern N 4k

## 1. 来源 (Location)
7.5.3

## 2. 用途 (Purpose)
验证显示设备的像素计数和结构。

## 3. 特性 (Characteristics)
2048x1080图像，包含128x67个16x16像素块。每个块包含二进制编码的坐标索引和颜色条带。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.3要求：
1. 在屏幕上完整显示该图案。
2. 目视检查像素结构是否完整，无截断、缩放或伪影。
3. 验证最外层像素是否可见。

### 素材文件验证
验证TIFF文件尺寸为2048x1080，且包含预期的网格结构。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `Pixel_Structure_Pattern_N_4k.tiff`
