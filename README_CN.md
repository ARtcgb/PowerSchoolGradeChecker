# PowerSchool Grade Checker

PowerSchool Grade Checker是一个基于 Python 的工具，可让用户监控课程成绩更新。该应用程序自动化了检查课程页面更新的过程，并记录课程成绩和更新时间的变化。

## 特性

- 自动登录PowerSchool网站。
- 检索具有指定目标的课程网址。
- 提取并存储课程成绩和更新时间。
- 将新数据与先前存储的数据进行比较。
- 记录课程成绩的任何更新和变化。

## 安装

1. 确保您的计算机上安装了 Python 3.7 或更高版本。您可以从 [python.org](https://www.python.org/downloads/) 下载。

2. 克隆此存储库或将其下载为 ZIP 文件。

    ```
    git clone https://github.com/ARtcgb/PowerSchoolGradeChecker.git
    ```

3. 导航到项目目录。

    ```
    cd PowerSchoolGradeChecker
    ```

4. 创建虚拟环境（可选但推荐）。

    ```
    python -m venv venv
    ```

5. 激活虚拟环境。

   对于 Windows：

    ```
    venv\Scripts\activate
    ```

   对于 macOS 和 Linux：

    ```
    source venv/bin/activate
    ```

6. 使用 `requirements.txt` 文件安装所需的依赖项。

    ```
    pip install -r requirements.txt
    ```

## 使用

1. 更新 `config/config.properties` 文件，填写您的登录凭据、网站 URL 和目标选择。

2. 运行 `main.py` 脚本以启动成绩检查器。

    ```
    python main.py
    ```

3. PowerSchool Grade Checker将登录课程网站，检索课程网址并提取课程成绩和更新时间。任何更新或成绩更改都将被记录。

## 贡献

欢迎提出拉取请求。对于重大变更，请先开启一个 issue 以讨论您希望进行的更改。

请确保适当更新测试。

## 许可

[MIT](https://choosealicense.com/licenses/mit/)
