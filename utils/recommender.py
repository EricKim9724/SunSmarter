def cloth_recommend():
    return "xdd"

def sunscreen_recommend(uv_index, height, weight, activity_type):
    # 计算防晒用量的函数
    def calculate_sunscreen_usage(uv_index, height, weight, activity_type):
        # 计算人体表面积
        body_surface_area = 0.0061 * height + 0.0124 * weight - 0.0099
        # 不同身体部位的占比
        body_parts_ratio = {
            'face': 0.03,
            'neck': 0.03,
            'arm': 0.09,
            'thigh': 0.09,
            'calf': 0.09,
            'chest': 0.18,
            'back': 0.18
        }
        # 不同活动形式的防晒用量因子
        activity_factors = {
            'Swimming/Water Activity': 2,
            'High Intensity Sports': 1.5,
            'Low Intensity Sports': 1
        }
        # 根据活动形式调整防晒用量
        activity_factor = activity_factors.get(activity_type, 1)
        # 计算每个身体部位的防晒用量
        sunscreen_usage = {}
        for body_part, ratio in body_parts_ratio.items():
            sunscreen_usage[body_part] = body_surface_area * ratio * 2 * activity_factor  # 使用2mg/平方厘米的防晒用量
        return sunscreen_usage

    # 根据用户选择的活动类型和UV指数值计算防晒用量
    sunscreen_usage = calculate_sunscreen_usage(uv_index, height, weight, activity_type)
    return pd.DataFrame.from_dict(sunscreen_usage, orient='index', columns=['Sunscreen Usage (ml)'])
