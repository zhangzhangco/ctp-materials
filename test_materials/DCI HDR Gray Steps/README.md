# DCI HDR Gray Steps

## 1. 来源 (Location)
7.5.28

## 2. 用途 (Purpose)
验证HDR暗部传递函数。

## 3. 特性 (Characteristics)
HDR Picture Track File containing five seconds (120 frames) of a chart showing all gray step values in DCI-HDR Table 8. This is followed by the step values, each as a full frame with a duration of 50 s.

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.28要求：
1. 使用光谱仪测量每个梯级中心的亮度。
2. 验证测量值与目标值(Table 7.5.28(a))的误差在±5%以内。

### 素材文件验证
验证TIFF文件像素值符合HDR Gamma 2.6转换。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `DCI_HDR_Gray_Steps.tiff`