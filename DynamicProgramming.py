


def fibonacci(n):
    # This function calculates the nth Fibonacci number using dynamic programming.
    # It builds up a table of results for all numbers up to n, so we don't repeat work.
    if n <= 0:
        # If n is 0 or negative, return 0 (base case)
        return 0
    if n == 1:
        # If n is 1, return 1 (base case)
        return 1
    # Create a list to store Fibonacci numbers up to n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1  # Set the first two Fibonacci numbers
    for i in range(2, n + 1):
        # For each number from 2 to n, calculate its Fibonacci value
        # by adding the two previous Fibonacci numbers
        dp[i] = dp[i - 1] + dp[i - 2]
    # Return the nth Fibonacci number
    return dp[n]

if __name__ == "__main__":
    # This block will only run if the script is executed directly (not imported)
    # We'll print the first 10 Fibonacci numbers to show how our function works.
    for i in range(10):
        # For each number from 0 to 9, calculate and print its Fibonacci number
        print(f"F({i}) = {fibonacci(i)}")