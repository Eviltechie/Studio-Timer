def scale_to_range(old_val, old_min, old_max, new_min, new_max):
    return (((old_val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

# 255 / 3 = 85

def rainbow(hue, saturation, value):
    r = 0
    g = 0
    b = 0
    
    # red
    if 0 <= hue < 32: # red to orange
        r = scale_to_range(hue, 0, 32, 255, 170)
    elif 32 <= hue < 64: # orange to yellow
        r = 170
    elif 64 <= hue < 96: # yellow to green
        r = scale_to_range(hue, 64, 96, 170, 0)
    elif 160 <= hue <= 255: # blue to red
        r = scale_to_range(hue, 160, 255, 0, 255)

    # green
    if 0 <= hue < 96: # red to green
        g = scale_to_range(hue, 0, 96, 0, 255)
    elif 96 <= hue < 128: # green to aqua
        g = scale_to_range(hue, 96, 128, 255, 170)
    elif 128 <= hue < 160: # aqua to blue
        g = scale_to_range(hue, 128, 160, 170, 0)

    # blue
    if 96 <= hue < 128: # green to aqua
        b = scale_to_range(hue, 96, 128, 0, 85)
    elif 128 <= hue < 160: # aqua to blue
        b = scale_to_range(hue, 128, 160, 85, 255)
    elif 160 <= hue <= 255: # blue to red
        b = scale_to_range(hue, 160, 255, 255, 0)
        
    r = scale_to_range(saturation, 0, 255, 255, r)
    g = scale_to_range(saturation, 0, 255, 255, g)
    b = scale_to_range(saturation, 0, 255, 255, b)
    
    r = scale_to_range(value, 0, 255, 0, r)
    g = scale_to_range(value, 0, 255, 0, g)
    b = scale_to_range(value, 0, 255, 0, b)
    
    r = round(r)
    g = round(g)
    b = round(b)

    return (r, g, b)
