# BaiduTongjiAPI

百度统计 API 的 Python 封装

## 上游项目

本项目 Fork 自 [JeffersonQin/BaiduTongjiAPI](https://github.com/JeffersonQin/BaiduTongjiAPI)（PyPI 包 [baidutongji](https://pypi.org/project/baidutongji/)），感谢上游作者 [JeffersonQin](https://github.com/JeffersonQin) 的原始工作。

## 支持范围

|   账号类型   | 支持情况 |
| :----------: | :------: |
| 百度商业账号 |    ❌     |
|   百度账号   |    ✅     |

|                      API                       | 支持情况 |
| :--------------------------------------------: | :------: |
|                   Token 刷新                   |    ✅     |
|                    站点列表                    |    ✅     |
|               网站概况(趋势数据)               |    ✅     |
|               网站概况(地域分布)               |    ✅     |
| 网站概况(来源网站、搜索词、入口页面、受访页面) |    ✅     |
|                    趋势分析                    |    ✅     |
|                    实时访客                    |    ✅     |
|                    推广方式                    |    ❌     |
|                  百度推广趋势                  |    ❌     |
|                    全部来源                    |    ✅     |
|                    搜索引擎                    |    ✅     |
|                     搜索词                     |    ✅     |
|                    外部链接                    |    ✅     |
|                  指定广告跟踪                  |    ❌     |
|                    受访页面                    |    ✅     |
|                    入口页面                    |    ✅     |
|                    受访域名                    |    ✅     |
|                    地域分布                    |    ✅     |
|                地域分布(按国家)                |    ✅     |

## Doc

百度统计官方文档：

* https://tongji.baidu.com/api/manual/
* https://tongji.baidu.com/api/debug/#

具体使用详见源代码，下面是对项目结构：

```
baidutongji
├── __init__.py
├── api.py          # API 定义
├── data.py         # 可选参数数据结构
└── metrics.py      # 各 API 筛选指标数据结构
```

使用样例：

* 查询站点今天的网站概况（趋势数据）报表：
  ```python
  import baidutongji
  
  baidutongji.getTimeTrendRpt('{ACCESS_TOKEN}', '{SITE_ID}', datetime.date.today(), datetime.date.today(), TimeTrendRptMetrics(pv_count=True, visitor_count=True, ip_count=True, bounce_ratio=True, avg_visit_time=True))
  ```
  或者可以简化：
  ```python
  import baidutongji
  
  baidutongji.getTimeTrendRpt('{ACCESS_TOKEN}', '{SITE_ID}', datetime.date.today(), datetime.date.today(), TimeTrendRptMetrics().setAllTrue())
  ```
* 查询 `2022/01/01 ~ 2022/01/10` 与 `2022/04/01 ~ 2022/04/10` 趋势分析对比报表，指定时间粒度以天为单位，筛选用户为老用户，访问设备为 PC，地区为上海市：
  ```python
  import baidutongji
  
  baidutongji.getTrendTime('{ACCESS_TOKEN}', '{SITE_ID}', datetime.date(2022, 1, 1), datetime.date(2022, 1, 10), TrendTimeMetrics().setAllTrue(), datetime.date(2022, 4, 1), datetime.date(2022, 4, 10), Source.ALL, ClientDevice.PC, VisitorType.RETURN, TimeGran.DAY, Region(RegionType.PROVINCE, '上海'))
  ```

## 其他特性

### 代理支持

可通过 `setProxy()` 为所有请求设置代理：

```python
import baidutongji

baidutongji.setProxy({'http': 'http://proxy.example.com:8080', 'https': 'https://proxy.example.com:8080'})
```

清除代理：

```python
import baidutongji

baidutongji.setProxy(None)
```

> 注意：`setProxy()` 仅接受 `dict` 类型的参数，传入其他类型时返回 `False`，设置成功时返回 `True`。

### 非 JSON 响应处理

当百度返回非 JSON 内容（如网关 HTML 错误页）时，所有 API 不会抛出 JSON 解析异常，而是返回统一格式的错误字典：

```python
{
    'error_code': 'invalid_json_response',
    'error_message': 'Baidu returned a non-JSON response',
    'response_text': '<html>...原始响应内容...</html>',
}
```

其中 `response_text` 为百度返回的原始响应文本，便于排查问题。
