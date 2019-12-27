
def test_decorator(func=None):
	def wrapper(*args, **kwargs):
		print()
		print(f"Test: {func.__name__}")
		print(f"\tArguments: {args}")
		print(f"\tKeyword Arguments: {kwargs}")
		print("-", end=" ")

		return func(*args, **kwargs,)

	return wrapper
