# 2K Scope SDR Black with Marks

## 1. 来源 (Location)
7.5.18

## 2. 用途 (Purpose)
验证SDR模式下，非活动区域（Inactive Area）是否发光。Marks用于定位，Active Area用于验证红光溢出。

## 3. 特性 (Characteristics)
图像轨迹文件，包含1分钟的 2K Scope 帧，每帧填充像素代码值 (X'=0, Y'=0, Z'=0)，但帧的每个角落都有代码值为 (X'=122, Y'=128, Z'=125) 的配准标记。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.29要求：
1. 使用光谱仪按照ICDM IDMS 'full-screen black' procedure测量亮度。
2. 验证亮度值符合SDR Minimum Active Black Level要求。

### 素材文件验证
验证TIFF文件所有像素值为0。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `2K_Scope_SDR_Black_with_Marks.tiff`