import re


def convert_num(text):  # okay... but why tho? what about zero?
    return text.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five',
                                                                                                           '5').replace(
        'six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9')


def convert_duration(duration):
    duration = duration.lower()
    duration = convert_num(duration)
    numbers = re.findall(r'\d+(?:\.\d+)?', duration)

    dur_type_list = []
    for word in duration.split():
        if 'semester' in word.lower() or 'term' in word.lower() or 'hour' in word.lower() or 'day' in word.lower() or 'week' in word.lower() or 'month' in word.lower() or 'year' in word.lower():
            dur_type_list.append(word)  # put each word of the duration into the list

    # put all numbers contained in the duration in this list
    nums = []
    for number in numbers:
        if number != '':
            nums.append(number)

    for number in nums:
        for dur in dur_type_list:

            # CHECK FOR "YEAR" (But note that Year could also carry a month field in decimals!)
            if 'year' in dur:
                if '.' in number:
                    if re.findall(r'(?:\d+\.)?\d+', duration)[0] != 0:
                        return convert_duration(str(round(float(number) * 12)) + ' months')
                    return int(re.findall(r'(?:\d+\.)?\d+', duration)[0]), 'Year'
                else:
                    return int(number), 'Years'

            # CHECK FOR "MONTH"
            elif 'month' in dur:
                if '.' in number:
                    if re.findall(r'(?:\d+\.)?\d+', duration)[0] < 7:
                        return convert_duration(str(int(float(number) * 4)) + ' week')
                elif int(number) % 12 == 0:  # if the number is a sharp factor of 12
                    return int(int(number) / 12), 'Years'
                else:
                    return int(round(float(number))), 'Months'  # if not, just round it up and return months

            elif 'week' in dur:
                return round(int(number)), ' Weeks'
            elif 'hour' in dur:  # for real bruh??
                return int(number), 'Hours'
            elif 'semester' in dur:  # one semester being rounded to 6 months... sure.
                return convert_duration(str(int(number) * 6) + 'month')
            elif 'trimester' in dur:
                return convert_duration(str(int(number) * 3) + 'month')
            elif 'term' in dur:
                return convert_duration(str(int(number) * 6) + 'month')
            elif 'day' in dur:
                if '.' in number:
                    for jk in re.findall(r'\d+', duration):
                        if int(jk) > 1:
                            return convert_duration(str(int(float(number) * 24)) + 'hour')
                else:
                    return int(number), 'Days'
            else:
                return 'WRONG DATA'
