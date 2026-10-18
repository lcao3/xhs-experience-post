#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书竖版图文 · 内容页生成器模板

用法：复制本文件到工作目录 -> 修改 BRAND 与 pages 字典 -> python3 build.py
     -> 对 pages/ 下每个 html 执行 scripts/render.py 转 PNG。

支持四种内容组件：
    rows([("左词", "右说明", 是否红色高亮), ...])   要点行
    steps([("标题", "说明"), ...])                 圆形数字步骤
    twocol("左标题",[要点...], "右标题",[要点...])  双栏对比
    table(["列头"...], [["行1列1","列2"...], ...]) 表格（首列自动加粗）

页面组件：cover(...) 封面 / page(...) 内容页。改数据即可批量出新图。
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "pages")

# ============ 每套图只需改这里 ============
BRAND = "品牌名 / 账号名"          # 页脚品牌，改成你自己的
TOTAL = 12                          # 总页数（含封面），用于页码 "03 / 12"
COVER_TAG = "干货指南"             # 封面顶部红色小标签
COVER_TITLE = "一行 15 字以内的超大标题"   # 封面主标题（可用 <span class="hl">金色关键词</span> 高亮）
COVER_SUB = "一句话钩子副标题，说明读者看完能得到什么"
COVER_NOTE = "非专业意见，仅供参考"          # 封面底部小字（免责/信任）
# =========================================

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1440px;}
body{font-family:"Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden;}
.page{width:1080px;height:1440px;position:relative;overflow:hidden;}
/* ---- 封面：深蓝底 ---- */
.cover{background:#16324F;color:#fff;padding:96px 88px;display:flex;flex-direction:column;}
.cover .ctag{display:inline-block;align-self:flex-start;background:#C0392B;color:#fff;font-size:26px;font-weight:700;
  padding:12px 26px;border-radius:8px;letter-spacing:2px;margin-bottom:36px;}
.cover h1{font-size:92px;line-height:1.2;font-weight:900;letter-spacing:2px;margin:auto 0 24px;}
.cover h1 .hl{color:#E8B84B;}
.cover .sub{font-size:34px;line-height:1.6;color:#D9E2EC;font-weight:500;}
.cover .note{position:absolute;left:88px;right:88px;bottom:48px;font-size:22px;color:#8FA3B5;}
/* ---- 内容页：米白底 ---- */
.content{background:#FAF7F1;padding:86px 88px 96px;display:flex;flex-direction:column;}
.kicker{display:inline-block;align-self:flex-start;font-size:26px;font-weight:700;color:#C0392B;letter-spacing:2px;margin-bottom:24px;}
.kicker::before{content:"";display:inline-block;width:36px;height:6px;background:#C0392B;vertical-align:middle;margin-right:14px;border-radius:2px;}
h1.title{font-size:56px;line-height:1.22;font-weight:900;color:#16324F;letter-spacing:1px;margin-bottom:6px;}
.rule{width:100%;height:2px;background:#E3DCD0;margin:26px 0 30px;}
/* 要点行：左粗词 + 右说明 */
.rows{display:flex;flex-direction:column;}
.row{display:flex;gap:34px;padding:22px 0;border-bottom:1px solid #E3DCD0;}
.row:last-child{border-bottom:none;}
.row .k{flex:0 0 250px;font-size:30px;font-weight:700;color:#16324F;line-height:1.35;}
.row .d{flex:1;font-size:28px;line-height:1.55;color:#2B2B2B;}
.row .k.hl{color:#C0392B;}
/* 步骤 */
.step{display:flex;gap:26px;padding:18px 0;align-items:flex-start;}
.step .num{flex:0 0 52px;height:52px;border-radius:50%;background:#16324F;color:#fff;font-size:28px;font-weight:900;
  display:flex;align-items:center;justify-content:center;margin-top:2px;}
.step:last-of-type .num{background:#C0392B;}
.step .body{flex:1;}
.step .t{font-size:31px;font-weight:700;color:#16324F;margin-bottom:6px;}
.step .d{font-size:27px;line-height:1.5;color:#2B2B2B;}
/* 双栏 */
.twocol{display:flex;gap:30px;margin-top:6px;}
.col{flex:1;background:#fff;border-radius:16px;padding:30px 30px;}
.col h3{font-size:30px;font-weight:900;margin-bottom:18px;}
.col.l h3{color:#16324F;}
.col.r h3{color:#C0392B;}
.col ul{list-style:none;}
.col li{font-size:25px;line-height:1.55;color:#2B2B2B;padding:9px 0 9px 22px;position:relative;}
.col li::before{content:"·";position:absolute;left:0;color:#C0392B;font-weight:900;}
.col .sub{font-size:22px;color:#888;margin-bottom:14px;}
/* 表格 */
table{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;}
th{background:#16324F;color:#fff;font-size:25px;padding:20px 14px;text-align:left;}
td{font-size:24px;line-height:1.45;color:#2B2B2B;padding:18px 14px;border-bottom:1px solid #EFEAE0;vertical-align:top;}
tr:last-child td{border-bottom:none;}
td.m{font-weight:700;color:#16324F;white-space:nowrap;}
/* callout */
.callout{margin-top:auto;background:#fff;border-left:8px solid #C0392B;padding:26px 32px;border-radius:0 14px 14px 0;}
.callout .tag{font-size:25px;font-weight:700;color:#C0392B;margin-bottom:8px;letter-spacing:1px;}
.callout .txt{font-size:26px;line-height:1.6;color:#2B2B2B;}
.callout .txt b{color:#C0392B;}
.footer{position:absolute;left:88px;right:88px;bottom:34px;display:flex;justify-content:space-between;align-items:center;font-size:21px;color:#9a9186;letter-spacing:1px;}
.footer .brand{font-weight:700;color:#16324F;}
"""

def cover(tag=COVER_TAG, title=COVER_TITLE, sub=COVER_SUB, note=COVER_NOTE):
    return f"""<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body><div class="page cover">
<div class="ctag">{tag}</div>
<h1>{title}</h1>
<div class="sub">{sub}</div>
<div class="note">{note}</div>
</div></body></html>"""

def rows(items):
    h = ""
    for k, d, hl in items:
        h += f'<div class="row"><div class="k{" hl" if hl else ""}">{k}</div><div class="d">{d}</div></div>'
    return h

def steps(items):
    h = ""
    for i, (t, d) in enumerate(items, 1):
        h += f'<div class="step"><div class="num">{i}</div><div class="body"><div class="t">{t}</div><div class="d">{d}</div></div></div>'
    return h

def twocol(lt, ls, rt, rs, lsub="", rsub=""):
    def li(lst): return "".join(f"<li>{x}</li>" for x in lst)
    return (f'<div class="twocol"><div class="col l"><h3>{lt}</h3>'
            f'{f"<div class=sub>{lsub}</div>" if lsub else ""}<ul>{li(ls)}</ul></div>'
            f'<div class="col r"><h3>{rt}</h3>{f"<div class=sub>{rsub}</div>" if rsub else ""}<ul>{li(rs)}</ul></div></div>')

def table(headers, rowsdata):
    th = "".join(f"<th>{x}</th>" for x in headers)
    tr = ""
    for i, r in enumerate(rowsdata):
        tds = "".join(f'<td class="m">{r[0]}</td>' if j == 0 else f"<td>{c}</td>" for j, c in enumerate(r))
        tr += f"<tr>{tds}</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

def page(kicker, title, body, ctag, ctxt, no):
    return f"""<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body><div class="page content">
<div class="kicker">{kicker}</div>
<h1 class="title">{title}</h1>
<div class="rule"></div>
{body}
<div class="callout"><div class="tag">{ctag}</div><div class="txt">{ctxt}</div></div>
<div class="footer"><span class="brand">{BRAND}</span><span>{no} / {TOTAL}</span></div>
</div></body></html>"""

# ============ 示例数据：替换为你的内容即可 ============
pages = {}

pages["01"] = cover()

pages["02"] = page("核心命题",
    "PR 是“住在哪的资格”，国籍是“随时回去的权利”",
    twocol("PR · 永久居留权（绿卡）",
        ["回国免签证，拿中国护照直接买机票回来","国内买房、银行、社保都与身份证绑定，生活办事方便","税务安排相对灵活，不想保留了可以放弃","<b>代价：</b>有“移民监”，须定期登录，否则身份可能被取消"],
        "入籍 · 外国公民",
        ["身份稳定，在中国想待多久待多久，无需为登录担心","回去就是买张机票的事，不用看移民局脸色","可申请中国“五星卡”，在国内办事更便利","<b>代价：</b>全球征税，且国内户口、房产、银行卡、社保连锁变更"],
        lsub="你依然是中国公民，持中国护照", rsub="你变成外国公民，持外国护照"),
    "一句话决策", "怕被“移民监”绑住就入籍；怕国内身份推倒重来、怕全球税，就先留 PR。", "02")

pages["03"] = page("01 身份抉择 · 入籍侧",
    "入籍换来自由，却要推倒与身份证绑定的一整套",
    rows([
        ("户口注销","派出所会主动找你注销，不办也得办，拿到《户籍注销证明》",False),
        ("房产变更","拿旧身份证卖不了房，须先办“同一人公证”，再到不动产中心变更",False),
        ("银行卡更新","不把身份信息从身份证更新为护照，大额资金动不了",False),
        ("社保处理","继续交也领不了，须终止养老保险，个人账户余额一次性退",False),
    ]),
    "两个长期义务", "<b>全球征税：</b>入籍后不管住哪，都要就全球收入申报（美国尤其典型）；<b>弃籍税：</b>日后想放弃该国国籍须走完弃籍手续，高净值人群可能被征弃籍税。", "03")

pages["04"] = page("02 国内善后 · 办理顺序",
    "入籍后第一次回国，按这个顺序把五件事办完",
    steps([
        ("注销户口","带外国护照、入籍证明到原户籍地派出所，取得《户籍注销证明》"),
        ("同一人声明公证","证明原中国身份与现外国护照为同一人，房产、银行变更都要用"),
        ("房产变更","到不动产中心把房产从旧身份证变更为外籍身份，否则日后卖房过不了户"),
        ("银行卡更新","到银行把身份信息从身份证更新为护照，否则后续大额业务办不了"),
        ("社保处理","到社保局终止养老保险，个人账户里的钱一次性退回本人"),
    ]),
    "关键提示", "第 2 步“同一人公证”是第 3、4 步的前置，第一次回国就集中办完，越拖越麻烦。", "04")

pages["05"] = page("02 国内善后 · 过来人建议",
    "决定的关键不是哪个身份更好，而是“你未来住在哪”",
    rows([
        ("还不确定回不回","先保留 PR，税务交给会计师做，给自己留条退路",False),
        ("确定长期在国内、已入籍","安心待着，找个好会计师每年正常报税即可",False),
        ("确定彻底不回国外","PR 早放弃早省心，省得每年还要为它报税",False),
        ("两边都想要、还没想清","过来人说最纠结：要么接受 PR 可能作废，要么早点入籍（代价是一辈子全球报税）",True),
        ("国内根基深、家人都在","没必要入籍，PR 留着当退路，真长期不在了作废就作废",False),
    ]),
    "没有完美选项", "PR 的上限是“可能作废”，入籍的代价是“一辈子全球税”。按你未来十年实际住哪来选，而不是按哪个身份听起来更好。", "05")

pages["06"] = page("03 年度合规 · 保留身份",
    "只要绿卡/国籍没放弃，每年 4 月这几张表一张都不能少",
    rows([
        ("Form 1040 联邦税","每年 4 月 15 日前申报，全球收入都要报，不论人在中国还是美国",False),
        ("FBAR (FinCEN 114)","海外银行账户合计任何时点超过 $10,000 就要报，与联邦税是两套系统，最易漏",True),
        ("Form 8938","海外金融资产超过规定门槛，随联邦税一并申报，门槛按申报身份区分",False),
        ("州税","若仍保留某州住址或税务居民联系，可能还要单独报该州税",False),
    ]),
    "最容易踩的漏报点","“人回中国了就不用报美国税”是错的。只要身份没放弃每年都要报；FBAR 单独走 FinCEN 系统，和联邦税不是一回事，务必分别处理。", "06")

pages["07"] = page("04 海外资产 · 房产",
    "人回国后，美国的房子只有三个去向",
    rows([
        ("卖掉","最简单直接：房款打回国内，或留在美国账户里继续理财",False),
        ("出租","找 Property Manager 远程管理，自己人在国内不用操心",False),
        ("留着自己度假","保留使用权，每年回去住一阵，当作往返两国的落脚点",False),
    ]),
    "过来人账要算清","房子不大、租金不高的话，远程管理往往不划算——管理费、招租费、地税、保险和报税层层扣下来，租金所剩无几。不少人最终结论：这种情况不如直接卖掉。", "07")

pages["08"] = page("04 海外资产 · 出租实操",
    "远程出租的真相：花两笔钱，换一套全托管",
    twocol("你要付的两笔钱",
        ["管理费：按月租金的 8%–12% 收取","招租费：每来一个新租客，另收相当于一个月租金的费用"],
        "它替你做的事",
        ["找租客、签租约、按时收租","日常维修与突发问题处理","代缴地税、维护房屋保险"]),
    "算账提醒","管理省心不等于划算。小房子、低租金下，管理费+招租费+地税+保险+报税层层扣减，租金常常所剩无几。是否出租，先按这个账算一遍再决定。", "08")

pages["09"] = page("04 海外资产 · 跨境汇款",
    "把钱转回国内，按金额大小选通道",
    table(["方式","手续费 / 汇率","到账速度","适合场景"],
        [["Remitly","$1.99 起，首笔常有优惠","几小时，直转微信/支付宝","小额"],
         ["Wise","中间市场汇率，费率约 0.5%–1%","较快","大额，追求透明"],
         ["美国银行电汇","$25–$45，加中间行费约 $50–$60","1–3 天","传统大额"],
         ["中银香港同名互转","同名账户互转免手续费","当天到账","有港户的大额"]]),
    "来源","过来人实操经验整理。手续费与汇率以各平台、各银行实时公布为准；Wise 原名 TransferWise。", "09")

pages["10"] = page("04 海外资产 · 外汇额度",
    "5 万美元是“结汇额度”，不是汇款上限",
    rows([
        ("5 万美元/年是什么","这是个人每年便利化结汇的额度，限制的是“换成人民币”这一步，不是你能把钱汇进来的总额",False),
        ("正当收入可超额","卖房、工资、投资收益等有正当来源，凭证明材料可汇超 5 万美元，不受年度额度限制",False),
        ("回国买房另有通道","凭购房合同可直接结汇支付房款，不占用、也不受 5 万美元额度限制",False),
    ]),
    "关键动作","大额转账务必留好证明材料（卖房合同、工资单等），否则银行会追问资金来源，钱可能被卡。", "10")

pages["11"] = page("04 海外资产 · 401k 养老账户",
    "401k 的提款时机，直接决定你交多少税",
    rows([
        ("Traditional 401k","59½ 岁前提款：10% 罚款 + 所得税，不建议提前动",False),
        ("Roth 401k","存满 5 年且满 59½ 岁后提取：本金与收益全部免税",True),
        ("弃籍前的转换技巧","放弃美国身份前一年，趁收入低、税率低，把 Traditional 401k 转成 Roth IRA，之后提取免税",False),
    ]),
    "过来人建议","50 岁以下、还年轻，401k 就留在美国别动，继续定投；等到 59½ 岁以后再分批提取，税最少。提前为了回国用钱而取出，往往最不划算。", "11")

pages["12"] = page("04 海外资产 · 资金配置",
    "人在国内、钱留美国：越省事的配置越省心",
    rows([
        ("省心打底","定投大盘指数基金（如 VOO、SPY），不用盯盘，长期持有即可",False),
        ("求稳压舱","买美国国债，利息免州税，本金安全，用来压波动",False),
        ("兼顾保障","指数型人寿保险（IUL），投资与养老保障二合一，适合养老规划",False),
    ]),
    "过来人总原则","别搞太复杂：定投大盘指数 + 配一部分国债，比例自己定，长期拿着就行。人在国内远程操作，越简单的策略越容易坚持，也越不容易出错。", "12")

os.makedirs(OUT, exist_ok=True)
for name, html in pages.items():
    with open(os.path.join(OUT, f"{name}.html"), "w", encoding="utf-8") as f:
        f.write(html)
print(f"generated {len(pages)} pages -> {OUT}")
