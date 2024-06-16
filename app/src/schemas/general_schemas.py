from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LLMType(str, Enum):
    yagpt_neuro = 'yagpt_neuro' # search api + yagpt
    yagpt = 'yagpt'
    saiga = 'saiga'
    # gigachat = 'gigachat'


class InputModeX(str, Enum):
    auto = 'auto'
    input = 'input'
    date = 'date'


class InputModeY(str, Enum):
    auto = 'auto'
    input = 'input'


class BlockType(str, Enum):
    curve_chart = 'curve_chart' 
    bar_chart = 'bar_chart'
    pie_chart = 'pie_chart'
    grid = 'grid'
    text = 'text'


class ReportType(str, Enum):
    template = 'template'
    doc = 'doc'


class LinkCreate(BaseModel):
    # id: int
    # report_id: int
    content: str


class BlockCreate(BaseModel):
    # id: int
    # report_id: int
    title: str
    axis_x: str = ''
    axis_y: str = ''
    input_mode_x: InputModeX = InputModeX.input
    input_mode_y: InputModeY = InputModeY.input
    block_type: BlockType = BlockType.bar_chart
    json_data: dict | None = None


class ReportSettingCreate(BaseModel):
    # id: int
    # report_id: int
    theme: str
    full_theme: str
    start_date: datetime
    end_date: datetime
    llm_model: LLMType = LLMType.saiga


class ReportCreate(BaseModel):
    # user_id: int
    name: str | None = None
    report_type: ReportType = ReportType.template
    create_date: datetime

    blocks: list[BlockCreate]
    links: list[LinkCreate]
    report_settings: ReportSettingCreate


# READ MODELS
class LinkRead(LinkCreate):
    id: int


class BlockRead(BlockCreate):
    id: int


class ReportSettingRead(ReportSettingCreate):
    id: int


class ReportRead(ReportCreate):
    id: int
    user_id: int
    blocks: list[BlockRead]
    links: list[LinkRead]
    report_settings: ReportSettingRead


class BlockUpdate(BlockCreate):
    id: int | None = None


class ReportUpdate(ReportCreate):
    id: int
    user_id: int
    blocks: list[BlockUpdate]
    links: list[LinkRead]
    report_settings: ReportSettingRead
