自述文件：

# 基于阿里dns服务的动态域名解析脚本
本脚本用于动态更新阿里云的域名解析记录（A记录和AAAA记录），通过获取当前公网IP并更新指定域名的解析记录。

### 功能简介
- **获取当前公网IP**：通过外部API获取当前服务器的公网IPv4和IPv6地址。
- **更新域名解析记录**：自动检查指定域名的解析记录，并根据当前公网IP更新阿里云DNS解析记录。
- **支持IPv4和IPv6**：可以同时处理IPv4和IPv6地址。

### 使用环境
- Python 3.6+
- 阿里云SDK (`aliyun-python-sdk-core` 和 `aliyun-python-sdk-alidns`)
- 需要网络访问权限以获取公网IP

### 代码说明
#### 1. 参数配置
- `access_key_id` 和 `access_key_secret`：阿里云的访问密钥，用于访问阿里云API。
- `domain`：您需要更新的一级域名（例如：`1111.xyz`）。
- `name_ipv4` 和 `name_ipv6`：指定需要更新的子域名列表，例如：`["111", "222"]`。
- `region`：阿里云的区域（默认为`cn-shanghai`）。

#### 2. 获取公网IP
- 通过访问以下API获取当前公网IP：
  - IPv4: `http://ip-api.com/json/?fields=query` 或 `http://ipv4.icanhazip.com`
  - IPv6: `https://api6.ipify.org?format=json` 或 `https://ipv6.icanhazip.com`

#### 3. 更新解析记录
- 脚本会自动检查域名解析记录，如果当前IP与解析记录中的IP不一致，则更新解析记录。
- 如果域名解析记录不存在，脚本会新建解析记录。

#### 4. 示例运行
运行脚本后，控制台会输出当时的公网IP和解析记录更新结果。

### 使用步骤
#### 1. 安装依赖
```bash
pip install aliyun-python-sdk-core aliyun-python-sdk-alidns requests
```

#### 2. 配置阿里云密钥
将`access_key_id`和`access_key_secret`替换为您的阿里云密钥。

#### 3. 修改域名和子域名
根据您的域名和需要更新的子域名，修改`domain`, `name_ipv4` 和 `name_ipv6`的参数。

#### 4. 运行脚本
```bash
python ddns.py
```

### 注意事项
- **安全性**：请勿将阿里云的`access_key_id`和`access_key_secret`泄露给他人，建议在生产环境中使用RAM角色和策略进行权限控制。
- **API调用限制**：阿里云API有一定的调用频率限制，请勿频繁调用。
- **外部依赖**：获取公网IP的API可能受网络环境影响，建议定期检查。

### 示例输出
```bash
获取到IPv4地址：
新建域名：111,解析成功
获取到IPv6地址：
修改域名：111,解析成功
```

希望这个自述文件能帮助你更好地使用和理解这个脚本！如果你有任何问题或建议，请随时联系我们。
