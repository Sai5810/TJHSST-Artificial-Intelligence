import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import random
from math import inf


def calc_dist(pix, r, c, m):
    return sum((pix[r, c][i] - m[i]) ** 2 for i in range(3))


def main():
    k = int(args[1])
    pix = img.load()
    print(f'Size: {img.size[0]} x {img.size[1]}')
    print(f'Pixels: {img.size[0] * img.size[1]}')
    pixel_map = {}
    for r in range(img.size[0]):
        for c in range(img.size[1]):
            if pix[r, c] in pixel_map:
                pixel_map[pix[r, c]] += 1
            else:
                pixel_map[pix[r, c]] = 1
    print(f'Distinct pixel count: {len(pixel_map)}')
    max_key = max(pixel_map, key=pixel_map.get)
    print(f'Most common pixel: {max_key} => {pixel_map[max_key]}')
    means = [pix[random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)] for _ in range(k)]
    prev_means = []
    while prev_means != means:
        prev_means = means
        clusters = [[] for _ in range(k)]
        pixel_map = {}
        for r in range(img.size[0]):
            for c in range(img.size[1]):
                if pix[r, c] in pixel_map:
                    clusters[pixel_map[pix[r, c]]].append(pix[r, c])
                else:
                    bdist = inf
                    bidx = 0
                    for idx, m in enumerate(means):
                        dist = calc_dist(pix, r, c, m)
                        if dist < bdist:
                            bidx = idx
                            bdist = dist
                    clusters[bidx].append(pix[r, c])
                    pixel_map[pix[r, c]] = bidx
        means = [tuple(sum(i) / len(c) for i in zip(*c)) for idx, c in enumerate(clusters)]
    final_means = [0] * k
    for r in range(img.size[0]):
        for c in range(img.size[1]):
            bdist = inf
            bidx = 0
            for idx, m in enumerate(means):
                dist = calc_dist(pix, r, c, m)
                if dist < bdist:
                    bidx = idx
                    bdist = dist
            img.putpixel((r, c), tuple(round(i) for i in means[bidx]))
            final_means[bidx] += 1
    print("Final means:")
    for i in range(k):
        print(f'{i+1}: {means[i]} => {final_means[i]}')
    img.save("kmeans/2023svaka.png", "PNG")
    print("Region counts: ", end="")
    edges = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    vis = set()
    reg_cts = {}
    for r in range(img.size[0]):
        for c in range(img.size[1]):
            if (r, c) not in vis:
                color = pix[r, c]
                if color in reg_cts:
                    reg_cts[color] += 1
                else:
                    reg_cts[color] = 1
                st = [(r, c)]
                while st:
                    cur = st[0]
                    st = st[1:]
                    if cur not in vis:
                        vis.add(cur)
                        for x, y in edges:
                            edge = (cur[0] + x, cur[1] + y)
                            if 0 <= edge[0] < img.size[0] and 0 <= edge[1] < img.size[1] and pix[edge] == color:
                                st.append(edge)
    print(*reg_cts.values(), sep=", ")


if __name__ == '__main__':
    main()
# Sai Vaka, Period 5, 2023
