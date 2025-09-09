import datetime
import re
from zoneinfo import ZoneInfo, available_timezones
from google.adk.agents import Agent
from .model.litellm_model.model_config import litellm_model

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    NOTE:
        這裡仍是示範用的假資料。
        若要全球可用，建議改接天氣 API（例如 Open-Meteo / OpenWeatherMap），
        並以城市 -> 經緯度 -> 天氣 的管線實作。
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def _normalize_city(s: str) -> str:
    """將城市字串正規化以利匹配 IANA time zone 的末段名稱。"""
    s = s.strip()
    # 常見字元轉換：空白 -> 底線、連字號同等視之、移除重複底線
    s = s.replace(" ", "_").replace("-", "_")
    s = re.sub(r"_+", "_", s)
    return s


def _search_timezones_by_city(city: str) -> list[str]:
    """以城市名稱嘗試匹配 IANA 時區，回傳候選清單（完整 IANA 名稱）。"""
    norm = _normalize_city(city)
    tzs = available_timezones()

    # 1) 強一致：最後一段完全等於（不分大小寫）
    exact = [
        tz for tz in tzs
        if tz.split("/")[-1].lower() == norm.lower()
    ]
    if exact:
        return exact

    # 2) 次一致：最後一段包含關鍵字（不分大小寫）
    partial = [
        tz for tz in tzs
        if norm.lower() in tz.split("/")[-1].lower()
    ]
    return partial


def get_current_time(city: str) -> dict:
    """Returns the current time for a city or IANA timezone worldwide.

    支援輸入：
        - IANA 時區名稱（例：'Asia/Taipei', 'America/New_York'）
        - 城市名稱（例：'Taipei', 'New York'）
          會嘗試以城市名匹配 IANA 時區最後一段；若多筆匹配，回傳候選清單。

    Returns:
        dict: {
            "status": "success" | "error",
            "report": str,                  # 成功時的人類可讀報告
            "timezone": str,                # 成功時實際採用的 IANA 時區
            "candidates": list[str] | None  # 模糊時的候選清單
        }
    """
    if not city or not isinstance(city, str):
        return {
            "status": "error",
            "error_message": "Input must be a non-empty city or IANA timezone string.",
        }

    # 若看起來像 IANA 時區（包含一個以上的 '/'），直接嘗試
    if "/" in city:
        try:
            tz = ZoneInfo(city)
            now = datetime.datetime.now(tz)
            report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
            return {"status": "success", "report": report, "timezone": city, "candidates": None}
        except Exception:
            # 繼續走城市名稱的搜尋流程
            pass

    # 將一般城市名稱嘗試映射到 IANA 時區
    candidates = _search_timezones_by_city(city)
    if not candidates:
        return {
            "status": "error",
            "error_message": f"Sorry, I couldn't resolve a timezone for '{city}'. Try an IANA name like 'Asia/Taipei'.",
        }

    # 若有多個候選，回傳清單供上層決策（避免選錯區）
    if len(candidates) > 1:
        # 可視需求：這裡也可加上偏好排序邏輯（例如偏好 'Asia/*', 'Europe/*' 等區域）
        top = sorted(candidates)
        return {
            "status": "error",
            "error_message": f"Multiple timezones matched '{city}'. Please choose one from 'candidates'.",
            "candidates": top[:10],  # 最多回 10 筆，避免過長
        }

    # 唯一匹配，直接回傳
    tz_name = candidates[0]
    try:
        tz = ZoneInfo(tz_name)
        now = datetime.datetime.now(tz)
        report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report, "timezone": tz_name, "candidates": None}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get time for '{city}' via timezone '{tz_name}': {e}",
        }


root_agent = Agent(
    name="weather_time_agent",
    model=litellm_model,
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather globally. "
        "For time queries, accept either an IANA timezone (e.g., 'Asia/Taipei') or a city name "
        "(e.g., 'Taipei'). When a city name is provided, attempt to resolve it to an IANA timezone "
        "by matching the last segment of available timezones. If multiple matches are found, return "
        "a list of candidates and ask the caller to choose one. For weather, respond with the current "
        "stubbed example unless a real weather API is integrated."
    ),
    tools=[get_weather, get_current_time],
)
