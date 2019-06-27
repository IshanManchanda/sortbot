import json

import requests

api = 'https://api.noopschallenge.com'


def start_exam():
	requests.get(api + '/sortbot')
	answer = {'login': 'IshanManchanda'}
	return requests.post(api + '/sortbot/exam/start', json=answer).json()


def try_answer(set_url, answer):
	return requests.post(api + set_url, json={'solution': answer}).json()


def get_answer(question, stage):
	vs = 'aeiou'
	if stage == 4:
		return sorted(question, reverse=True, key=len)

	if stage == 5:
		return sorted(question, key=lambda x: sum(map(x.count, vs)))

	if stage == 6:
		return sorted(question, key=lambda x: len(x) - sum(map(x.count, vs)))

	if stage == 7:
		return sorted(question, key=lambda x: len(x.split(' ')))
	return sorted(question)


def solve_set(set_url, stage):
	print(f'Starting set: {set_url} (stage {stage})')

	question = requests.get(api + set_url).json()
	print(json.dumps(question, indent=4))

	answer = get_answer(question['question'], stage)
	print(f'Solution is: {answer}')

	response = try_answer(set_url, answer)
	if response['result'] == 'finished':
		print(response)
		exit(0)

	elif response['result'] != 'success':
		print('Hmmm, something doesn\'t seem right')
		print(f'Set URL: {set_url}')
		print('Set:', json.dumps(question, indent=4))
		print(f'Answer: {answer}')
		exit(0)

	return response['nextSet']


def main():
	print("Starting...")
	set_url = start_exam()['nextSet']
	print(f'Initial set URL is: {set_url}')
	stage = 1

	while set_url:
		set_url = solve_set(set_url, stage)
		stage += 1


if __name__ == '__main__':
	main()
