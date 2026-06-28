---
name: "gold-analysis"
description: "全面分析黄金价格走势 with HTML table formatting for Telegram"
metadata:
  version: 1.0.0
  author: FMouse
  tags: gold, trading, analysis, finance
---

# 黄金走势分析 Skill

全面分析黄金价格走势，整合多维度数据，生成专业的分析报告。

## What's New

- ✅ **HTML Table Formatting**: Clean table display for Telegram Rich Messages
- ✅ **Minimalist Box Style**: Rapi tanpa garis putus-putus
- ✅ **Multi-datasource**: 金十数据、Kitco、Bloomberg、新浪财经

## 功能说明

### 核心能力
1. **数据源整合**
   - 金十数据：实时金价、财经日历、宏观数据
   - 金价网站：Kitco、Bloomberg、新浪财经
   - 财经新闻：律动 BlockBeats、华尔街见闻

2. **分析维度**
   - 技术面：K线、均线、MACD、RSI、布林带
   - 基本面：美元指数、实际利率、通胀数据、央行政策
   - 情绪面：CFTC持仓、恐慌指数、市场情绪指标
   - 地缘政治：战争、大选、地缘风险事件

3. **输出内容**
   - 当前金价及近期走势
   - 技术指标分析（支撑位/阻力位）
   - 宏观因素影响分析
   - 短期/中期/长期展望
   - 可操作的投资建议

## Output Format

When `richMessages: true` is enabled in Telegram config, output uses clean HTML tables:

### Example Format:
```html
<h3>💰 MULTI-TIMEFRAME PRICE DATA</h3>
| Timeframe | Open | High | Low | Close | Source |
|:---|:---|:---|:---|:---|:---|
| **1d** | $4,014.68 | $4,095.97 | $3,983.17 | **$4,081.45** | Deriv API |
```

### Formatting Rules:
- Use `|:---|:---|` for left-aligned columns
- Use `**bold**` for important values (current price, signals)
- Keep columns minimal (max 6 columns per table)
- Use emoji headers for visual distinction
- Avoid ASCII art boxes (ganti dengan tabel HTML)

## 分析框架

### 一、技术面分析

#### 1. 价格走势
- 当前金价（美元/盎司、人民币/克）
- 24小时涨跌幅
- 近1周/1月/3月/1年走势

#### 2. 技术指标
- **均线系统**：MA5、MA10、MA20、MA60、MA120、MA250
- **趋势指标**：MACD (DIF, DEA, 柱状图)
- **震荡指标**：RSI (14)
- **volatility指标**：布林带 (上轨、中轨、下轨)
- **支撑与阻力**：关键支撑位/阻力位

### 二、基本面分析

#### 1. 美元指数 (DXY)
- 当前美元指数及走势
- 与黄金的负相关性分析

#### 2. 实际利率
- 美国10年期国债收益率
- 通胀预期（CPI、PCE）
- 实际利率 = 名义利率 - 通胀

#### 3. 通胀数据
- 美国CPI（同比、环比）
- 核心CPI
- PCE物价指数

#### 4. 央行政策
- 美联储（FOMC）最新决议
- 利率路径预期（点阵图）
- 其他主要央行（欧央行、日央行、英国央行）

### 三、情绪面分析

#### 1. CFTC持仓报告
- 商业持仓（套保）
- 非商业持仓（投机）
- 净多头/净空头变化

#### 2. 市场情绪指标
- 贪婪恐慌指数
- 金价波动性（GVZ）
- ETF持仓变化（GLD、IAU）

### 四、展望与建议

#### 1. 短期展望（1周-1月）
- 技术面信号
- 重要事件日历
- 操作建议（买入/卖出/观望）
- 止损止盈位置

#### 2. 中期展望（1月-3月）
- 趋势判断
- 关键价位
- 仓位建议
- 风险提示

#### 3. 长期展望（3月-1年）
- 宏观大趋势
- 战略配置建议
- 风险因素
- 预期收益空间

## 数据源

### 实时金价
- 金十数据：https://www.jin10.com/
- Kitco：https://www.kitco.com/
- Investing.com：https://www.investing.com/
- 新浪财经：https://finance.sina.com.cn/

### 技术面数据
- TradingView：https://www.tradingview.com/
- 东方财富：https://www.eastmoney.com/

### 基本面数据
- 美联储官网：https://www.federalreserve.gov/
- 美国劳工部：https://www.bls.gov/
- 美国经济分析局：https://www.bea.gov/

### 情绪面数据
- CFTC持仓报告：https://www.cftc.gov/
- 贪婪恐慌指数：https://alternative.me/crypto/fear-and-greed/

## 使用示例

### 完整分析报告
```
用户：帮我写一份完整的黄金分析报告

输出：HTML table format dengan data lengkap
```

### 快速分析
```
用户：现在黄金多少钱？可以买吗？

输出：
【当前金价】$4,081.45（+0.5%）
【技术面】RSI 55中性
【基本面】美元走弱
【建议】轻仓试多，止损$4,064
```

## 最佳实践

1. **数据验证**：多个数据源交叉验证
2. **周期搭配**：短中长期结合
3. **动态跟踪**：重大事件发生后及时更新
4. **风险意识**：任何分析都要有止损
5. **HTML Tables**: Gunakan format tabel untuk Telegram Rich Messages

## 更新日志

- v1.1.0 (2026-06-28) - Added HTML table formatting for Telegram
- v1.0.0 (2026-03-12) - Initial release
