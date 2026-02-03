# HDR Dark Gray Scale

## 1. 来源 (Location)
7.5.35

## 2. 用途 (Purpose)
验证HDR轮廓（Contouring）表现。

## 3. 特性 (Characteristics)
结构同 DCI HDR Gray Steps：包含5秒（120帧）的汇总图，展示表A.2.293中的所有灰阶值；随后每个灰阶以全屏展示，单档持续50秒。
包含10个暗部灰阶梯级。
* 目标亮度覆盖约0.01–1.0 cd/m²（以PQ EOTF映射至光度值），用于评估低亮区的量化和映射精度。
* 梯级在代码值上等间隔，但在感知域（JND）接近线性，以便突出任何压缩或断层伪影。

## 4. 验证方法 (Verification)
**硬件测量：** 测量每个全屏灰色色块的亮度，计算二阶近似导数。

**软件验证：** 同DCI HDR Gray Steps，采样所有梯级验证单调性。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `HDR_Dark_Gray_Scale.tiff`
