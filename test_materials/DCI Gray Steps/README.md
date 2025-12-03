# DCI Gray Steps

## 1. 来源 (Location)
7.5.11, 7.5.9

## 2. 用途 (Purpose)
验证SDR暗部传递函数。

## 3. 特性 (Characteristics)
MXF track file containing five seconds (120 frames) of a chart showing all gray step values in Table A.2.15. This is followed by the step values, each as a full frame with a duration of 50 s.

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.9要求：
1. 使用光谱仪(Spectroradiometer)测量每个梯级中心的亮度。
2. 减去黑电平(Black Level)。
3. 验证测量值与目标值(Table 7.5.11(a))的误差在±5%以内。

### 素材文件验证
使用Python脚本读取TIFF文件像素值，验证其Code Value符合Gamma 2.6转换公式。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `DCI_Gray_Steps.tiff`