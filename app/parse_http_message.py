# 첫번째 방법
# \r\n으로 쪼개기
# \n을 대응 할 수 없는 문제
# decoded_data.split('\r\n')

# 두번째 방법
# \r\n을 \n으로 바꾸고
# \n으로 쪼개기
# 잘못하면 body의 데이터도 쪼개지는 문제
# decoded_data.replace('\r\n', '\n')
# decoded_data.split('\n')

# 세번째 방법


def split_by_line(data):
    split_by_line_data = []
    buffer = []
    carriage_return = '\r'
    line_feed = '\n'
    cr_flag = False
    body_flag = False
    previous_char = None

    for i in range(0, len(data)):
        current_char = data[i]

        if current_char == carriage_return:
            cr_flag = True

        if (not ((previous_char == carriage_return) ^ cr_flag)) and current_char == line_feed and not body_flag:
            if cr_flag:
                buffer = buffer[:(len(buffer) - 1)]

            if not buffer:
                body_flag = True

            split_by_line_data.append(''.join(buffer))

            buffer = []
        else:
            buffer.append(current_char)
            previous_char = current_char

    if buffer:
        if cr_flag:
            buffer = buffer[:(len(buffer) - 1)]

        split_by_line_data.append(''.join(buffer))

    return split_by_line_data


def parse(data):
    data_split_by_line = split_by_line(data)
    return data_split_by_line


if __name__ == "__main__":
    print(parse("GET /index.html HTTP/1.1\n\nsadklfj\nalsjf"))