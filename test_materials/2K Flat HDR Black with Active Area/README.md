# 2K Flat HDR Black with Active Area

## 1. 来源 (Location)
7.5.17, 7.5.32

## 2. 用途 (Purpose)
验证HDR模式下的最小黑电平和非活动区域漏光情况。

## 3. 特性 (Characteristics)

图像轨迹文件，包含1分钟的 2K flat 帧。每帧包含一个中心矩形区域，尺寸为 (1998×998) 填充代码值 (X″=0, Y″=0, Z″=0)。帧的其余部分填充代码值 (X″= 2234, Y″=1925, Z″=68)。配准标记代码值为 (X″=157, Y″=161, Z″=167) 位于中心矩形区域的四个角落。

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

文件路径: `2k_flat_hdr_black_active.tiff`
