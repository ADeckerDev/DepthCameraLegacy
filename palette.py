import math


def rgb_to_hex(rgb):
    r, g, b = (max(0, min(255, val)) for val in rgb)
    rgb = [r, g, b]
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


class Palette: # starter code
    def __init__(self):
        if type(self) is Palette:
            raise NotImplementedError("Palette is an abstract class and must be extended")
        self.num_colors = scale
        self.step = 1

    def get_color(self, n):
        raise NotImplementedError("Concrete subclass of Palette must override get_color()")

    def __len__(self):
        return self.num_colors

    def loop(self, request):
        x = request / float(self.num_colors)
        x = math.floor(x)
        index = request - (x * self.num_colors)
        if x % 2 == 1:  # Reverse index if odd
            index = self.num_colors - index - 1

        return self.get_color(index)

MAX_COLORS_PER_COLOR = 256 #this represents the maximum number of useful colors which can be made via linear interpolation without repeats

class singular_linear_interpolation(Palette):
    def __init__(self, start_color, end_color):
        self.num_colors = MAX_COLORS_PER_COLOR
        self.start_color = start_color
        self.end_color = end_color

    def loop(self, request):
        x = request / float(self.num_colors)
        x = math.floor(x)
        index = request - (x * self.num_colors)
        if x % 2 == 1: # if it is odd
            index = self.num_colors - index -1

        return self.get_color(index) # its kinda like recursion

    def __lerp_color__(self, color1, color2, x):
        r1, g1, b1 = color1
        r2, g2, b2, = color2

        t = x / float(self.num_colors - 1)

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)

        return [r, g, b]


    def get_color(self, n):
        if n > self.num_colors:
            return self.loop(n)
        
        return self.__lerp_color__(self.start_color, self.end_color, n)
    
class multiple_linear_interpolation(Palette):
    def __init__(self, colors):
        self.colors_len = len(colors)
        self.num_colors = int((self.colors_len - 1) * MAX_COLORS_PER_COLOR)

        # Initialize palettes for each segment
        self.palettes = [
            singular_linear_interpolation(colors[i], colors[i + 1])
            for i in range(len(colors) - 1)
        ]

    def get_color(self, n):
        if self.num_colors < n:
            return self.loop(n)

        # Determine the segment and local index
        segment_size = MAX_COLORS_PER_COLOR
        segment = int(n // segment_size)  # Ensure integer segment index
        local_index = n % segment_size  # Calculate local index within the segment

        # Clamp to last segment if out of bounds
        if segment >= len(self.palettes):
            segment = len(self.palettes) - 1
            local_index = MAX_COLORS_PER_COLOR - 1

        # Get the color from the correct palette
        return self.palettes[segment].get_color(local_index)


import colorsys

class hsl_cycle(Palette):
    def __init__(self, num_colors=360, start_offset=0, sat=.7, lightness=.5):
        num_colors = int(num_colors)
        self.saturation = sat
        self.lightness = lightness
        self.num_colors = num_colors
        self.start_offset = start_offset
        if num_colors < 360:
            self.scaling_factor = num_colors
        else:
            self.scaling_factor = 360
        self.start_offset = start_offset
    
    def get_color(self, n):
        # Get HSL values
        h = (self.start_offset/self.scaling_factor) + n * (1/self.scaling_factor)
        s = self.saturation
        l = self.lightness
        # normalize h
        h = h % 1

        #convert to rgb
        r, g, b = colorsys.hls_to_rgb(h, l, s)

        #scale
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        return [r, g, b]

class cos(Palette):
    def __init__(self, offset = 0):
        self.offset = offset
        

    def get_color(self, n):
        r = int(128 * math.cos(((2*math.pi) / 11) * (n + self.offset)) + 128)
        g = int(128 * math.cos(((2*math.pi) / 13) * (n + self.offset)) + 128)
        b = int(128 * math.cos(((2*math.pi) / 17) * (n + self.offset)) + 128)

        return [r, g, b]


import random

class noise(Palette):
    def __init__(self, seed = None, sat=.7, lightness=.5, offset = 0):
        if seed == None:
            seed = random.randint(0, 10000)
        self.offset = offset
        self.seed = seed
        self.noise = PerlinNoise(seed)
        self.saturation = sat
        self.lightness = lightness
    
    def get_color(self, n):
        noise = self.noise.get((n) + self.offset)
        h = noise
        s = self.saturation
        l = self.lightness
        # normalize h
        h = h % 1

        #convert to rgb
        r, g, b = colorsys.hls_to_rgb(h, l, s)

        #scale
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        return [r, g, b]
'''
    This code is for perlin noise, a popular and well documented noise function. I do not take credit for this function. It was invented far before I was ever born, back in 1983 by Ken Perlin. You can find information about the invention of perlin noise here:
    https://en.wikipedia.org/wiki/Perlin_noise#:~:text=Ken%20Perlin%20developed%20Perlin%20noise,called%20%22An%20Image%20Synthesizer%22.

    This implementation was initially made by alenxandr-grnk on github. I have taken the liberty of adapting and modifying it for this assignment. As it was posted open-source. Here is the original githup repo:

    https://github.com/alexandr-gnrk/perlin-1d/blob/main/perlin_noise.py
'''
class PerlinNoise():
    def __init__(self, 
            seed, amplitude=.5, frequency=1, 
            octaves=1):
        self.seed = random.Random(seed).random()
        self.amplitude = amplitude
        self.frequency = frequency
        self.octaves = octaves

        self.mem_x = dict()


    def __noise(self, x):
        # made for improve performance
        if x not in self.mem_x:
            self.mem_x[x] = random.Random(self.seed + x).uniform(-1, 1)
        return self.mem_x[x]


    def __interpolated_noise(self, x):
        prev_x = int(x) # previous integer
        next_x = prev_x + 1 # next integer
        frac_x = x - prev_x # fractional of x

        res = self.__cosine_interp(
            self.__noise(prev_x), 
            self.__noise(next_x),
            frac_x)

        return res


    def get(self, x):
        frequency = self.frequency
        amplitude = self.amplitude
        result = 0
        for _ in range(self.octaves):
            result += self.__interpolated_noise(x * frequency) * amplitude
            frequency *= 2
            amplitude /= 2

        return result



    def __cosine_interp(self, a, b, x):
        x2 = (1 - math.cos(x * math.pi)) / 2
        return a * (1 - x2) + b * x2



        
