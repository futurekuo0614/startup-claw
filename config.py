import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise EnvironmentError(
            f"Required environment variable '{name}' is not set. "
            "Add it to your .env file and restart."
        )
    return val


GEMINI_API_KEY          = os.environ.get("GEMINI_API_KEY", "")   # optional: Gemini fallback LLM
FIREBASE_PROJECT_ID     = _require_env("FIREBASE_PROJECT_ID")
SHEETS_ID               = _require_env("SHEETS_ID")
GOOGLE_CREDENTIALS_JSON = _require_env("GOOGLE_CREDENTIALS_JSON")

FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

MAX_ARTICLES_PER_SOURCE = 30
MAX_GEMINI_PER_RUN      = 20

SOURCES = [
    # ── 台灣 ──
    {"id": "bnext",      "name": "數位時代",          "rss": "https://www.bnext.com.tw/rss",                                                 "region": "台灣", "enabled": True},
    {"id": "meet",       "name": "Meet 創業小聚",      "rss": "https://meet.bnext.com.tw/rss",                                               "region": "台灣", "enabled": True},
    {"id": "tc_tw",      "name": "TechCrunch TW RSS",  "rss": "https://news.google.com/rss/search?q=新創+募資+台灣&hl=zh-TW&gl=TW&ceid=TW:zh-Hant", "region": "台灣", "enabled": True},
    # ── 中國 ──
    {"id": "36kr",       "name": "36氪",              "rss": "https://36kr.com/feed",                                                        "region": "中國", "enabled": True},
    {"id": "lieyunwang", "name": "獵雲網",             "rss": "https://www.lieyunwang.com/rss.xml",                                          "region": "中國", "enabled": True},
    {"id": "kr_asia",    "name": "KrASIA",             "rss": "https://kr-asia.com/feed",                                                     "region": "中國", "enabled": True},
    {"id": "cn_google",  "name": "中國新創 Google News","rss": "https://news.google.com/rss/search?q=中国+创业+融资+startup&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "region": "中國", "enabled": True},
    {"id": "cn_google2", "name": "中國科技 Google News","rss": "https://news.google.com/rss/search?q=中国+科技+独角兽+IPO&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "region": "中國", "enabled": True},
    # ── 東南亞 ──
    {"id": "e27_gn",     "name": "e27 Google News",   "rss": "https://news.google.com/rss/search?q=e27+startup+funding+southeast+asia&hl=en&gl=SG&ceid=SG:en", "region": "東南亞", "enabled": True},
    {"id": "dealstreet", "name": "DealStreetAsia",     "rss": "https://www.dealstreetasia.com/feed/",                                         "region": "東南亞", "enabled": True},
    {"id": "techinasia", "name": "Tech in Asia",       "rss": "https://www.techinasia.com/feed",                                              "region": "東南亞", "enabled": True},
    {"id": "sea_google", "name": "SEA新創 Google News", "rss": "https://news.google.com/rss/search?q=startup+funding+series+southeast+asia+2025&hl=en&gl=SG&ceid=SG:en", "region": "東南亞", "enabled": True},
    {"id": "sea_google2","name": "SEA科技 Google News", "rss": "https://news.google.com/rss/search?q=Indonesia+Vietnam+Thailand+startup+raised&hl=en&gl=SG&ceid=SG:en", "region": "東南亞", "enabled": True},
    # ── 全球 ──
    {"id": "tc_startup", "name": "TechCrunch Startups","rss": "https://techcrunch.com/category/startups/feed/",                               "region": "全球", "enabled": True},
    {"id": "venturebeat","name": "VentureBeat",        "rss": "https://venturebeat.com/category/business/feed/",                              "region": "全球", "enabled": True},
    {"id": "crunchbase", "name": "Crunchbase News",    "rss": "https://news.crunchbase.com/feed/",                                            "region": "全球", "enabled": True},
    {"id": "global_gn",  "name": "全球新創 Google News","rss": "https://news.google.com/rss/search?q=startup+funding+series+A+B+2025&hl=en&gl=US&ceid=US:en", "region": "全球", "enabled": True},
    {"id": "global_gn2", "name": "全球科技 Google News","rss": "https://news.google.com/rss/search?q=unicorn+IPO+venture+capital+2025&hl=en&gl=US&ceid=US:en", "region": "全球", "enabled": True},
]

REGION_MAP = {s["id"]: s["region"] for s in SOURCES}

# 和泰集團八大業務柱對應關鍵字（用於 ML 特徵評分）
# 業務背景：Toyota/Lexus/Hino 總代理、iRent/yoxi/和運租車 MaaS、和泰產險/和安保險、
#           和潤企業汽車金融、和泰Pay/Points/聯名卡、去趣旅遊 App、EVRun 充電、AI 中台
FIT_KEYWORDS = {
    # iRent、yoxi、和運租車、MaaS 生態
    "MaaS_Mobility": [
        "MaaS", "共享汽車", "car sharing", "ride hailing", "叫車", "租車", "車隊管理",
        "fleet management", "短租", "長租", "共乘", "出行平台", "mobility service",
        "乘車", "代駕", "派遣", "mobility as a service", "shared mobility",
    ],
    # EVRun 充電網、U-POWER 投資、Toyota MIRAI 氫能
    "EV_Charging": [
        "電動車", "EV", "充電樁", "充電站", "充電基礎設施", "氫能", "氫燃料",
        "hydrogen", "FCEV", "換電", "battery swap", "CPO", "充電管理", "smart charging",
        "charging infrastructure", "ev charging", "電動化", "electrification",
    ],
    # 車聯網、ADAS、智慧座艙、預測保養
    "AutoTech_ADAS": [
        "ADAS", "自動駕駛", "autonomous", "車聯網", "V2X", "OBD", "telematics",
        "車載", "智慧座艙", "cockpit", "預測保養", "predictive maintenance",
        "connected vehicle", "車輛感測", "lidar", "雷達", "over-the-air", "OTA",
    ],
    # 和泰產險、和安保險、UBI 車險
    "InsurTech": [
        "保險", "insurtech", "UBI", "車險", "usage-based insurance", "telematics insurance",
        "理賠自動化", "核保", "再保", "數位保險", "嵌入式保險", "embedded insurance",
        "insurance tech", "parametric insurance",
    ],
    # 和潤企業：汽車貸款、融資租賃
    "AutoFinance": [
        "汽車貸款", "車貸", "融資租賃", "auto finance", "leasing", "分期付款",
        "殘值", "balloon payment", "fleet financing", "設備融資", "auto loan",
    ],
    # 和泰Pay、和泰Points、和泰聯名卡：點數經濟與支付
    "Loyalty_Payment": [
        "點數", "loyalty", "會員生態", "支付", "payment", "digital wallet", "信用卡",
        "co-branded card", "reward", "回饋", "fintech", "數位支付", "points economy",
    ],
    # 和泰 AI 中台、AI First 戰略：生成式 AI、資料平台
    "AI_DataPlatform": [
        "人工智慧", "機器學習", "AI", "大數據", "data platform", "個人化",
        "personalization", "預測分析", "generative AI", "LLM", "AI platform",
        "數位轉型", "API platform", "生成式", "大模型",
    ],
    # 去趣 App：旅遊規劃、跨境出行
    "TravelTech": [
        "旅遊科技", "travel tech", "旅行規劃", "trip planning", "tourism platform",
        "訂房", "訂票", "出行", "跨境旅遊", "smart tourism", "旅遊 APP",
    ],
}


SKIP_KEYWORDS = ["廣告","sponsor","特別報導","白皮書","webinar","招募","徵才"]
FX = {"TWD": 32, "CNY": 7.2, "JPY": 155, "SGD": 0.74, "MYR": 4.7}
