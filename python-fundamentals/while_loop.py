exam_score = []
while True:

    subject = input("Enter subject (or 'done' to finish): ")
    if subject.lower() == "done":
        break
    try:
        score = float(input(f"Enter score for {subject}: "))
        exam_score.append((subject, score))

    except ValueError as e:
        print("Invalid input. Please enter a number or 'done'.", e)
        continue
total_score = 0
for subject, score in exam_score:
    print(f"{subject}: {score}")
    total_score += score
print(f"Total score: {total_score}")
