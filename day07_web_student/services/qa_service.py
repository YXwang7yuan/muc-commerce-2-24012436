from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # DONE 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    # 2. 流失情况：总体流失率、流失人数
    if any(word in normalized for word in ["流失率", "流失人数", "流失多少"]):
        loss_user = int(metrics["流失人数"])
        loss_rate = metrics.get("流失率", 0)
        return f"系统流失用户共{loss_user:,}人，总体流失率为{loss_rate:.1%}。"

    # 3. 偏好品类：用户最多的品类
    if any(word in normalized for word in ["哪个品类用户最多", "用户最多品类", "偏好品类"]):
        category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
        max_cat_row = category_df.loc[category_df["用户数"].idxmax()]
        cat_name = max_cat_row["PreferedOrderCat"]
        cat_user = int(max_cat_row["用户数"])
        return f"用户数量最多的偏好品类是「{cat_name}」，该品类用户共{cat_user:,}人。"

    # 4. 生命周期：流失风险最高阶段
    if any(word in normalized for word in ["哪个阶段风险最高", "流失最高阶段", "生命周期风险", "流失风险最高", "生命周期阶段"]):
        segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
        max_segment_row = segment_df.loc[segment_df["流失率"].idxmax()]
        stage_name = max_segment_row.get("TenureGroup", "未知")
        seg_loss_rate = max_segment_row["流失率"]
        return f"流失风险最高的生命周期阶段为「{stage_name}」，该阶段流失率高达{seg_loss_rate:.1%}。"

    # 5. 订单情况：平均订单数均值、中位数
    if any(word in normalized for word in ["平均订单数", "订单均值", "订单中位数"]):
        avg_order = metrics["平均订单数"]
        median_order = metrics["订单数中位数"]
        return f"用户平均订单数为{avg_order:.2f}单，订单数中位数为{median_order:.2f}单。"

    return (
        "抱歉，当前系统暂不支持该问题查询。你可以尝试询问：总用户数、总体流失情况、用户最多的偏好品类、流失风险最高的生命周期阶段、用户平均订单相关数据。"
    )
