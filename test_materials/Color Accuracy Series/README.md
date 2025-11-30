# Color Accuracy Series

## 1. 来源 (Location)
7.5.12

## 2. 用途 (Purpose)
验证SDR色彩准确性。

## 3. 特性 (Characteristics)
包含12个色块，分为两排：
- 第一排 (Row 1): Red-1, Green-1, Blue-1, Cyan-1, Magenta-1, Yellow-1 (高饱和度)
- 第二排 (Row 2): Red-2, Green-2, Blue-2, Cyan-2, Magenta-2, Yellow-2 (次级色/色彩偏移)
分辨率: 2048 x 1080 (2K) & 4096 x 2160 (4K).
背景: 纯黑.
文字: 包含详细的xyY和12-bit XYZ数值。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.12要求：
1. 使用光谱仪测量色块的亮度和色度坐标(x, y)。
2. 验证色度坐标与目标值的误差在Review Room Tolerances内。
3. 验证亮度误差在±3%以内。

### 素材文件验证
验证TIFF文件RGB/XYZ值符合目标色度坐标的转换结果。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。

文件路径: 
- `Color_Accuracy_Series.tiff`: 分辨率 2048x1080 (DCI 2K)
- `Color_Accuracy_Series_4K.tiff`: 分辨率 4096x2160 (DCI 4K)
