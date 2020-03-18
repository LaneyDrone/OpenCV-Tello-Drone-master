import ImageTools as IT

img = IT.load_image('4a.png')
lines = IT.get_lines(img)

horizontal_lines = lines[0]
longest_line = horizontal_lines[0]
print(longest_line)

