# 4K Scaling Test Patterns

## 1. 来源 (Location)
7.5.25

## 2. 用途 (Purpose)
验证图像缩放伪影（Aliasing, Ringing, Jaggies）。

## 3. 特性 (Characteristics)
包含10秒图A.2.254所示4K帧的图像轨迹文件，由以下部分组成：(a) 帧左侧，不同角度和颜色的连续1像素线段及一个小灰色方块；(b) 帧右侧，波长为2像素的波带片(Zone Plate)。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.25要求：
1. 显示图案并观察是否存在混叠(Aliasing)或振铃(Ringing)现象。
2. 验证图像缩放处理的质量。

### 素材文件验证
验证TIFF文件包含预期的测试图样元素。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `4K_Scaling_Test_Patterns.tiff`