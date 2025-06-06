from django.shortcuts import render
from .forms import PuzzleForm
import random
import math

def puzzle_view(request):
    result = {}
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            text = form.cleaned_data['text']

            if number % 2 == 0:
                number_result = f"{number} is even. Its square root is {math.sqrt(number):.2f}."
            else:
                number_result = f"{number} is odd. Its cube is {number ** 3}."

            binary_text = ' '.join(format(ord(char), '08b') for char in text)
            vowel_count = sum(1 for c in text.lower() if c in 'aeiou')

            secret = random.randint(1, 100)
            attempts = []
            for i in range(1, 6):
                guess = random.randint(1, 100)
                if guess == secret:
                    attempts.append(f"Attempt {i}: {guess} (Correct!)")
                    success = True
                    break
                elif guess < secret:
                    attempts.append(f"Attempt {i}: {guess} (Too low!)")
                else:
                    attempts.append(f"Attempt {i}: {guess} (Too high!)")
            else:
                success = False

            treasure_result = f"You {'found' if success else 'did not find'} the treasure in {len(attempts)} attempts!"

            result = {
                'number_result': number_result,
                'binary': binary_text,
                'vowel_count': vowel_count,
                'attempts': attempts,
                'treasure_result': treasure_result,
            }
    else:
        form = PuzzleForm()

    return render(request, 'puzzle/index.html', {'form': form, 'result': result})
