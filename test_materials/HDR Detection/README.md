# HDR Detection

## 1. 来源 (Location)
7.5.31

## 2. 用途 (Purpose)
验证SDR/HDR模式自动切换功能。

## 3. 特性 (Characteristics)
包含HDR Dark Gray和HDR Light Gray补丁。用于验证设备自动切换HDR模式。

## 4. 验证方法 (Verification)
### DCI合规性测试
根据CTP 7.5.31要求：
1. 播放包含SDR和HDR内容的播放列表。
2. 验证显示设备是否正确切换到HDR模式。
3. 测量亮度确认模式切换成功。

### 素材文件验证
验证TIFF文件包含预期的HDR灰阶补丁。

## 5. 素材状态 (Material Status)
✅ **已生成 (Generated)**

该素材文件（16-bit XYZ TIFF）已包含在当前目录中。
文件路径: `HDR_Detection.tiff`
