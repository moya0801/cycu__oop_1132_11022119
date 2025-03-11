print(reversed('parrot'))
print(list(reversed('parrot')))
print(''.join(reversed('parrot')))

def reverse_word(word):
    return ''.join(reversed(word))

def is_palindrome(word):
    return word == word[::-1]

word_list = ['example', 'words', 'to', 'check', 'palindrome', 'racecar', 'level']

for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)