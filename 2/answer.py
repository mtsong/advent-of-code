USE_EXAMPLE = False
power_sum = 0
with open("2/example.txt" if USE_EXAMPLE else "2/input.txt", encoding="utf-8") as f:
    for game in f:
        pulls = game.strip().split(":")[1].strip().split(";")
        red_min = green_min = blue_min = 0
        for pull in pulls:
            draws = pull.strip().split(",")
            for draw in draws:
                number, color = draw.strip().split()
                number = int(number)
                if color == "red" and number > red_min:
                    red_min = number
                elif color == "green" and number > green_min:
                    green_min = number
                elif color == "blue" and number > blue_min:
                    blue_min = number
        print(red_min, green_min, blue_min)
        if (red_min * green_min * blue_min) == 0:
            print(f"Game {game.strip().split(':').split()[1]} is missing a color")
        power_sum += red_min * green_min * blue_min
    print(power_sum)
