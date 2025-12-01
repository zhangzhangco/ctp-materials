# 4K White Lines

## 1. 来源 (Location)
7.5.27

## 2. 用途 (Purpose)
验证子像素空间重合度（Sub-pixel Spatial Coincidence）及色边伪影。

## 3. 特性 (Characteristics)
包含1分钟4K Flat帧的图像轨迹文件。 Each frame consists of 3 sets of three patches, with the sets stacked vertically and the patches arranged horizontally. 每组包含一个水平线条色块，一个垂直线条色块和一个斜线条色块。 每个色块包含1、2、3和4像素宽的线条，且未进行抗锯齿处理。 线条为D65全屏白，背景为黑色。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.27要求：
1. 显示图案并检查色彩边缘(Color Fringing)或收敛性(Convergence)。
2. 确认线条清晰，无明显色散。

### 素材文件验证
验证TIFF文件包含间隔规律的白色线条(CV 65535)。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `4K_White_Lines.tiff`