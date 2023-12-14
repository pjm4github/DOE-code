

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class Interpolator:
    def interpolate_linear(self, t, x0, y0, x1, y1):
        pass

    def interpolate_quadratic(self, t, x0, y0, x1, y1, x2, y2):
        pass


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def interpolate_linear(t, x0, y0, x1, y1):
    return y0 + (t - x0) * (y1 - y0) / (x1 - x0)


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def interpolate_quadratic(t, x0, y0, x1, y1, x2, y2):
    if x1 - x0 != x2 - x1:
        print("interpolate_quadratic: this only works given three equally spaced points")
        return 0.0
    h = x1 - x0
    c = y0
    b = (y1 - y0) / h
    a = (y2 - 2 * y1 + y0) / (2 * h * h)
    v = a * (t - x0) * (t - x1) + b * (t - x0) + c
    return v
