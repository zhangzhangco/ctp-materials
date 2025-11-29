# Pixel Structure Pattern E 4k

## 1. 来源 (Location)
7.5.3

## 2. 用途 (Purpose)
验证显示设备的像素计数和结构(4K, E orientation)。

### 设计原理与意义 (Design Rationale & Significance)
**为什么说是为投影机设计的？(Why Projector-Centric?)**
除了分辨率因素，该图案的**结构设计**本身就是为了应对投影显示的特有挑战：
1.  **三色会聚 (Convergence/Registration)**: 影院投影机通常由3片DLP芯片(R/G/B)组成。此图案中精细的**1像素宽颜色条带**和**白色边框**是检测三色芯片物理对齐（会聚）的绝佳工具。如果R/G/B芯片未对齐，白色线条边缘会出现色边（Fringing）。（LED屏像素是物理固定的，不存在此问题）。
2.  **光学几何与梯形校正 (Optical Geometry & Keystone)**: **对角线阶梯**对重采样算法极度敏感。如果投影机开启了梯形校正（Keystone）或存在光学畸变，对角线将不再平滑，出现锯齿或模糊。
3.  **物理遮幅 (Physical Masking)**: 影院银幕常有物理遮幅（Masking）。**二进制索引梯**让放映员能精确读出银幕边缘被遮挡的具体像素行/列数，从而精确调整画幅。

**方向意义 (E Orientation):**
测试水平扫描方向（从左到右）和垂直转置。用于检测纵向安装的屏幕或处理器旋转设置错误。

**分辨率意义 (4K Resolution):**
4K图案使用16x16像素块，包含更复杂的二进制索引和双重背景结构。这不仅测试分辨率，还通过精细的1像素宽线条测试高频细节解析力和信号带宽。

## 3. 特性 (Characteristics)
4096x2160图像，包含256x135个16x16像素块。每个块包含二进制编码的坐标索引和颜色条带。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.3要求：
1. 在屏幕上完整显示该图案。
2. 目视检查像素结构是否完整，无截断、缩放或伪影。
3. 验证最外层像素是否可见。

### LED屏测试建议 (LED Display Recommendations)
根据CTP 7.5.3，此测试对于2K主要针对投影机，对于4K则同时适用于投影机和直视型显示器（Direct View Displays）。在LED屏测试中，其价值在于：
1. **信号链路验证**: 确认处理器未进行错误的缩放或裁剪（规范要求关闭梯形校正等缩放功能）。
2. **像素映射**: 验证1:1像素映射，特别是对于非标准分辨率的LED屏。
3. **模组方向**: 通过N/S/E/W四个方向的图案，可以快速识别模组物理安装方向或数据走线方向的错误。

**建议补充测试 (Recommended Additional Tests):**
- **纯色全屏**: 检测坏点和模组色差。
- **低灰阶渐变**: 测试LED屏特有的低亮非线性问题。
- **高帧率移动条**: 测试动态刷新率和扫描线问题。

### 素材文件验证
验证TIFF文件尺寸为4096x2160，且包含预期的网格结构。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `Pixel_Structure_Pattern_E_4k.tiff`

## 6. 像素结构分析 (Pixel Structure Analysis)
根据DCI 1.4.3规范生成的16x16像素结构图(E orientation)。

### 结构描述
每个16x16块包含：
1.  **左半部分 (Cols 0-7)**:
    -   Rows 0-7: 对角线黑色阶梯背景 (Diagonal Black Steps)。
    -   Rows 8-15: 黑色背景。
2.  **右半部分 (Cols 8-15)**:
    -   Rows 0-7: 垂直颜色条带 (Vertical Color Bands, 0-7)。
    -   Rows 8-15: 对角线黑色阶梯背景 (Diagonal Black Steps, Repeated)。
3.  **二进制索引 (Binary Ladders)**:
    -   **Y索引 (Vertical)**: 位于 Cols 1-2，Rows 5-12。8位 (MSb at Top)。
    -   **X索引 (Horizontal)**: 位于 Rows 13-14，Cols 3-10。8位 (MSb at Left)。
    -   **Short Gray Scales**: 仅在上述区域显示。'0'位为灰色 (Gray Marker)，'1'位为白色 (WHT)。其余区域为黑色或背景。

### 结构图 (Structure Diagram)
![Pixel Structure Diagram](pixel_structure_diagram_e_4k.png)
*(Diagram shows a sample block with indices X=81, Y=37 to illustrate the binary ladder structure)*

### 验证 (Verification)
- **颜色映射**: 0-7对应 Brown, Red, Orange, Yellow, Green, Blue, Violet, Gray。
- **特殊值**: Black映射为"BLK"，White映射为"WHT"，Gray Marker映射为"LDR" (Gray)。
