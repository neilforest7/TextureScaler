# TextureScaler

TextureScaler是一个用于批量处理3D工程中贴图分辨率的工具。它可以批量地限制贴图的最大分辨率，提高工作效率。

## 主要功能

1. 批量调整贴图分辨率
2. 支持多种图像格式（.exr, .png, .jpg, .hdr, .tif, .tga, .jpeg）
3. 可以设置分辨率阈值进行筛选
4. 提供多种预设分辨率选项
5. 支持覆盖原文件或创建备份
6. 鼠标悬停预览图片功能

## 技术栈

- Python
- PySide6 (Qt for Python)
- OpenImageIO

## 安装

1. 确保您已安装 Python 3.7 或更高版本
2. 克隆此仓库到本地
3. 在项目目录中运行以下命令安装依赖项:
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 运行程序: `python main.py`
2. 点击"Open Folder"或"Open Images"选择需要处理的贴图
3. 在表格中选择需要处理的贴图
4. 使用右侧的"Set Resolution"选项设置目标分辨率
5. 选择是否覆盖原文件或创建备份
6. 点击"Execute"开始处理
7. 将鼠标悬停在文件名上可以预览图片

## 未来计划

- 添加色彩空间转换功能（如从sRGB到ACES CG）
- 优化贴图命名功能
- 添加批处理命令行接口
- 支持更多图像格式

## 贡献

欢迎提交问题和拉取请求。对于重大更改，请先开issue讨论您想要更改的内容。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。
