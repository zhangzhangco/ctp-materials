# CTP 合规性测试环境

本目录包含用于数字电影系统规范合规性测试计划 (CTP) 1.4.3 版的工具和脚本。
这些工具源自 CTP 文档的附录 C (Appendix C)。

## 包含的工具

### 🚀 快速开始 (下载编译好的工具)
如果您不想自己编译源码，可以直接从本仓库的 **[Releases 页面](../../releases)** 下载适用于 **macOS** 和 **Linux** 的预编译工具包。
下载解压后即可直接使用，无需安装任何依赖库。

### C/C++ 工具
- `dc-thumbprint`: 计算证书公钥的指纹 (SHA-1 哈希)。
- `schema-check`: 根据 Schema 解析并验证 XML 实例文档。
- `kdm-decrypt`: 解密 KDM 中的 EncryptedKey 元素。
- `j2c-scan`: 解析 JPEG 2000 码流并生成参数数据。

### Python 工具
- `uuid_check.py`: 检查 XML 文件中的 UUID 是否符合 RFC-4122 标准。
- `dsig_cert.py`: 对 XML 签名中的证书进行重新排序。
- `dsig_extract.py`: 从签名的 XML 文件中提取证书。

## 前置要求

- **C/C++ 构建工具**: `cc`, `c++`, `make`
- **依赖库**:
    - OpenSSL (`libcrypto`)
    - Xerces-C (`libxerces-c`)
    - OpenJPEG (`libopenjpeg`, 推荐版本 1.5.2)
    - XML-Security-C (`libxml-security-c`)
    - ASDCPLib (`libkumu`, `libas02`, `libasdcp`)
- **Python**: Python 2.7 或更高版本 (脚本兼容 Python 3)。

## 构建说明

1. 进入 `tools` 目录：
   ```bash
   cd tools
   ```

2. 运行 `make` 构建 C/C++ 工具：
   ```bash
   make
   ```
   *注意：您可能需要先安装所需的依赖库。在 macOS 上使用 Homebrew，可以尝试：*
   ```bash
   brew install openssl xerces-c openjpeg xml-security-c asdcplib
   ```
   *根据您的系统配置，您可能需要调整 Makefile 中的库路径。*

## 使用方法

### dc-thumbprint
```bash
./tools/dc-thumbprint <certificate_file.pem>
```

### schema-check
```bash
./tools/schema-check <xml-file> [<schema-file> ...]
```

### kdm-decrypt
```bash
./tools/kdm-decrypt <kdm-file> <RSA-PEM-file>
```

### j2c-scan
```bash
./tools/j2c-scan <file.j2c>
```

### uuid_check.py
```bash
python3 tools/uuid_check.py <xml-file> [...]
```

### dsig_cert.py
```bash
python3 tools/dsig_cert.py <xml-file>
```

### dsig_extract.py
```bash
python3 tools/dsig_extract.py [-p <prefix>] <xml-file>
```
